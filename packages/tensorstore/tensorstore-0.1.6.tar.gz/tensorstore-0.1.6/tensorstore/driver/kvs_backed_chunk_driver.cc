// Copyright 2020 The TensorStore Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "tensorstore/driver/kvs_backed_chunk_driver.h"

#include "absl/container/fixed_array.h"
#include "tensorstore/driver/kvs_backed_chunk_driver_impl.h"
#include "tensorstore/internal/box_difference.h"
#include "tensorstore/internal/cache_key.h"
#include "tensorstore/internal/cache_pool_resource.h"
#include "tensorstore/internal/data_copy_concurrency_resource.h"
#include "tensorstore/internal/staleness_bound_json_binder.h"
#include "tensorstore/util/bit_vec.h"
#include "tensorstore/util/iterate_over_index_range.h"
#include "tensorstore/util/quote_string.h"

namespace tensorstore {
namespace internal_kvs_backed_chunk_driver {

OpenState::~OpenState() = default;

Result<IndexTransform<>> DataCache::GetExternalToInternalTransform(
    const void* metadata, std::size_t component_index) {
  return IndexTransform<>();
}

OpenState::OpenState(Initializer initializer)
    : PrivateOpenState{std::move(initializer.spec),
                       initializer.read_write_mode} {
  request_time_ = absl::Now();
}

std::string OpenState::GetMetadataCacheKey() { return {}; }

Result<KeyValueStore::Ptr> OpenState::GetMetadataKeyValueStore(
    KeyValueStore::Ptr base_kv_store) {
  return base_kv_store;
}

Result<KeyValueStore::Ptr> OpenState::GetDataKeyValueStore(
    KeyValueStore::Ptr base_kv_store, const void* metadata) {
  return base_kv_store;
}

ReadWriteMode OpenState::GetReadWriteMode(const void* metadata) {
  return ReadWriteMode::read_write;
}

AtomicUpdateConstraint OpenState::GetCreateConstraint() {
  return AtomicUpdateConstraint::kRequireMissing;
}

MetadataCache::MetadataCache(Initializer initializer)
    : Base(KeyValueStore::Ptr(), initializer.data_copy_concurrency->executor),
      data_copy_concurrency_(std::move(initializer.data_copy_concurrency)),
      cache_pool_(std::move(initializer.cache_pool)) {}

DataCache::DataCache(Initializer initializer,
                     internal::ChunkGridSpecification grid)
    : Base(std::move(initializer.store),
           GetOwningCache(initializer.metadata_cache_entry)->executor(),
           std::move(grid)),
      metadata_cache_entry_(std::move(initializer.metadata_cache_entry)),
      initial_metadata_(initializer.metadata),
      validated_metadata_(std::move(initializer.metadata)) {}

namespace {

/// Returns an error status indicating that a resize request would implicitly
/// affect a region of dimension `output_dim`, or an out-of-bounds region.
///
/// If `affected_inclusive_min <= affected_exclusive_max`, then the error
/// indicates that the resize would affect the region
/// `[affected_inclusive_min, affected_exclusive_max)`.  If
/// `affected_inclusive_min > affected_exclusive_max`, then the error indicates
/// that the resize request was made with a view containing an out-of-bounds
/// region.
///
/// \param output_dim The output dimension number to be included in the error
///     message.
/// \param affected_inclusive_min Either the inclusive lower bound of the
///     affected region, or the exclusive upper bound of the out-of-bounds
///     region.
/// \param affected_exclusive_max Either the exclusive upper bound of the
///     affected region, or the inclusive lower bound of the out-of-bounds
///     region.
/// \dchecks `affected_inclusive_min != affected_exclusive_max`.
Status ShapeConstraintError(DimensionIndex output_dim,
                            DimensionIndex affected_inclusive_min,
                            DimensionIndex affected_exclusive_max) {
  assert(affected_inclusive_min != affected_exclusive_max);
  if (affected_inclusive_min < affected_exclusive_max) {
    return absl::FailedPreconditionError(
        StrCat("Resize operation would also affect output dimension ",
               output_dim, " over the interval ",
               IndexInterval::UncheckedHalfOpen(affected_inclusive_min,
                                                affected_exclusive_max),
               " but `resize_tied_bounds` was not specified"));
  }
  return absl::FailedPreconditionError(
      StrCat("Resize operation would also affect output dimension ", output_dim,
             " over the out-of-bounds interval ",
             IndexInterval::UncheckedHalfOpen(affected_exclusive_max,
                                              affected_inclusive_min)));
}

IndexInterval GetNewIndexInterval(IndexInterval existing,
                                  Index new_inclusive_min,
                                  Index new_exclusive_max) {
  return IndexInterval::UncheckedHalfOpen(
      ExplicitIndexOr(new_inclusive_min, existing.inclusive_min()),
      ExplicitIndexOr(new_exclusive_max, existing.exclusive_max()));
}

/// Validates that `current_domain` is compatible with
/// `{inclusive_min,exclusive_max}_constraint`.
///
/// For each value in `{inclusive_min,exclusive_max}_constraint` that is not
/// `kImplicit`, the corresponding bound of `current_domain` must be equal.
///
/// \param current_domain The current bounds.
/// \param inclusive_min_constraint The inclusive min constraint vector of
///     length `current_domain.rank()`.
/// \param exclusive_max_constraint The inclusive max constraint vector of
///     length `current_domain.rank()`.
/// \dchecks `current_domain.rank() == inclusive_min_constraint.size()`
/// \dchecks `current_domain.rank() == exclusive_max_constraint.size()`
/// \return `Status()` if compatible.
/// \error `absl::StatusCode::kFailedPrecondition` if not compatible.
Status ValidateResizeDomainConstraint(
    BoxView<> current_domain, span<const Index> inclusive_min_constraint,
    span<const Index> exclusive_max_constraint) {
  assert(current_domain.rank() == inclusive_min_constraint.size());
  assert(current_domain.rank() == exclusive_max_constraint.size());
  for (DimensionIndex i = 0; i < current_domain.rank(); ++i) {
    const IndexInterval cur_interval = current_domain[i];
    if (!ImplicitOrEqual(inclusive_min_constraint[i],
                         cur_interval.inclusive_min())) {
      return ShapeConstraintError(i, cur_interval.inclusive_min(),
                                  inclusive_min_constraint[i]);
    }
    if (!ImplicitOrEqual(exclusive_max_constraint[i],
                         cur_interval.exclusive_max())) {
      return ShapeConstraintError(i, exclusive_max_constraint[i],
                                  cur_interval.exclusive_max());
    }
  }
  return absl::OkStatus();
}

/// Validates that `new_{inclusive_min,exclusive_max}` differ from
/// `current_domain` only as allowed by the `expand_only` and `shrink_only`
/// constraints.
///
/// \param current_domain The existing domain.
/// \param new_inclusive_min The new inclusive min bounds of length
///     `current_domain.rank()`, where a value of `kImplicit` indicates no
///     change.
/// \param new_exclusive_max The new exclusive max bounds of length
///     `current_domain.rank()`, where a value of `kImplicit` indicates no
///     change.
/// \param expand_only If `true`, the bounds must not shrink.
/// \param shrink_only If `true`, the bounds must not expand.
/// \returns `OkStatus()` if the constraints are satisfied.
/// \error `absl::StatusCode::kFailedPrecondition` if the constraints are not
///     satisfied.
/// \dchecks `current_domain.rank() == new_inclusive_min.size()`
/// \dchecks `current_domain.rank() == new_exclusive_max.size()`
Status ValidateExpandShrinkConstraints(BoxView<> current_domain,
                                       span<const Index> new_inclusive_min,
                                       span<const Index> new_exclusive_max,
                                       bool expand_only, bool shrink_only) {
  assert(current_domain.rank() == new_inclusive_min.size());
  assert(current_domain.rank() == new_exclusive_max.size());
  for (DimensionIndex i = 0; i < current_domain.rank(); ++i) {
    const IndexInterval cur_interval = current_domain[i];
    const IndexInterval new_interval = GetNewIndexInterval(
        cur_interval, new_inclusive_min[i], new_exclusive_max[i]);
    if (shrink_only && !Contains(cur_interval, new_interval)) {
      return absl::FailedPreconditionError(
          StrCat("Resize operation would expand output dimension ", i, " from ",
                 cur_interval, " to ", new_interval,
                 " but `shrink_only` was specified"));
    }
    if (expand_only && !Contains(new_interval, cur_interval)) {
      return absl::FailedPreconditionError(
          StrCat("Resize operation would shrink output dimension ", i, " from ",
                 cur_interval, " to ", new_interval,
                 " but `expand_only` was specified"));
    }
  }
  return absl::OkStatus();
}

/// Validates that the parsed metadata in the metadata cache entry associated
/// with `cache` is compatible with the existing metadata from which `cache` was
/// constructed.
///
/// If the metadata has changed in an incompatible way (e.g. a change to the
/// chunk shape), returns an error.  Otherwise, sets
/// `cache->validated_metadata_` to the new parsed metadata.
Result<std::shared_ptr<const void>> ValidateNewMetadata(DataCache* cache) {
  auto new_metadata = cache->metadata_cache_entry_->GetMetadata();
  absl::MutexLock lock(&cache->mutex_);
  TENSORSTORE_RETURN_IF_ERROR(cache->ValidateMetadataCompatibility(
      cache->validated_metadata_.get(), new_metadata.get()));
  cache->validated_metadata_ = new_metadata;
  return new_metadata;
}

void GetComponentBounds(DataCache* data_cache, const void* metadata,
                        std::size_t component_index, MutableBoxView<> bounds,
                        BitSpan<std::uint64_t> implicit_lower_bounds,
                        BitSpan<std::uint64_t> implicit_upper_bounds) {
  const auto& grid = data_cache->grid();
  const auto& component_spec = grid.components[component_index];
  assert(bounds.rank() == component_spec.rank());
  assert(implicit_lower_bounds.size() == bounds.rank());
  assert(implicit_upper_bounds.size() == bounds.rank());
  Box<dynamic_rank(internal::kNumInlinedDims)> grid_bounds(
      grid.chunk_shape.size());
  BitVec<> grid_implicit_lower_bounds(grid_bounds.rank());
  BitVec<> grid_implicit_upper_bounds(grid_bounds.rank());
  data_cache->GetChunkGridBounds(metadata, grid_bounds,
                                 grid_implicit_lower_bounds,
                                 grid_implicit_upper_bounds);
  span<const DimensionIndex> chunked_to_cell_dimensions =
      component_spec.chunked_to_cell_dimensions;
  bounds.DeepAssign(component_spec.fill_value.domain());
  implicit_lower_bounds.fill(false);
  implicit_upper_bounds.fill(false);
  for (DimensionIndex grid_dim = 0; grid_dim < grid_bounds.rank(); ++grid_dim) {
    const DimensionIndex cell_dim = chunked_to_cell_dimensions[grid_dim];
    bounds[cell_dim] = grid_bounds[grid_dim];
    implicit_lower_bounds[cell_dim] = grid_implicit_lower_bounds[grid_dim];
    implicit_upper_bounds[cell_dim] = grid_implicit_upper_bounds[grid_dim];
  }
}

struct ResolveBoundsContinuation {
  internal::CachePtr<DataCache> cache;
  IndexTransform<> transform;
  std::size_t component_index;
  ResolveBoundsOptions options;
  Result<IndexTransform<>> operator()(const Result<void>& result) {
    TENSORSTORE_RETURN_IF_ERROR(result);
    TENSORSTORE_ASSIGN_OR_RETURN(auto new_metadata,
                                 ValidateNewMetadata(cache.get()));
    return ResolveBoundsFromMetadata(cache.get(), new_metadata.get(),
                                     component_index, std::move(transform),
                                     options);
  }
};

}  // namespace

Future<IndexTransform<>> DriverBase::ResolveBounds(
    IndexTransform<> transform, ResolveBoundsOptions options) {
  return ResolveBounds(transform, metadata_staleness_bound_, options);
}

Future<IndexTransform<>> DriverBase::ResolveBounds(
    IndexTransform<> transform, StalenessBound metadata_staleness_bound,
    ResolveBoundsOptions options) {
  auto* cache = this->cache();

  return MapFuture(
      cache->executor(),
      ResolveBoundsContinuation{internal::CachePtr<DataCache>(cache),
                                std::move(transform), component_index(),
                                options},
      cache->metadata_cache_entry_->Read(metadata_staleness_bound));
}

namespace {

/// Enqueues a request to resize the chunked dimensions of a DataCache.
///
/// \param cache The DataCache to resize.
/// \param parameters Specifies the resize request.
/// \param request_time Time at which the request was initiated (affects
///     retrying in the case of concurrent modifications).
/// \returns A `Future` that becomes ready when the request completes
///     successfully or with an error.  Must call `Force` to ensure the request
///     is actually issued.
Future<const void> RequestResize(DataCache* cache, ResizeParameters parameters,
                                 absl::Time request_time) {
  return cache->metadata_cache_entry_->RequestAtomicUpdate(
      /*update=*/
      [parameters = std::move(parameters),
       cache = internal::CachePtr<DataCache>(cache),
       metadata_constraint = cache->initial_metadata_](
          const void* current_metadata) -> Result<std::shared_ptr<const void>> {
        if (!current_metadata) {
          return absl::NotFoundError("Metadata was deleted");
        }
        TENSORSTORE_RETURN_IF_ERROR(cache->ValidateMetadataCompatibility(
            metadata_constraint.get(), current_metadata));
        Box<dynamic_rank(internal::kNumInlinedDims)> bounds(
            parameters.new_inclusive_min.size());
        BitVec<> implicit_lower_bounds(bounds.rank());
        BitVec<> implicit_upper_bounds(bounds.rank());
        cache->GetChunkGridBounds(current_metadata, bounds,
                                  implicit_lower_bounds, implicit_upper_bounds);
        // The resize request has already been validated against explicit grid
        // bounds (i.e. bounds corresponding to `false` values in
        // `implicit_{lower,upper}_bounds`), so we don't need to check again
        // here.
        TENSORSTORE_RETURN_IF_ERROR(ValidateResizeConstraints(
            bounds, parameters.new_inclusive_min, parameters.new_exclusive_max,
            parameters.inclusive_min_constraint,
            parameters.exclusive_max_constraint, parameters.expand_only,
            parameters.shrink_only));

        return cache->GetResizedMetadata(current_metadata,
                                         parameters.new_inclusive_min,
                                         parameters.new_exclusive_max);
      },
      AtomicUpdateConstraint::kRequireExisting, request_time);
}

struct ResizeContinuation {
  internal::CachePtr<DataCache> cache;
  std::size_t component_index;
  IndexTransform<> transform;
  Result<IndexTransform<>> GetResult() {
    TENSORSTORE_ASSIGN_OR_RETURN(auto new_metadata,
                                 ValidateNewMetadata(cache.get()));
    return ResolveBoundsFromMetadata(cache.get(), new_metadata.get(),
                                     component_index, std::move(transform),
                                     /*options=*/{});
  }

