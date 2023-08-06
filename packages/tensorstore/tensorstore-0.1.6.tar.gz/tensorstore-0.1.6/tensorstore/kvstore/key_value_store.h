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

#ifndef TENSORSTORE_KVSTORE_KEY_VALUE_H_
#define TENSORSTORE_KVSTORE_KEY_VALUE_H_

/// \file
/// Asynchronous key-value storage interface.
///
/// This file define the interface for using a KeyValueStore.  See `registry.h`
/// for the interface for defining a KeyValueStore driver.
///
/// There are three representations of a KeyValueStore that may be used for
/// different purposes:
///
/// 1. `KeyValueStore::Spec` specifies the parameters necessary to open/create a
///    `KeyValueStore`, including the driver id as well as any relevant
///    driver-specific options.  Parsing a `KeyValueStore::Spec` from JSON does
///    not involve any I/O and does not depend on a `Context` object.
///    Consequently, any references to context resources in the JSON
///    specification are left unresolved.
///
/// 2. `KeyValueStore::BoundSpec::Ptr` specifies the parameters and resources
///    necessary to open/create a `KeyValueStore` after resolving any resources
///    from a specified `Context`.  Converting from a `KeyValueStore::Spec` to a
///    `KeyValueStore::BoundSpec::Ptr` still does not involve any I/O, however.
///    In most cases it is unnecessary to work with the `BoundSpec`
///    representation directly, but it is useful for calculating a cache key
///    without actually opening the `KeyValueStore`, and for composition.
///
/// 3. `KeyValueStore::Ptr` is a handle to an open key value store that may be
///    used to perform reads and writes to the underlying key value store.  It
///    is opened asynchronously from a `KeyValueStore::BoundSpec::Ptr` or from a
///    `Context` and a `KeyValueStore::Spec` (and this open operation may
///    involve I/O).
///
/// The `KeyValueStore::Spec` and `KeyValueStore::BoundSpec::Ptr`
/// representations may be used to validate a JSON specification without
/// actually performing any I/O.
///
/// Example of opening directly:
///
///     Future<KeyValueStore::Ptr> store =
///         KeyValueStore::Open(Context::Default(), {"driver", "memory"});
///
/// Example of opening via `KeyValueStore::Spec`:
///
///     KeyValueStore::Spec spec =
///         KeyValueStore::Spec::FromJson({"driver", "memory"}).value();
///
///     Future<KeyValueStore::Ptr> store = spec.Open(Context::Default());
///
/// Example of opening via `KeyValueStore::Spec` and
/// `KeyValueStore::BoundSpec::Ptr`:
///
///     KeyValueStore::Spec spec =
///         KeyValueStore::Spec::FromJson({"driver", "memory"}).value();
///
///     KeyValueStore::BoundSpec::Ptr bound_spec =
///         spec.Bind(Context::Default()).value();
///
///     std::string store_cache_key;
///     internal::EncodeCacheKey(&store_cache_key, bound_spec);
///
///     // Compute derived cache key based on `store_cache_key`.  If already
///     // present in cache of opened objects, use existing object and return.
///
///     Future<KeyValueStore::Ptr> store = bound_spec->Open();
///
/// Some internal-only KeyValueStore implementations may not support
/// construction from a JSON specification.

#include <functional>
#include <iosfwd>
#include <optional>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

#include "absl/strings/cord.h"
#include "absl/time/time.h"
#include <nlohmann/json.hpp>
#include "tensorstore/context.h"
#include "tensorstore/internal/context_binding.h"
#include "tensorstore/internal/intrusive_ptr.h"
#include "tensorstore/kvstore/byte_range.h"
#include "tensorstore/kvstore/generation.h"
#include "tensorstore/kvstore/key_range.h"
#include "tensorstore/util/future.h"
#include "tensorstore/util/result.h"
#include "tensorstore/util/sender.h"
#include "tensorstore/util/status.h"