  void operator()(Promise<IndexTransform<>> promise, ReadyFuture<const void>) {
    promise.SetResult(GetResult());
  }
};

struct ResizeState {
  internal::CachePtr<DataCache> cache;
  std::size_t component_index;
  absl::Time request_time;
  IndexTransform<> transform;
  ResizeParameters resize_parameters;
};

void SubmitResizeRequest(Promise<IndexTransform<>> promise, ResizeState state) {
  auto* cache_ptr = state.cache.get();
  LinkValue(WithExecutor(cache_ptr->executor(),
                         ResizeContinuation{std::move(state.cache),
                                            state.component_index,
                                            std::move(state.transform)}),
            std::move(promise),
            RequestResize(cache_ptr, std::move(state.resize_parameters),
                          state.request_time));
}

struct DeleteChunksForResizeContinuation {
  std::unique_ptr<ResizeState> state;
  void operator()(Promise<IndexTransform<>> promise, ReadyFuture<const void>) {
    SubmitResizeRequest(std::move(promise), std::move(*state));
  }
};

Future<const void> DeleteChunksForResize(internal::CachePtr<DataCache> cache,
                                         BoxView<> current_bounds,
                                         span<const Index> new_inclusive_min,
                                         span<const Index> new_exclusive_max) {
  span<const Index> chunk_shape = cache->grid().chunk_shape;
  const DimensionIndex rank = chunk_shape.size();
  assert(current_bounds.rank() == rank);
  assert(new_inclusive_min.size() == rank);
  assert(new_exclusive_max.size() == rank);
  auto pair = PromiseFuturePair<void>::Make(MakeResult(Status()));
  pair.future.Force();
  Box<dynamic_rank(internal::kNumInlinedDims)> current_grid_bounds(rank);
  Box<dynamic_rank(internal::kNumInlinedDims)> new_grid_bounds(rank);
  for (DimensionIndex i = 0; i < rank; ++i) {
    const IndexInterval cur_dim_bounds = current_bounds[i];
    const IndexInterval new_dim_bounds = IndexInterval::UncheckedHalfOpen(
        ExplicitIndexOr(new_inclusive_min[i], cur_dim_bounds.inclusive_min()),
        ExplicitIndexOr(new_exclusive_max[i], cur_dim_bounds.exclusive_max()));
    const Index chunk_size = chunk_shape[i];
    current_grid_bounds[i] = DividePositiveRoundOut(cur_dim_bounds, chunk_size);
    new_grid_bounds[i] = DividePositiveRoundOut(new_dim_bounds, chunk_size);
  }
  internal::BoxDifference box_difference(current_grid_bounds, new_grid_bounds);
  Box<dynamic_rank(internal::kNumInlinedDims)> part(rank);
  if (!box_difference.valid()) {
    return absl::InvalidArgumentError(StrCat("Resize would require more than ",
                                             std::numeric_limits<Index>::max(),
                                             " chunk regions to be deleted"));
  }
  for (Index box_i = 0; box_i < box_difference.num_sub_boxes(); ++box_i) {
    box_difference.GetSubBox(box_i, part);
    IterateOverIndexRange(part, [&](span<const Index> cell_indices) {
      auto entry = cache->GetEntryForCell(cell_indices);
      LinkError(pair.promise, entry->Delete());
    });
  }
  return pair.future;
}

struct ResolveBoundsForDeleteAndResizeContinuation {
  std::unique_ptr<ResizeState> state;
  void operator()(Promise<IndexTransform<>> promise, ReadyFuture<const void>) {
    TENSORSTORE_ASSIGN_OR_RETURN(auto new_metadata,
                                 ValidateNewMetadata(state->cache.get()),
                                 static_cast<void>(promise.SetResult(_)));
    // Chunks should never be deleted if `expand_only==false`.
    const DimensionIndex grid_rank = state->cache->grid().chunk_shape.size();
    assert(!state->resize_parameters.expand_only);
    Box<dynamic_rank(internal::kNumInlinedDims)> bounds(grid_rank);
    BitVec<> implicit_lower_bounds(grid_rank);
    BitVec<> implicit_upper_bounds(grid_rank);
    state->cache->GetChunkGridBounds(new_metadata.get(), bounds,
                                     implicit_lower_bounds,
                                     implicit_upper_bounds);
    // The resize request has already been validated against explicit grid
    // bounds (i.e. bounds corresponding to `false` values in
    // `implicit_{lower,upper}_bounds`), so we don't need to check again here.
    TENSORSTORE_RETURN_IF_ERROR(
        ValidateResizeConstraints(
            bounds, state->resize_parameters.new_inclusive_min,
            state->resize_parameters.new_exclusive_max,
            state->resize_parameters.inclusive_min_constraint,
            state->resize_parameters.exclusive_max_constraint,
            /*expand_only=*/false,
            /*shrink_only=*/state->resize_parameters.shrink_only),
        static_cast<void>(promise.SetResult(_)));
    auto* state_ptr = state.get();
    LinkValue(
        WithExecutor(state_ptr->cache->executor(),
                     DeleteChunksForResizeContinuation{std::move(state)}),
        std::move(promise),
        DeleteChunksForResize(state_ptr->cache, bounds,
                              state_ptr->resize_parameters.new_inclusive_min,
                              state_ptr->resize_parameters.new_exclusive_max));
  }
};
}  // namespace

Future<IndexTransform<>> DriverBase::Resize(IndexTransform<> transform,
                                            span<const Index> inclusive_min,
                                            span<const Index> exclusive_max,
                                            ResizeOptions options) {
  auto* cache = this->cache();
  auto resize_parameters = GetResizeParameters(
      cache, cache->initial_metadata_.get(), component_index(), transform,
      inclusive_min, exclusive_max, options);
  if (!resize_parameters) {
    if (resize_parameters.status().code() == absl::StatusCode::kAborted) {
      // Requested resize is a no-op.  Currently there is no resize option
      // corresponding to the `fix_resizable_bounds` resolve option, so we
      // don't specify it.
      return ResolveBounds(std::move(transform), /*staleness=*/{},
                           /*options=*/{});
    }
    return resize_parameters.status();
  }

  auto pair = PromiseFuturePair<IndexTransform<>>::Make();
  const absl::Time request_time = absl::Now();
  ResizeState resize_state{
      /*.cache=*/internal::CachePtr<DataCache>(cache),
      /*.component_index=*/component_index(),
      /*.request_time=*/request_time,
      /*.transform=*/std::move(transform),
      /*.resize_parameters=*/std::move(*resize_parameters),
  };
  if ((options.mode & resize_metadata_only) == resize_metadata_only ||
      (options.mode & expand_only) == expand_only) {
    // No existing data chunks need to be deleted.  Just update the metadata.
    SubmitResizeRequest(std::move(pair.promise), std::move(resize_state));
  } else {
    // Delete any out-of-bounds data chunks before updating the metadata.
    LinkValue(WithExecutor(
                  cache->executor(),
                  ResolveBoundsForDeleteAndResizeContinuation{
                      std::make_unique<ResizeState>(std::move(resize_state))}),
              std::move(pair.promise),
              cache->metadata_cache_entry_->Read(request_time));
  }
  return std::move(pair.future);
}

Result<IndexTransformSpec> DriverBase::GetBoundSpecData(
    SpecT<internal::ContextBound>* spec, IndexTransformView<> transform_view) {
  auto* cache = this->cache();
  auto* metadata_cache = cache->metadata_cache();
  TENSORSTORE_ASSIGN_OR_RETURN(spec->store,
                               metadata_cache->base_store()->GetBoundSpec());
  spec->data_copy_concurrency = metadata_cache->data_copy_concurrency_;
  spec->cache_pool = metadata_cache->cache_pool_;
  spec->delete_existing = false;
  spec->open = true;
  spec->create = false;
  spec->allow_metadata_mismatch = false;
  spec->staleness.metadata = this->metadata_staleness_bound();
  spec->staleness.data = this->data_staleness_bound();
  spec->rank = this->rank();
  spec->data_type = this->data_type();

  std::shared_ptr<const void> validated_metadata;
  {
    absl::ReaderMutexLock lock(&cache->mutex_);
    validated_metadata = cache->validated_metadata_;
  }

  TENSORSTORE_RETURN_IF_ERROR(cache->GetBoundSpecData(
      spec, validated_metadata.get(), this->component_index()));

  IndexTransform<> transform(transform_view);

  TENSORSTORE_ASSIGN_OR_RETURN(
      auto external_to_internal_transform,
      cache->GetExternalToInternalTransform(validated_metadata.get(),
                                            component_index()));
  if (external_to_internal_transform.valid()) {
    TENSORSTORE_ASSIGN_OR_RETURN(
        auto internal_to_external_transform,
        InverseTransform(external_to_internal_transform));
    TENSORSTORE_ASSIGN_OR_RETURN(
        transform,
        ComposeTransforms(internal_to_external_transform, transform));
  }

  return IndexTransformSpec{transform};
}

Status DriverBase::ConvertSpec(SpecT<internal::ContextUnbound>* spec,
                               const SpecRequestOptions& options) {
  if (options.staleness) {
    spec->staleness = *options.staleness;
  }
  return spec->OpenModeSpec::ConvertSpec(options);
}

namespace {
/// Validates that the open request specified by `state` can be applied to
/// `metadata`.
Result<std::size_t> ValidateOpenRequest(OpenState* state,
                                        const void* metadata) {
  if (!metadata) {
    return absl::NotFoundError(
        StrCat("Metadata key ",
               QuoteString(GetMetadataCache(*state)->GetMetadataStorageKey(
                   GetMetadataCacheEntry(*state)->key())),
               " does not exist"));
  }
  auto& base = *(PrivateOpenState*)state;  // Cast to private base
  return state->GetComponentIndex(metadata, base.spec_->open_mode());
}

/// \pre `component_index` is the result of a previous call to
///     `state->GetComponentIndex` with the same `metadata`.
/// \pre `metadata != nullptr`
Result<internal::Driver::ReadWriteHandle> CreateTensorStoreFromMetadata(
    OpenState::Ptr state, std::shared_ptr<const void> metadata,
    std::size_t component_index) {
  auto& base = *(PrivateOpenState*)state.get();  // Cast to private base
  // TODO(jbms): The read-write mode should be determined based on the
  // KeyValueStore mode, once that is exposed.
  auto read_write_mode = state->GetReadWriteMode(metadata.get());
  if (base.read_write_mode_ != ReadWriteMode::dynamic) {
    TENSORSTORE_RETURN_IF_ERROR(internal::ValidateSupportsModes(
        read_write_mode, base.read_write_mode_));
    read_write_mode = base.read_write_mode_;
  }

  std::string chunk_cache_identifier;
  if (!base.metadata_cache_key_.empty()) {
    auto data_cache_key = state->GetDataCacheKey(metadata.get());
    if (!data_cache_key.empty()) {
      internal::EncodeCacheKey(&chunk_cache_identifier, data_cache_key,
                               base.metadata_cache_key_);
    }
  }
  Status data_key_value_store_status;
  auto chunk_cache =
      (*state->cache_pool())
          ->GetCache<DataCache>(
              chunk_cache_identifier, [&]() -> std::unique_ptr<DataCache> {
                auto store_result = state->GetDataKeyValueStore(
                    GetMetadataCache(*state)->base_store_, metadata.get());
                if (!store_result) {
                  data_key_value_store_status =
                      std::move(store_result).status();
                  return nullptr;
                }
                return state->GetDataCache(
                    {std::move(*store_result),
                     GetMetadataCacheEntry(std::move(*state)), metadata});
              });
  TENSORSTORE_RETURN_IF_ERROR(data_key_value_store_status);
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto new_transform,
      chunk_cache->GetExternalToInternalTransform(
          chunk_cache->initial_metadata_.get(), component_index));

  TENSORSTORE_ASSIGN_OR_RETURN(
      new_transform,
      ResolveBoundsFromMetadata(chunk_cache.get(), metadata.get(),
                                component_index, std::move(new_transform),
                                /*options=*/{}));
  internal::Driver::Ptr driver(state->AllocateDriver(
      {std::move(chunk_cache), component_index,
       base.spec_->staleness.BoundAtOpen(base.request_time_)}));
  return internal::Driver::ReadWriteHandle{
      {std::move(driver), std::move(new_transform)}, read_write_mode};
}

/// Called when the metadata has been written (successfully or unsuccessfully).
struct HandleWroteMetadata {
  OpenState::Ptr state;
  void operator()(Promise<internal::Driver::ReadWriteHandle> promise,
                  ReadyFuture<const void> future) {
    auto& base = *(PrivateOpenState*)state.get();  // Cast to private base
    auto& result = future.result();
    if (!result) {
      // Creation of new array metadata failed.
      if (result.status().code() != absl::StatusCode::kAlreadyExists ||
          !base.spec_->open) {
        promise.SetResult(result.status());
        return;
      }
      // Creation of the array failed due to it already existing.  Attempt to
      // open the existing array.
    }
    promise.SetResult([&]() -> Result<internal::Driver::ReadWriteHandle> {
      auto metadata = GetMetadataCacheEntry(*state)->GetMetadata();
      TENSORSTORE_ASSIGN_OR_RETURN(
          std::size_t component_index,
          ValidateOpenRequest(state.get(), metadata.get()));
      return CreateTensorStoreFromMetadata(
          std::move(state), std::move(metadata), component_index);
    }());
  }
};

/// Attempts to create new array.
void CreateMetadata(OpenState::Ptr state,
                    Promise<internal::Driver::ReadWriteHandle> promise) {
  auto state_ptr = state.get();
  auto& base = *(PrivateOpenState*)state.get();  // Cast to private base
  LinkValue(
      WithExecutor(state_ptr->executor(),
                   HandleWroteMetadata{std::move(state)}),
      std::move(promise),
      GetMetadataCacheEntry(*state_ptr)
          ->RequestAtomicUpdate(
              [state = state_ptr](const void* existing_metadata)
                  -> Result<std::shared_ptr<const void>> {
                auto result = state->Create(existing_metadata);
                if (result) return result;
                return MaybeAnnotateStatus(
                    result.status(),
                    StrCat("Error creating array with metadata key ",
                           QuoteString(
                               GetMetadataCache(*state)->GetMetadataStorageKey(
                                   GetMetadataCacheEntry(*state)->key()))));
              },
              state_ptr->GetCreateConstraint(), base.request_time_));
}

/// Called when the metadata has been read (successfully or not found).
struct HandleReadMetadata {
  OpenState::Ptr state;
  void operator()(Promise<internal::Driver::ReadWriteHandle> promise,
                  ReadyFuture<const void> metadata_future) {
    auto metadata = GetMetadataCacheEntry(*state)->GetMetadata();
    auto& base = *(PrivateOpenState*)state.get();  // Cast to private base
    auto component_index_result =
        ValidateOpenRequest(state.get(), metadata.get());
    if (component_index_result) {
      promise.SetResult(CreateTensorStoreFromMetadata(
          std::move(state), std::move(metadata), *component_index_result));
      return;
    }
    if (component_index_result.status().code() == absl::StatusCode::kNotFound) {
      if (base.spec_->create) {
        CreateMetadata(std::move(state), std::move(promise));
        return;
      }
    }
    promise.SetResult(component_index_result.status());
  }
};

/// Called when the metadata should be requested or created.
struct GetMetadataForOpen {
  OpenState::Ptr state;
  void operator()(Promise<internal::Driver::ReadWriteHandle> promise) {
    auto& base = *(PrivateOpenState*)state.get();  // Cast to private base
    auto state_ptr = state.get();
    if (base.spec_->open) {
      LinkValue(WithExecutor(state_ptr->executor(),
                             HandleReadMetadata{std::move(state)}),
                std::move(promise),
                GetMetadataCacheEntry(*state_ptr)
                    ->Read(base.spec_->staleness.metadata));
      return;
    }
    // `tensorstore::Open` ensures that at least one of `OpenMode::create` and
    // `OpenMode::open` is specified.
    assert(base.spec_->create);
    CreateMetadata(std::move(state), std::move(promise));
  }
};

/// Called when the KeyValueStore has been successfully opened.
struct HandleKeyValueStoreReady {
  OpenState::Ptr state;
  void operator()(Promise<internal::Driver::ReadWriteHandle> promise,
                  ReadyFuture<const void> store) {
    auto& base = *(PrivateOpenState*)state.get();  // Cast to private base
    auto* state_ptr = state.get();
    if (base.spec_->delete_existing) {
      // Delete all keys starting with the key prefix.
      auto prefix_for_delete = state->GetPrefixForDeleteExisting();
      LinkValue(std::bind(WithExecutor(state_ptr->executor(),
                                       GetMetadataForOpen{std::move(state)}),
                          std::placeholders::_1),
                std::move(promise),
                GetMetadataCache(*state_ptr)
                    ->base_store_->DeleteRange(
                        KeyRange::Prefix(std::move(prefix_for_delete))));
      return;
    }
    // Immediately proceed with reading/creating the metadata.
    GetMetadataForOpen callback{std::move(state)};
    callback(std::move(promise));
  }
};

}  // namespace

Future<const void> MetadataCache::Entry::RequestAtomicUpdate(
    UpdateFunction update, AtomicUpdateConstraint update_constraint,
    absl::Time request_time) {
  auto [promise, future] = PromiseFuturePair<void>::Make();
  auto writeback_future = AddPendingWrite(
      PendingWrite{std::move(update), update_constraint, promise},
      (update_constraint == AtomicUpdateConstraint::kRequireExisting)
          ? WriteFlags::kConditionalWriteback
          : WriteFlags::kUnconditionalWriteback,
      request_time);
  LinkError(std::move(promise), std::move(writeback_future));
  return std::move(future);
}

void MetadataCache::DoDecode(
    internal::AsyncStorageBackedCache::PinnedEntry base_entry,
    std::optional<absl::Cord> value) {
  auto* entry = static_cast<Entry*>(base_entry.get());
  MetadataPtr new_metadata;
  if (value) {
    TENSORSTORE_ASSIGN_OR_RETURN(
        new_metadata, this->DecodeMetadata(entry->key(), *value),
        this->NotifyReadError(entry,
                              ConvertInvalidArgumentToFailedPrecondition(_)));
  }
  auto lock = entry->AcquireReadStateWriterLock();
  entry->metadata = std::move(new_metadata);
  this->NotifyReadSuccess(entry, std::move(lock));
}

std::string MetadataCache::GetKeyValueStoreKey(internal::Cache::Entry* entry) {
  return this->GetMetadataStorageKey(entry->key());
}

void MetadataCache::NotifyWritebackNeedsRead(internal::Cache::Entry* base_entry,
                                             WriteStateLock lock,
                                             absl::Time staleness_bound) {
  auto* entry = static_cast<Entry*>(base_entry);
  if (absl::c_all_of(entry->issued_writes, [](const PendingWrite& request) {
        return request.update_constraint ==
               AtomicUpdateConstraint::kRequireMissing;
      })) {
    std::vector<PendingWrite> issued_requests;
    std::swap(issued_requests, entry->issued_writes);
    Base::NotifyWritebackSuccess(entry, std::move(lock).Upgrade());
    for (auto& request : issued_requests) {
      int junk = 0;
      // Pass in a bogus non-null pointer.  The update function is guaranteed to
      // return an error.
      request.promise.raw_result() = request.update(&junk).status();
    }
    return;
  }
  Base::NotifyWritebackNeedsRead(entry, std::move(lock), staleness_bound);
}

void MetadataCache::NotifyWritebackSuccess(internal::Cache::Entry* base_entry,
                                           WriteAndReadStateLock lock) {
  auto* entry = static_cast<Entry*>(base_entry);
  entry->metadata = std::move(entry->new_metadata);
  Base::NotifyWritebackSuccess(entry, std::move(lock));
}

void MetadataCache::DoWriteback(internal::Cache::PinnedEntry entry) {
  executor()([entry = internal::static_pointer_cast<Entry>(std::move(entry))] {
    MetadataPtr new_metadata;
    // Indicates whether there is an update request newer than the metadata.
    absl::Time newest_request_time;
    {
      auto lock = entry->AcquireWriteStateLock();
      newest_request_time = entry->last_pending_write_time;
      const void* existing_metadata = entry->metadata.get();
      for (const auto& request : entry->pending_writes) {
        auto result = request.update(existing_metadata);
        if (result) {
          assert(*result);
          assert(request.update_constraint !=
                     AtomicUpdateConstraint::kRequireMissing ||
                 existing_metadata == nullptr);
          assert(request.update_constraint !=
                     AtomicUpdateConstraint::kRequireExisting ||
                 existing_metadata != nullptr);
          new_metadata = std::move(*result);
          existing_metadata = new_metadata.get();
          request.promise.raw_result() = MakeResult();
        } else {
          request.promise.raw_result() = std::move(result).status();
        }
      }
      GetOwningCache(entry)->NotifyWritebackStarted(entry.get(),
                                                    std::move(lock));
    }
    auto* cache = GetOwningCache(entry);
    if (!new_metadata) {
      // None of the requested changes are compatible with the current state.
      if (newest_request_time > entry->last_read_time) {
        // At least one update request is newer than the current metadata.
        // Request an updated "read state".
        cache->Base::NotifyWritebackNeedsRead(
            entry.get(), entry->AcquireWriteStateLock(), newest_request_time);
      } else {
        // Complete the writeback successfully (but all pending requests will
        // fail).
        cache->Base::NotifyWritebackSuccess(
            entry.get(), entry->AcquireWriteAndReadStateLock());
      }
      return;
    }
    TENSORSTORE_ASSIGN_OR_RETURN(
        auto encoded, cache->EncodeMetadata(entry->key(), new_metadata.get()),
        cache->Base::NotifyWritebackError(entry.get(),
                                          entry->AcquireWriteStateLock(), _));
    entry->new_metadata = std::move(new_metadata);
    cache->Writeback(std::move(entry), std::move(encoded),
                     /*unconditional=*/false);
  });
}

std::string DataCache::GetKeyValueStoreKey(internal::Cache::Entry* base_entry) {
  auto* entry = static_cast<Entry*>(base_entry);
  return GetChunkStorageKey(initial_metadata_.get(), entry->cell_indices());
}

void DataCache::DoDecode(internal::Cache::PinnedEntry base_entry,
                         std::optional<absl::Cord> value) {
  auto* entry = static_cast<Entry*>(base_entry.get());
  if (!value) {
    this->NotifyReadSuccess(entry, entry->AcquireReadStateWriterLock(),
                            /*components=*/{});
    return;
  }
  const auto validated_metadata = this->validated_metadata();
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto decoded,
      this->DecodeChunk(validated_metadata.get(), entry->cell_indices(),
                        std::move(*value)),
      this->NotifyReadError(entry,
                            ConvertInvalidArgumentToFailedPrecondition(_)));
  this->NotifyReadSuccess(entry, entry->AcquireReadStateWriterLock(),
                          /*components=*/decoded);
}