namespace tensorstore {

class KeyValueStore;
using KeyValueStorePtr = internal::IntrusivePtr<KeyValueStore>;

namespace internal {
template <typename Derived>
class RegisteredKeyValueStore;
template <typename Derived>
class RegisteredKeyValueStoreSpec;
template <typename Derived>
class RegisteredKeyValueStoreBoundSpec;
}  // namespace internal

/// Abstract base class representing a KeyValueStore specification, for creating
/// a `KeyValueStore` from a JSON representation.
///
/// A `KeyValueStoreSpec` object specifies:
///
/// - The driver id (as a string);
///
/// - Any driver-specific options, such as a cloud storage bucket or path to the
///   data, and `Context::ResourceSpec` objects for any necessary credentials or
///   concurrency pools.
///
/// - A `Context::Spec` with context resource specifications that may be
///   referenced by driver-specific context resource specifications; these
///   context resource specifications override any resources provided by the
///   `Context` object used to bind/open the `KeyValueStoreSpec`.
///
/// For each `Derived` KeyValueStore driver implementation that supports a JSON
/// representation, `internal::RegisteredKeyValueStoreSpec<Derived>` defined in
/// `registry.h` serves as the corresponding `KeyValueStoreSpec` implementation.
class KeyValueStoreSpec
    : public internal::AtomicReferenceCount<KeyValueStoreSpec> {
  friend class KeyValueStore;

 public:
  /// Driver-agnostic options that may be specified when opening a
  /// `KeyValueStore`, which may alter the interpretation of the
  /// `KeyValueStoreSpec`.
  ///
  /// Currently, no options are supported.
  struct OpenOptions {};

  /// Opens a `KeyValueStore` from this specification.
  Future<KeyValueStorePtr> Open(const Context& context,
                                const OpenOptions& options = {}) const;

  /// Returns the driver id.
  const std::string& driver() const;

  /// Returns the associated context resource specification.
  const Context::Spec& context() const { return context_spec_; }

  using ToJsonOptions = Context::ToJsonOptions;
  using FromJsonOptions = Context::FromJsonOptions;

  /// KeyValueStoreSpec objects are always managed using a reference-counted
  /// `Ptr`.
  ///
  /// Conversion to/from JSON is supported via
  /// `KeyValueStore::Spec::Ptr::{ToJson,FromJson}`.
  class Ptr : public internal::IntrusivePtr<KeyValueStoreSpec> {
    using Base = internal::IntrusivePtr<KeyValueStoreSpec>;

   public:
    using Base::Base;
    TENSORSTORE_DECLARE_JSON_DEFAULT_BINDER(Ptr, FromJsonOptions, ToJsonOptions)
  };

  /// Options that may be specified to alter an existing `Spec` in a
  /// driver-agnostic way.
  ///
  /// Currently, this is the same as `OpenOptions`.
  using RequestOptions = OpenOptions;

  /// Returns a modified specification according to `options`.
  virtual Result<Ptr> Convert(const RequestOptions& options) const;

  /// Representation of a KeyValueStore specification after context resources
  /// are resolved.
  ///
  /// This representation can be used to obtain a cache key representing the
  /// `KeyValueStore`, and to validate the context resource bindings.  It is not
  /// normally needed except to implement other composed `KeyValueStore` or
  /// `TensorStore` drivers.
  class Bound;
  using BoundPtr = internal::IntrusivePtr<const Bound>;

  /// Resolves any context references using `context` and returns a
  /// `BoundSpec` representation.
  virtual Result<BoundPtr> Bind(const Context& context) const;

  virtual ~KeyValueStoreSpec();

 private:
  template <typename Derived>
  friend class internal::RegisteredKeyValueStore;
  template <typename Derived>
  friend class internal::RegisteredKeyValueStoreSpec;
  template <typename Derived>
  friend class internal::RegisteredKeyValueStoreBoundSpec;
  /// Specifies context resource overrides.
  Context::Spec context_spec_;
};

/// `KeyValueStoreSpec` bound to a `Context`, normally used only in the
/// implementation of other composed `KeyValueStore` or `TensorStore` drivers.
///
/// All `Context` resources required by the driver are fully resolved.
///
/// This provides an interface to obtain the cache key for a given
/// `KeyValueStoreSpec` (which depends on the `Context`) without actually
/// opening the `KeyValueStore`.
///
/// Instances of this class should be managed using a
/// `KeyValueStore::Spec::BoundPtr` reference-counted smart pointer.
///
/// For each `Derived` KeyValueStore driver implementation that supports a JSON
/// representation, `internal::RegisteredKeyValueStoreBoundSpec<Derived>`
/// defined in `registry.h` serves as the corresponding
/// `KeyValueStoreSpec::Bound` implementation.
class KeyValueStoreSpec::Bound
    : public AtomicReferenceCount<KeyValueStoreSpec::Bound> {
 public:
  using Ptr = internal::IntrusivePtr<const Bound>;

  /// Encodes any relevant parameters as a cache key.  This should only include
  /// parameters relevant after the `KeyValueStore` is open that determine
  /// whether two `KeyValueStore` objects may be used interchangeably.
  /// Parameters that only affect creation should be excluded.
  virtual void EncodeCacheKey(std::string* out) const = 0;

  Future<KeyValueStorePtr> Open() const;

  virtual KeyValueStoreSpec::Ptr Unbind(
      const internal::ContextSpecBuilder& builder = {}) const = 0;

  virtual ~Bound();

 private:
  virtual Future<KeyValueStorePtr> DoOpen() const = 0;

  /// For compatibility with `tensorstore::internal::EncodeCacheKey`.
  friend void EncodeCacheKeyAdl(std::string* out, const Ptr& ptr) {
    ptr->EncodeCacheKey(out);
  }
};

struct KeyValueStoreReadOptions {
  /// The read is aborted if the generation associated with the stored `key`
  /// matches `if_not_equal`.  The special values of
  /// `StorageGeneration::Unknown()` (the default) or
  /// `StorageGeneration::NoValue()` disable this condition.
  StorageGeneration if_not_equal;