void DataCache::DoWriteback(internal::Cache::PinnedEntry base_entry) {
  executor()([entry = internal::static_pointer_cast<Entry>(
                  std::move(base_entry))]() mutable {
    auto* cache = static_cast<DataCache*>(GetOwningCache(entry));
    std::optional<absl::Cord> encoded;
    ChunkCache::WritebackSnapshot snapshot(entry.get());
    if (!snapshot.equals_fill_value()) {
      const auto validated_metadata = cache->validated_metadata();
      // Convert from array of `SharedArrayView<const void>` to array of
      // `ArrayView<const void>`.
      absl::FixedArray<ArrayView<const void>, 2> component_arrays_unowned(
          snapshot.component_arrays().begin(),
          snapshot.component_arrays().end());
      TENSORSTORE_ASSIGN_OR_RETURN(
          encoded,
          cache->EncodeChunk(validated_metadata.get(), entry->cell_indices(),
                             component_arrays_unowned),
          cache->NotifyWritebackError(entry.get(),
                                      entry->AcquireWriteStateLock(), _));
    }
    cache->Writeback(std::move(entry), std::move(encoded),
                     snapshot.unconditional());
  });
}

namespace {
/// Returns the metadata cache for `state`, creating it if it doesn't already
/// exist.
///
/// The key used to lookup the cache depends on the
/// `KeyValueStore::Bound::Spec`; the actual `KeyValueStore` has not yet been
/// opened.
///
/// The returned `metadata_cache` must not be used for read or write operations
/// until the `metadata_cache->initialized_` future becomes ready.  This
/// asynchronous initialization pattern is needed in order to asynchronously
/// open the `KeyValueStore` when the metadata cache is created.
internal::CachePtr<MetadataCache> GetOrCreateMetadataCache(OpenState* state) {
  auto& base = *(PrivateOpenState*)state;  // Cast to private base

  auto& spec = *base.spec_;
  internal::EncodeCacheKey(&base.metadata_cache_key_, spec.store,
                           typeid(*state), state->GetMetadataCacheKey());
  // Set to a promise paired with the `initialized_` future if the cache is
  // created.
  Promise<void> metadata_cache_promise;
  MetadataCache* created_metadata_cache = nullptr;
  auto metadata_cache =
      (*state->cache_pool())
          ->GetCache<MetadataCache>(
              base.metadata_cache_key_,
              [&]() -> std::unique_ptr<MetadataCache> {
                auto metadata_cache =
                    state->GetMetadataCache({base.spec_->data_copy_concurrency,
                                             base.spec_->cache_pool});
                created_metadata_cache = metadata_cache.get();
                auto [promise, future] =
                    PromiseFuturePair<void>::Make(MakeResult());
                metadata_cache->initialized_ = std::move(future);
                metadata_cache_promise = std::move(promise);
                return metadata_cache;
              });
  // Even if we just created a new cache, it is possible that another cache for
  // the same cache_identifier was created concurrently, in which case the cache
  // we just created should be discarded.
  if (metadata_cache_promise.valid() &&
      metadata_cache.get() == created_metadata_cache) {
    // The cache didn't previously exist.  Open the KeyValueStore.
    LinkValue(
        [state = OpenState::Ptr(state), metadata_cache](
            Promise<void> metadata_cache_promise,
            ReadyFuture<KeyValueStore::Ptr> future) {
          metadata_cache->base_store_ = *future.result();
          TENSORSTORE_ASSIGN_OR_RETURN(
              auto metadata_kvstore,
              state->GetMetadataKeyValueStore(metadata_cache->base_store_),
              static_cast<void>(metadata_cache_promise.SetResult(_)));
          metadata_cache->SetKeyValueStore(std::move(metadata_kvstore));
        },
        metadata_cache_promise, spec.store->Open());
  }
  return metadata_cache;
}
}  // namespace

Future<internal::Driver::ReadWriteHandle> OpenDriver(OpenState::Ptr state) {
  auto& base = *(PrivateOpenState*)state.get();  // Cast to private base
  auto& spec = *base.spec_;
  TENSORSTORE_RETURN_IF_ERROR(
      spec.OpenModeSpec::Validate(base.read_write_mode_));
  auto* state_ptr = state.get();
  auto metadata_cache = GetOrCreateMetadataCache(state_ptr);
  base.metadata_cache_entry_ =
      GetCacheEntry(metadata_cache, state->GetMetadataCacheEntryKey());
  return PromiseFuturePair<internal::Driver::ReadWriteHandle>::LinkValue(
             HandleKeyValueStoreReady{std::move(state)},
             metadata_cache->initialized_)
      .future;
}

Result<IndexTransform<>> ResolveBoundsFromMetadata(
    DataCache* data_cache, const void* new_metadata,
    std::size_t component_index, IndexTransform<> transform,
    ResolveBoundsOptions options) {
  auto& grid = data_cache->grid();
  const DimensionIndex base_rank = grid.components[component_index].rank();
  BitVec<> base_implicit_lower_bounds(base_rank);
  BitVec<> base_implicit_upper_bounds(base_rank);
  Box<dynamic_rank(internal::kNumInlinedDims)> base_bounds(base_rank);
  GetComponentBounds(data_cache, new_metadata, component_index, base_bounds,
                     base_implicit_lower_bounds, base_implicit_upper_bounds);
  if ((options.mode & fix_resizable_bounds) == fix_resizable_bounds) {
    base_implicit_lower_bounds.fill(false);
    base_implicit_upper_bounds.fill(false);
  }
  return PropagateBoundsToTransform(
      BoxView<>(base_bounds),
      BitSpan<const std::uint64_t>(base_implicit_lower_bounds),
      BitSpan<const std::uint64_t>(base_implicit_upper_bounds),
      std::move(transform));
}