  /// The read is aborted if the generation associated with `key` does not
  /// match `if_equal`.  This is primarily useful in conjunction with a
  /// `byte_range` request to ensure consistency.
  ///
  /// - The special value of `StorageGeneration::Unknown()` (the default)
  ///   disables this condition.
  ///
  /// - The special value of `StorageGeneration::NoValue()` specifies a
  ///   condition that the value not exist.  This condition is valid but of
  ///   limited use since the only possible read results are "not found" and
  ///   "aborted".
  StorageGeneration if_equal;

  /// Cached data may be used without validation if not older than
  /// `staleness_bound`.  Cached data older than `staleness_bound` must be
  /// validated before being returned.  A value of `absl::InfiniteFuture()` (the
  /// default) indicates that the result must be current as of the time the
  /// `Read` request was made, i.e. it is equivalent to specifying the value of
  /// `absl::Now()` just before invoking `Read`.
  absl::Time staleness_bound{absl::InfiniteFuture()};

  /// Specifies the byte range.
  OptionalByteRangeRequest byte_range;
};

/// Abstract base class representing a key-value store.
///
/// Support for different storage systems is provided by individual key-value
/// store drivers, which are defined as derived classes of `KeyValueStore`.
/// Drivers that support a JSON representation should inherit from the CRTP base
/// `RegisteredKeyValueStore` defined in `registry.h`.
///
/// `KeyValueStore` uses intrusive reference counting. `KeyValueStore` objects
/// must always be heap-allocated with ownership managed through a
/// `KeyValueStore::Ptr`.
///
/// Destroying all references to the `Future` returned from `Read`, `Write`, or
/// `Delete` may (depending on the derived class implementation) cancel the
/// operation.
///
/// The user is not required to hold a reference to the `KeyValueStore` while
/// operations are outstanding; releasing the last externally held reference to
/// a `KeyValueStore` object does not cancel outstanding operations.
class KeyValueStore {
 public:
  /// Keys and values are both represented as strings.
  using Key = std::string;
  using Value = absl::Cord;

  template <typename T>
  using PtrT = internal::IntrusivePtr<T>;

  using Ptr = PtrT<KeyValueStore>;

  struct ReadResult {
    enum class State {
      /// Indicates an unspecified value, used when a conditional read was
      /// requested and the condition was not satisfied.  The `value` member
      /// must be empty.
      kUnspecified,
      /// Indicates a missing value (not an error).  The `value` member must be
      /// empty.
      kMissing,
      /// Indicates a value is present.
      kValue
    };

    constexpr static State kUnspecified = State::kUnspecified;
    constexpr static State kMissing = State::kMissing;
    constexpr static State kValue = State::kValue;

    friend std::ostream& operator<<(std::ostream& os, State state);

    ReadResult() = default;

    /// Constructs a `ReadResult` with the value unspecified.
    ReadResult(TimestampedStorageGeneration stamp) : stamp(std::move(stamp)) {}

    ReadResult(State state, Value value, TimestampedStorageGeneration stamp)
        : state(state), value(std::move(value)), stamp(std::move(stamp)) {}

    /// Indicates the interpretation of `value`.
    State state = kUnspecified;

    /// Specifies the value if `state == kValue`.  Otherwise must be empty.
    Value value;