Status ValidateResizeConstraints(BoxView<> current_domain,
                                 span<const Index> new_inclusive_min,
                                 span<const Index> new_exclusive_max,
                                 span<const Index> inclusive_min_constraint,
                                 span<const Index> exclusive_max_constraint,
                                 bool expand_only, bool shrink_only) {
  TENSORSTORE_RETURN_IF_ERROR(ValidateResizeDomainConstraint(
      current_domain, inclusive_min_constraint, exclusive_max_constraint));
  TENSORSTORE_RETURN_IF_ERROR(ValidateExpandShrinkConstraints(
      current_domain, new_inclusive_min, new_exclusive_max, expand_only,
      shrink_only));
  return absl::OkStatus();
}

Result<ResizeParameters> GetResizeParameters(
    DataCache* data_cache, const void* metadata, size_t component_index,
    IndexTransformView<> transform, span<const Index> inclusive_min,
    span<const Index> exclusive_max, ResizeOptions options) {
  assert(transform.input_rank() == inclusive_min.size());
  assert(transform.input_rank() == exclusive_max.size());
  const DimensionIndex output_rank = transform.output_rank();

  const auto& grid = data_cache->grid();
  const DimensionIndex base_rank = grid.components[component_index].rank();
  BitVec<> base_implicit_lower_bounds(base_rank);
  BitVec<> base_implicit_upper_bounds(base_rank);
  Box<dynamic_rank(internal::kNumInlinedDims)> base_bounds(base_rank);
  GetComponentBounds(data_cache, metadata, component_index, base_bounds,
                     base_implicit_lower_bounds, base_implicit_upper_bounds);

  const DimensionIndex grid_rank = grid.grid_rank();

  using FixedIndexVec = absl::FixedArray<Index, internal::kNumInlinedDims>;

  FixedIndexVec new_output_inclusive_min(output_rank);
  FixedIndexVec new_output_exclusive_max(output_rank);
  FixedIndexVec output_inclusive_min_constraint(output_rank);
  FixedIndexVec output_exclusive_max_constraint(output_rank);

  bool is_noop;
  TENSORSTORE_RETURN_IF_ERROR(PropagateInputDomainResizeToOutput(
      transform, inclusive_min, exclusive_max,
      /*can_resize_tied_bounds=*/(options.mode & resize_tied_bounds) ==
          resize_tied_bounds,
      output_inclusive_min_constraint, output_exclusive_max_constraint,
      new_output_inclusive_min, new_output_exclusive_max, &is_noop));

  if (is_noop) return absl::AbortedError("");

  if (grid.components.size() != 1 && !(options.mode & resize_tied_bounds)) {
    return absl::FailedPreconditionError(
        "Resize operation would affect other fields but "
        "`resize_tied_bounds` was not specified");
  }

  // Validate that new bounds and constraints are compatible with non-resizable
  // bounds.
  for (DimensionIndex output_dim = 0; output_dim < output_rank; ++output_dim) {
    const IndexInterval dim_bounds = base_bounds[output_dim];
    if (!base_implicit_lower_bounds[output_dim]) {
      const Index min_constraint = output_inclusive_min_constraint[output_dim];
      if (!ImplicitOrEqual(min_constraint, dim_bounds.inclusive_min())) {
        return ShapeConstraintError(output_dim, dim_bounds.inclusive_min(),
                                    min_constraint);
      }
      const Index new_inclusive_min = new_output_inclusive_min[output_dim];
      if (!ImplicitOrEqual(new_inclusive_min, dim_bounds.inclusive_min())) {
        return absl::FailedPreconditionError(
            StrCat("Cannot change inclusive lower bound of output dimension ",
                   output_dim, ", which is fixed at ",
                   dim_bounds.inclusive_min(), ", to ", new_inclusive_min));
      }
    }
    if (!base_implicit_upper_bounds[output_dim]) {
      const Index max_constraint = output_exclusive_max_constraint[output_dim];
      if (!ImplicitOrEqual(max_constraint, dim_bounds.exclusive_max())) {
        return ShapeConstraintError(output_dim, max_constraint,
                                    dim_bounds.exclusive_max());
      }
      const Index new_exclusive_max = new_output_exclusive_max[output_dim];
      if (!ImplicitOrEqual(new_exclusive_max, dim_bounds.exclusive_max())) {
        return absl::FailedPreconditionError(
            StrCat("Cannot change exclusive upper bound of output dimension ",
                   output_dim, ", which is fixed at ",
                   dim_bounds.exclusive_max(), ", to ", new_exclusive_max));
      }
    }
  }

  // Convert resize request on component dimensions to chunk dimensions.
  span<const DimensionIndex> chunked_to_cell_dimensions =
      grid.components[component_index].chunked_to_cell_dimensions;

  std::vector<Index> new_grid_inclusive_min(grid_rank);
  std::vector<Index> new_grid_exclusive_max(grid_rank);
  std::vector<Index> grid_inclusive_min_constraint(grid_rank);
  std::vector<Index> grid_exclusive_max_constraint(grid_rank);

  for (DimensionIndex i = 0; i < grid_rank; ++i) {
    const DimensionIndex j = chunked_to_cell_dimensions[i];
    new_grid_inclusive_min[i] = new_output_inclusive_min[j];
    new_grid_exclusive_max[i] = new_output_exclusive_max[j];
    grid_inclusive_min_constraint[i] = output_inclusive_min_constraint[j];
    grid_exclusive_max_constraint[i] = output_exclusive_max_constraint[j];
  }

  return ResizeParameters{
      /*.new_inclusive_min=*/new_grid_inclusive_min,
      /*.new_exclusive_max=*/new_grid_exclusive_max,
      /*.inclusive_min_constraint=*/grid_inclusive_min_constraint,
      /*.exclusive_max_constraint=*/grid_exclusive_max_constraint,
      /*.expand_only=*/(options.mode & expand_only) == expand_only,
      /*.shrink_only=*/(options.mode & shrink_only) == shrink_only};
}

DriverBase::DriverBase(Initializer&& initializer)
    : internal::ChunkCacheDriver(std::move(initializer.cache),
                                 initializer.component_index,
                                 initializer.staleness_bounds.data),
      metadata_staleness_bound_(initializer.staleness_bounds.metadata) {}

DataCache* DriverBase::cache() const {
  return static_cast<DataCache*>(internal::ChunkCacheDriver::cache());
}

Executor DriverBase::data_copy_executor() { return cache()->executor(); }

namespace jb = tensorstore::internal::json_binding;
TENSORSTORE_DEFINE_JSON_BINDER(
    SpecJsonBinder,
    jb::Sequence(
        jb::Member(internal::DataCopyConcurrencyResource::id,
                   jb::Projection(&SpecT<>::data_copy_concurrency)),
        jb::Member(internal::CachePoolResource::id,
                   jb::Projection(&SpecT<>::cache_pool)),
        jb::Member("kvstore", jb::Projection(&SpecT<>::store)),
        jb::Projection(
            &SpecT<>::staleness,
            jb::Sequence(
                jb::Member("recheck_cached_metadata",
                           jb::Projection(&StalenessBounds::metadata,
                                          jb::DefaultValue([](auto* obj) {
                                            obj->bounded_by_open_time = true;
                                          }))),
                jb::Member("recheck_cached_data",
                           jb::Projection(&StalenessBounds::data,
                                          jb::DefaultInitializedValue())))),
        internal::OpenModeSpecJsonBinder));

}  // namespace internal_kvs_backed_chunk_driver
}  // namespace tensorstore