    /// Generation and timestamp associated with `value` and `state`.
    ///
    /// The `time` must be greater than or equal to the `staleness_bound`
    /// specified in the `ReadOptions` (or the time of the read request, if a
    /// `staleness_bound` in the future was specified).
    TimestampedStorageGeneration stamp;

    /// Returns `true` if the read was aborted because the conditions were not
    /// satisfied.
    bool aborted() const { return state == kUnspecified; }

    /// Returns `true` if the key was not found.
    bool not_found() const { return state == kMissing; }

    bool has_value() const { return state == kValue; }

    std::optional<Value> optional_value() const& {
      if (state == kValue) return value;
      return std::nullopt;
    }

    std::optional<Value> optional_value() && {
      if (state == kValue) return std::move(value);
      return std::nullopt;
    }

    friend bool operator==(const ReadResult& a, const ReadResult& b) {
      return a.state == b.state && a.value == b.value && a.stamp == b.stamp;
    }
    friend bool operator!=(const ReadResult& a, const ReadResult& b) {
      return !(a == b);
    }
    friend std::ostream& operator<<(std::ostream& os, const ReadResult& x);
  };

  // Note: This is not defined directly as a nested class in order to work
  // around Clang bug https://bugs.llvm.org/show_bug.cgi?id=36684.
  using ReadOptions = KeyValueStoreReadOptions;

  /// Attempts to read the specified key.
  ///
  /// \param key The key to read.
  /// \param options Specifies options for reading.
  /// \returns A Future that resolves when the read completes successfully or
  ///     with an error.
  virtual Future<ReadResult> Read(Key key, ReadOptions options = {});

  struct WriteOptions {
    // Note: While it would be nice to use default member initializers to be
    // more explicit about what the default values are, doing so would trigger
    // Clang bug https://bugs.llvm.org/show_bug.cgi?id=36684.

    /// The write is aborted if the existing generation associated with the
    /// stored `key` does not match `if_equal`.
    ///
    /// - The special value of `StorageGeneration::Unknown()` (the default)
    ///   disables this condition.
    ///
    /// - The special value of `StorageGeneration::NoValue()` specifies a
    ///   condition that the `key` does not have an existing value.
    StorageGeneration if_equal;
  };

  /// Performs an optionally-conditional write.
  ///
  /// Atomically updates or deletes the value stored for `key` subject to the
  /// conditions specified in `options`.
  ///
  /// \param key The key to write or delete.
  /// \param value The value to write, or `std::nullopt` to delete.
  /// \returns A Future that resolves to the generation corresponding to the new
  ///     value on success, or to `StorageGeneration::Unknown()` if the
  ///     conditions in `options` are not satisfied.
  virtual Future<TimestampedStorageGeneration> Write(Key key,
                                                     std::optional<Value> value,
                                                     WriteOptions options = {});

  /// Performs an optionally-conditional delete.
  ///
  /// Equivalent to calling `Write` with `value` equal to `std::nullopt`.
  Future<TimestampedStorageGeneration> Delete(Key key,
                                              WriteOptions options = {}) {
    return Write(key, std::nullopt, std::move(options));
  }

  /// Deletes all keys in the specified range.
  ///
  /// This operation is not guaranteed to be atomic with respect to other
  /// operations affecting keys in `range`.  If there are concurrent writes to
  /// keys in `range`, this operation may fail with an error or indicate success
  /// despite not having removed the newly-added keys.
  ///
  /// \returns A Future that becomes ready when the operation has completed
  ///     either successfully or with an error.
  virtual Future<void> DeleteRange(KeyRange range);

  /// Options for `List`.
  struct ListOptions {
    /// Only keys in this range are emitted.
    KeyRange range;
  };

  /// Implementation of `List` that driver implementations must define.
  virtual void ListImpl(const ListOptions& options,
                        AnyFlowReceiver<Status, Key> receiver);

  /// List keys in the KeyValueStore.
  ///
  /// The keys are emitted in arbitrary order.
  ///
  /// This simply forwards to `ListImpl`.
  AnyFlowSender<Status, Key> List(ListOptions options);

  using Spec = KeyValueStoreSpec;
  using OpenOptions = Spec::OpenOptions;
  using SpecRequestOptions = Spec::RequestOptions;
  using BoundSpec = Spec::Bound;

  /// Opens a `KeyValueStore` based on a JSON specification.
  ///
  /// \param context Specifies context resources that may be used.
  /// \param j JSON specification, passed by value because it is destructively
  ///     modified (and sub-objects may be retained) during parsing.
  /// \param options Options that may alter the interpretation of the JSON
  ///     specification.
  /// \threadsafety Thread safe.
  static Future<KeyValueStore::Ptr> Open(const Context& context,
                                         ::nlohmann::json j,
                                         const OpenOptions& options = {});

  /// Returns a Spec that can be used to re-open this KeyValueStore.
  ///
  /// Returns `absl::StatusCode::kUnimplemented` if a JSON representation is not
  /// supported.  (This behavior is provided by the default implementation.)
  ///
  /// For drivers that do support a JSON representation, this is defined
  /// automatically by `RegisteredKeyValueStore` in `registry.h`.
  ///
  /// \param context_builder Optional.  Specifies a parent context spec builder,
  ///     if this `Spec` is to be used in conjunction with a parent context.  If
  ///     specified, all required shared context resources are recorded in the
  ///     specified builder.  If not specified, required shared context
  ///     resources are recorded in the `Context::Spec` owned by the returned
  ///     `Spec`.
  virtual Result<Spec::Ptr> spec(
      const internal::ContextSpecBuilder& context_builder = {}) const;

  /// Returns a BoundSpec that can be used to re-open this KeyValueStore.
  ///
  /// Returns `absl::StatusCode::kUnimplemented` if a JSON representation is not
  /// supported.  (This behavior is provided by the default implementation.)
  ///
  /// For drivers that do support a JSON representation, this is defined
  /// automatically by `RegisteredKeyValueStore` in `registry.h`.
  virtual Result<Spec::BoundPtr> GetBoundSpec() const;

  /// Encodes relevant state as a cache key.
  ///
  /// Typically this should be called indirectly via
  /// `tensorstore::internal::EncodeCacheKey`.
  ///
  /// The default implementation simply encodes the pointer value `this`, and is
  /// used for KeyValueStore implementations that do not support a JSON
  /// representation or are incompatible with the cache key mechanism.
  ///
  /// For drivers that do support a JSON representation, this is defined
  /// automatically by `RegisteredKeyValueStore` in `registry.h`.
  virtual void EncodeCacheKey(std::string* out) const;

  /// For compatibility with `tensorstore::internal::EncodeCacheKey`.
  friend void EncodeCacheKeyAdl(std::string* out, const Ptr& ptr) {
    ptr->EncodeCacheKey(out);
  }

  /// Returns a human-readable description of a key for use in error messages.
  ///
  /// By default, returns `QuoteString(key)`.
  virtual std::string DescribeKey(absl::string_view key);

  virtual ~KeyValueStore();

 private:
  void DestroyLastReference();

  friend void intrusive_ptr_increment(KeyValueStore* store) {
    store->reference_count_.fetch_add(1, std::memory_order_relaxed);
  }

  friend void intrusive_ptr_decrement(KeyValueStore* store) {
    if (store->reference_count_.fetch_sub(1, std::memory_order_acq_rel) == 1) {
      store->DestroyLastReference();
    }
  }

  std::atomic<size_t> reference_count_{0};
};

/// Calls `List` and collects the results in an `std::vector`.
Future<std::vector<KeyValueStore::Key>> ListFuture(
    KeyValueStore* store, KeyValueStore::ListOptions options = {});

namespace internal {

/// For compatibility with `ContextBindingTraits`.  `KeyValueStore::Spec::Ptr`
/// is the context-unbound type corresponding to the context-bound type
/// `KeyValueStore::BoundSpec::Ptr`.
template <>
struct ContextBindingTraits<KeyValueStoreSpec::Ptr> {
  using Spec = KeyValueStoreSpec::Ptr;
  using Bound = KeyValueStoreSpec::BoundPtr;
  static Status Bind(const Spec* spec, Bound* bound, const Context& context) {
    if (!*spec) {
      *bound = Bound{};
    } else {
      TENSORSTORE_ASSIGN_OR_RETURN(*bound, (*spec)->Bind(context));
    }
    return Status();
  }
  static void Unbind(Spec* spec, const Bound* bound,
                     const ContextSpecBuilder& builder) {
    *spec = (*bound)->Unbind(builder);
  }
};
}  // namespace internal

}  // namespace tensorstore

#endif  // TENSORSTORE_KVSTORE_KEY_VALUE_H_
