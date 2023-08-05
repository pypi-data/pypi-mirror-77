# orm/state.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Defines instrumentation of instances.

This module is usually not directly visible to user applications, but
defines a large part of the ORM's interactivity.

"""

import weakref

from . import base
from . import exc as orm_exc
from . import interfaces
from .base import ATTR_WAS_SET
from .base import INIT_OK
from .base import NEVER_SET
from .base import NO_VALUE
from .base import PASSIVE_NO_INITIALIZE
from .base import PASSIVE_NO_RESULT
from .base import PASSIVE_OFF
from .base import SQL_OK
from .path_registry import PathRegistry
from .. import exc as sa_exc
from .. import inspection
from .. import util


@inspection._self_inspects
class InstanceState(interfaces.InspectionAttrInfo):
    """tracks state information at the instance level.

    The :class:`.InstanceState` is a key object used by the
    SQLAlchemy ORM in order to track the state of an object;
    it is created the moment an object is instantiated, typically
    as a result of :term:`instrumentation` which SQLAlchemy applies
    to the ``__init__()`` method of the class.

    :class:`.InstanceState` is also a semi-public object,
    available for runtime inspection as to the state of a
    mapped instance, including information such as its current
    status within a particular :class:`.Session` and details
    about data on individual attributes.  The public API
    in order to acquire a :class:`.InstanceState` object
    is to use the :func:`_sa.inspect` system::

        >>> from sqlalchemy import inspect
        >>> insp = inspect(some_mapped_object)

    .. seealso::

        :ref:`core_inspection_toplevel`

    """

    session_id = None
    key = None
    runid = None
    load_options = util.EMPTY_SET
    load_path = PathRegistry.root
    insert_order = None
    _strong_obj = None
    modified = False
    expired = False
    _deleted = False
    _load_pending = False
    _orphaned_outside_of_session = False
    is_instance = True
    identity_token = None
    _last_known_values = ()

    callables = ()
    """A namespace where a per-state loader callable can be associated.

    In SQLAlchemy 1.0, this is only used for lazy loaders / deferred
    loaders that were set up via query option.

    Previously, callables was used also to indicate expired attributes
    by storing a link to the InstanceState itself in this dictionary.
    This role is now handled by the expired_attributes set.

    """

    def __init__(self, obj, manager):
        self.class_ = obj.__class__
        self.manager = manager
        self.obj = weakref.ref(obj, self._cleanup)
        self.committed_state = {}
        self.expired_attributes = set()

    expired_attributes = None
    """The set of keys which are 'expired' to be loaded by
       the manager's deferred scalar loader, assuming no pending
       changes.

       see also the ``unmodified`` collection which is intersected
       against this set when a refresh operation occurs."""

    @util.memoized_property
    def attrs(self):
        """Return a namespace representing each attribute on
        the mapped object, including its current value
        and history.

        The returned object is an instance of :class:`.AttributeState`.
        This object allows inspection of the current data
        within an attribute as well as attribute history
        since the last flush.

        """
        return util.ImmutableProperties(
            dict((key, AttributeState(self, key)) for key in self.manager)
        )

    @property
    def transient(self):
        """Return ``True`` if the object is :term:`transient`.

        .. seealso::

            :ref:`session_object_states`

        """
        return self.key is None and not self._attached

    @property
    def pending(self):
        """Return ``True`` if the object is :term:`pending`.


        .. seealso::

            :ref:`session_object_states`

        """
        return self.key is None and self._attached

    @property
    def deleted(self):
        """Return ``True`` if the object is :term:`deleted`.

        An object that is in the deleted state is guaranteed to
        not be within the :attr:`.Session.identity_map` of its parent
        :class:`.Session`; however if the session's transaction is rolled
        back, the object will be restored to the persistent state and
        the identity map.

        .. note::

            The :attr:`.InstanceState.deleted` attribute refers to a specific
            state of the object that occurs between the "persistent" and
            "detached" states; once the object is :term:`detached`, the
            :attr:`.InstanceState.deleted` attribute **no longer returns
            True**; in order to detect that a state was deleted, regardless
            of whether or not the object is associated with a
            :class:`.Session`, use the :attr:`.InstanceState.was_deleted`
            accessor.

        .. versionadded: 1.1

        .. seealso::

            :ref:`session_object_states`

        """
        return self.key is not None and self._attached and self._deleted

    @property
    def was_deleted(self):
        """Return True if this object is or was previously in the
        "deleted" state and has not been reverted to persistent.

        This flag returns True once the object was deleted in flush.
        When the object is expunged from the session either explicitly
        or via transaction commit and enters the "detached" state,
        this flag will continue to report True.

        .. versionadded:: 1.1 - added a local method form of
           :func:`.orm.util.was_deleted`.

        .. seealso::

            :attr:`.InstanceState.deleted` - refers to the "deleted" state

            :func:`.orm.util.was_deleted` - standalone function

            :ref:`session_object_states`

        """
        return self._deleted

    @property
    def persistent(self):
        """Return ``True`` if the object is :term:`persistent`.

        An object that is in the persistent state is guaranteed to
        be within the :attr:`.Session.identity_map` of its parent
        :class:`.Session`.

        .. versionchanged:: 1.1 The :attr:`.InstanceState.persistent`
           accessor no longer returns True for an object that was
           "deleted" within a flush; use the :attr:`.InstanceState.deleted`
           accessor to detect this state.   This allows the "persistent"
           state to guarantee membership in the identity map.

        .. seealso::

            :ref:`session_object_states`

            """
        return self.key is not None and self._attached and not self._deleted

    @property
    def detached(self):
        """Return ``True`` if the object is :term:`detached`.

        .. seealso::

            :ref:`session_object_states`

        """
        return self.key is not None and not self._attached

    @property
    @util.dependencies("sqlalchemy.orm.session")
    def _attached(self, sessionlib):
        return (
            self.session_id is not None
            and self.session_id in sessionlib._sessions
        )

    def _track_last_known_value(self, key):
        """Track the last known value of a particular key after expiration
        operations.

        .. versionadded:: 1.3

        """

        if key not in self._last_known_values:
            self._last_known_values = dict(self._last_known_values)
            self._last_known_values[key] = NO_VALUE

    @property
    @util.dependencies("sqlalchemy.orm.session")
    def session(self, sessionlib):
        """Return the owning :class:`.Session` for this instance,
        or ``None`` if none available.

        Note that the result here can in some cases be *different*
        from that of ``obj in session``; an object that's been deleted
        will report as not ``in session``, however if the transaction is
        still in progress, this attribute will still refer to that session.
        Only when the transaction is completed does the object become
        fully detached under normal circumstances.

        """
        return sessionlib._state_session(self)

    @property
    def object(self):
        """Return the mapped object represented by this
        :class:`.InstanceState`."""
        return self.obj()

    @property
    def identity(self):
        """Return the mapped identity of the mapped object.
        This is the primary key identity as persisted by the ORM
        which can always be passed directly to
        :meth:`_query.Query.get`.

        Returns ``None`` if the object has no primary key identity.

        .. note::
            An object which is :term:`transient` or :term:`pending`
            does **not** have a mapped identity until it is flushed,
            even if its attributes include primary key values.

        """
        if self.key is None:
            return None
        else:
            return self.key[1]

    @property
    def identity_key(self):
        """Return the identity key for the mapped object.

        This is the key used to locate the object within
        the :attr:`.Session.identity_map` mapping.   It contains
        the identity as returned by :attr:`.identity` within it.


        """
        # TODO: just change .key to .identity_key across
        # the board ?  probably
        return self.key

    @util.memoized_property
    def parents(self):
        return {}

    @util.memoized_property
    def _pending_mutations(self):
        return {}

    @util.memoized_property
    def mapper(self):
        """Return the :class:`_orm.Mapper` used for this mapped object."""
        return self.manager.mapper

    @property
    def has_identity(self):
        """Return ``True`` if this object has an identity key.

        This should always have the same value as the
        expression ``state.persistent`` or ``state.detached``.

        """
        return bool(self.key)

    @classmethod
    def _detach_states(self, states, session, to_transient=False):
        persistent_to_detached = (
            session.dispatch.persistent_to_detached or None
        )
        deleted_to_detached = session.dispatch.deleted_to_detached or None
        pending_to_transient = session.dispatch.pending_to_transient or None
        persistent_to_transient = (
            session.dispatch.persistent_to_transient or None
        )

        for state in states:
            deleted = state._deleted
            pending = state.key is None
            persistent = not pending and not deleted

            state.session_id = None

            if to_transient and state.key:
                del state.key
            if persistent:
                if to_transient:
                    if persistent_to_transient is not None:
                        persistent_to_transient(session, state)
                elif persistent_to_detached is not None:
                    persistent_to_detached(session, state)
            elif deleted and deleted_to_detached is not None:
                deleted_to_detached(session, state)
            elif pending and pending_to_transient is not None:
                pending_to_transient(session, state)

            state._strong_obj = None

    def _detach(self, session=None):
        if session:
            InstanceState._detach_states([self], session)
        else:
            self.session_id = self._strong_obj = None

    def _dispose(self):
        self._detach()
        del self.obj

    def _cleanup(self, ref):
        """Weakref callback cleanup.

        This callable cleans out the state when it is being garbage
        collected.

        this _cleanup **assumes** that there are no strong refs to us!
        Will not work otherwise!

        """

        # Python builtins become undefined during interpreter shutdown.
        # Guard against exceptions during this phase, as the method cannot
        # proceed in any case if builtins have been undefined.
        if dict is None:
            return

        instance_dict = self._instance_dict()
        if instance_dict is not None:
            instance_dict._fast_discard(self)
            del self._instance_dict

            # we can't possibly be in instance_dict._modified
            # b.c. this is weakref cleanup only, that set
            # is strong referencing!
            # assert self not in instance_dict._modified

        self.session_id = self._strong_obj = None
        del self.obj

    def obj(self):
        return None

    @property
    def dict(self):
        """Return the instance dict used by the object.

        Under normal circumstances, this is always synonymous
        with the ``__dict__`` attribute of the mapped object,
        unless an alternative instrumentation system has been
        configured.

        In the case that the actual object has been garbage
        collected, this accessor returns a blank dictionary.

        """
        o = self.obj()
        if o is not None:
            return base.instance_dict(o)
        else:
            return {}

    def _initialize_instance(*mixed, **kwargs):
        self, instance, args = mixed[0], mixed[1], mixed[2:]  # noqa
        manager = self.manager

        manager.dispatch.init(self, args, kwargs)

        try:
            return manager.original_init(*mixed[1:], **kwargs)
        except:
            with util.safe_reraise():
                manager.dispatch.init_failure(self, args, kwargs)

    def get_history(self, key, passive):
        return self.manager[key].impl.get_history(self, self.dict, passive)

    def get_impl(self, key):
        return self.manager[key].impl

    def _get_pending_mutation(self, key):
        if key not in self._pending_mutations:
            self._pending_mutations[key] = PendingCollection()
        return self._pending_mutations[key]

    def __getstate__(self):
        state_dict = {"instance": self.obj()}
        state_dict.update(
            (k, self.__dict__[k])
            for k in (
                "committed_state",
                "_pending_mutations",
                "modified",
                "expired",
                "callables",
                "key",
                "parents",
                "load_options",
                "class_",
                "expired_attributes",
                "info",
            )
            if k in self.__dict__
        )
        if self.load_path:
            state_dict["load_path"] = self.load_path.serialize()

        state_dict["manager"] = self.manager._serialize(self, state_dict)

        return state_dict

    def __setstate__(self, state_dict):
        inst = state_dict["instance"]
        if inst is not None:
            self.obj = weakref.ref(inst, self._cleanup)
            self.class_ = inst.__class__
        else:
            # None being possible here generally new as of 0.7.4
            # due to storage of state in "parents".  "class_"
            # also new.
            self.obj = None
            self.class_ = state_dict["class_"]

        self.committed_state = state_dict.get("committed_state", {})
        self._pending_mutations = state_dict.get("_pending_mutations", {})
        self.parents = state_dict.get("parents", {})
        self.modified = state_dict.get("modified", False)
        self.expired = state_dict.get("expired", False)
        if "info" in state_dict:
            self.info.update(state_dict["info"])
        if "callables" in state_dict:
            self.callables = state_dict["callables"]

            try:
                self.expired_attributes = state_dict["expired_attributes"]
            except KeyError:
                self.expired_attributes = set()
                # 0.9 and earlier compat
                for k in list(self.callables):
                    if self.callables[k] is self:
                        self.expired_attributes.add(k)
                        del self.callables[k]
        else:
            if "expired_attributes" in state_dict:
                self.expired_attributes = state_dict["expired_attributes"]
            else:
                self.expired_attributes = set()

        self.__dict__.update(
            [
                (k, state_dict[k])
                for k in ("key", "load_options")
                if k in state_dict
            ]
        )
        if self.key:
            try:
                self.identity_token = self.key[2]
            except IndexError:
                # 1.1 and earlier compat before identity_token
                assert len(self.key) == 2
                self.key = self.key + (None,)
                self.identity_token = None

        if "load_path" in state_dict:
            self.load_path = PathRegistry.deserialize(state_dict["load_path"])

        state_dict["manager"](self, inst, state_dict)

    def _reset(self, dict_, key):
        """Remove the given attribute and any
           callables associated with it."""

        old = dict_.pop(key, None)
        if old is not None and self.manager[key].impl.collection:
            self.manager[key].impl._invalidate_collection(old)
        self.expired_attributes.discard(key)
        if self.callables:
            self.callables.pop(key, None)

    def _copy_callables(self, from_):
        if "callables" in from_.__dict__:
            self.callables = dict(from_.callables)

    @classmethod
    def _instance_level_callable_processor(cls, manager, fn, key):
        impl = manager[key].impl
        if impl.collection:

            def _set_callable(state, dict_, row):
                if "callables" not in state.__dict__:
                    state.callables = {}
                old = dict_.pop(key, None)
                if old is not None:
                    impl._invalidate_collection(old)
                state.callables[key] = fn

        else:

            def _set_callable(state, dict_, row):
                if "callables" not in state.__dict__:
                    state.callables = {}
                state.callables[key] = fn

        return _set_callable

    def _expire(self, dict_, modified_set):
        self.expired = True

        if self.modified:
            modified_set.discard(self)
            self.committed_state.clear()
            self.modified = False

        self._strong_obj = None

        if "_pending_mutations" in self.__dict__:
            del self.__dict__["_pending_mutations"]

        if "parents" in self.__dict__:
            del self.__dict__["parents"]

        self.expired_attributes.update(
            [
                impl.key
                for impl in self.manager._scalar_loader_impls
                if impl.expire_missing or impl.key in dict_
            ]
        )

        if self.callables:
            for k in self.expired_attributes.intersection(self.callables):
                del self.callables[k]

        for k in self.manager._collection_impl_keys.intersection(dict_):
            collection = dict_.pop(k)
            collection._sa_adapter.invalidated = True

        if self._last_known_values:
            self._last_known_values.update(
                (k, dict_[k]) for k in self._last_known_values if k in dict_
            )

        for key in self.manager._all_key_set.intersection(dict_):
            del dict_[key]

        self.manager.dispatch.expire(self, None)

    def _expire_attributes(self, dict_, attribute_names, no_loader=False):
        pending = self.__dict__.get("_pending_mutations", None)

        callables = self.callables

        for key in attribute_names:
            impl = self.manager[key].impl
            if impl.accepts_scalar_loader:
                if no_loader and (impl.callable_ or key in callables):
                    continue

                self.expired_attributes.add(key)
                if callables and key in callables:
                    del callables[key]
            old = dict_.pop(key, NO_VALUE)
            if impl.collection and old is not NO_VALUE:
                impl._invalidate_collection(old)

            if (
                self._last_known_values
                and key in self._last_known_values
                and old is not NO_VALUE
            ):
                self._last_known_values[key] = old

            self.committed_state.pop(key, None)
            if pending:
                pending.pop(key, None)

        self.manager.dispatch.expire(self, attribute_names)

    def _load_expired(self, state, passive):
        """__call__ allows the InstanceState to act as a deferred
        callable for loading expired attributes, which is also
        serializable (picklable).

        """

        if not passive & SQL_OK:
            return PASSIVE_NO_RESULT

        toload = self.expired_attributes.intersection(self.unmodified)

        self.manager.deferred_scalar_loader(self, toload)

        # if the loader failed, or this
        # instance state didn't have an identity,
        # the attributes still might be in the callables
        # dict.  ensure they are removed.
        self.expired_attributes.clear()

        return ATTR_WAS_SET

    @property
    def unmodified(self):
        """Return the set of keys which have no uncommitted changes"""

        return set(self.manager).difference(self.committed_state)

    def unmodified_intersection(self, keys):
        """Return self.unmodified.intersection(keys)."""

        return (
            set(keys)
            .intersection(self.manager)
            .difference(self.committed_state)
        )

    @property
    def unloaded(self):
        """Return the set of keys which do not have a loaded value.

        This includes expired attributes and any other attribute that
        was never populated or modified.

        """
        return (
            set(self.manager)
            .difference(self.committed_state)
            .difference(self.dict)
        )

    @property
    def unloaded_expirable(self):
        """Return the set of keys which do not have a loaded value.

        This includes expired attributes and any other attribute that
        was never populated or modified.

        """
        return self.unloaded.intersection(
            attr
            for attr in self.manager
            if self.manager[attr].impl.expire_missing
        )

    @property
    def _unloaded_non_object(self):
        return self.unloaded.intersection(
            attr
            for attr in self.manager
            if self.manager[attr].impl.accepts_scalar_loader
        )

    def _instance_dict(self):
        return None

    def _modified_event(
        self, dict_, attr, previous, collection=False, is_userland=False
    ):
        if attr:
            if not attr.send_modified_events:
                return
            if is_userland and attr.key not in dict_:
                raise sa_exc.InvalidRequestError(
                    "Can't flag attribute '%s' modified; it's not present in "
                    "the object state" % attr.key
                )
            if attr.key not in self.committed_state or is_userland:
                if collection:
                    if previous is NEVER_SET:
                        if attr.key in dict_:
                            previous = dict_[attr.key]

                    if previous not in (None, NO_VALUE, NEVER_SET):
                        previous = attr.copy(previous)
                self.committed_state[attr.key] = previous

            if attr.key in self._last_known_values:
                self._last_known_values[attr.key] = NO_VALUE

        # assert self._strong_obj is None or self.modified

        if (self.session_id and self._strong_obj is None) or not self.modified:
            self.modified = True
            instance_dict = self._instance_dict()
            if instance_dict:
                instance_dict._modified.add(self)

            # only create _strong_obj link if attached
            # to a session

            inst = self.obj()
            if self.session_id:
                self._strong_obj = inst

            if inst is None and attr:
                raise orm_exc.ObjectDereferencedError(
                    "Can't emit change event for attribute '%s' - "
                    "parent object of type %s has been garbage "
                    "collected."
                    % (self.manager[attr.key], base.state_class_str(self))
                )

    def _commit(self, dict_, keys):
        """Commit attributes.

        This is used by a partial-attribute load operation to mark committed
        those attributes which were refreshed from the database.

        Attributes marked as "expired" can potentially remain "expired" after
        this step if a value was not populated in state.dict.

        """
        for key in keys:
            self.committed_state.pop(key, None)

        self.expired = False

        self.expired_attributes.difference_update(
            set(keys).intersection(dict_)
        )

        # the per-keys commit removes object-level callables,
        # while that of commit_all does not.  it's not clear
        # if this behavior has a clear rationale, however tests do
        # ensure this is what it does.
        if self.callables:
            for key in (
                set(self.callables).intersection(keys).intersection(dict_)
            ):
                del self.callables[key]

    def _commit_all(self, dict_, instance_dict=None):
        """commit all attributes unconditionally.

        This is used after a flush() or a full load/refresh
        to remove all pending state from the instance.

         - all attributes are marked as "committed"
         - the "strong dirty reference" is removed
         - the "modified" flag is set to False
         - any "expired" markers for scalar attributes loaded are removed.
         - lazy load callables for objects / collections *stay*

        Attributes marked as "expired" can potentially remain
        "expired" after this step if a value was not populated in state.dict.

        """
        self._commit_all_states([(self, dict_)], instance_dict)

    @classmethod
    def _commit_all_states(self, iter_, instance_dict=None):
        """Mass / highly inlined version of commit_all()."""

        for state, dict_ in iter_:
            state_dict = state.__dict__

            state.committed_state.clear()

            if "_pending_mutations" in state_dict:
                del state_dict["_pending_mutations"]

            state.expired_attributes.difference_update(dict_)

            if instance_dict and state.modified:
                instance_dict._modified.discard(state)

            state.modified = state.expired = False
            state._strong_obj = None


class AttributeState(object):
    """Provide an inspection interface corresponding
    to a particular attribute on a particular mapped object.

    The :class:`.AttributeState` object is accessed
    via the :attr:`.InstanceState.attrs` collection
    of a particular :class:`.InstanceState`::

        from sqlalchemy import inspect

        insp = inspect(some_mapped_object)
        attr_state = insp.attrs.some_attribute

    """

    def __init__(self, state, key):
        self.state = state
        self.key = key

    @property
    def loaded_value(self):
        """The current value of this attribute as loaded from the database.

        If the value has not been loaded, or is otherwise not present
        in the object's dictionary, returns NO_VALUE.

        """
        return self.state.dict.get(self.key, NO_VALUE)

    @property
    def value(self):
        """Return the value of this attribute.

        This operation is equivalent to accessing the object's
        attribute directly or via ``getattr()``, and will fire
        off any pending loader callables if needed.

        """
        return self.state.manager[self.key].__get__(
            self.state.obj(), self.state.class_
        )

    @property
    def history(self):
        """Return the current **pre-flush** change history for
        this attribute, via the :class:`.History` interface.

        This method will **not** emit loader callables if the value of the
        attribute is unloaded.

        .. note::

            The attribute history system tracks changes on a **per flush
            basis**. Each time the :class:`.Session` is flushed, the history
            of each attribute is reset to empty.   The :class:`.Session` by
            default autoflushes each time a :class:`_query.Query` is invoked.
            For
            options on how to control this, see :ref:`session_flushing`.


        .. seealso::

            :meth:`.AttributeState.load_history` - retrieve history
            using loader callables if the value is not locally present.

            :func:`.attributes.get_history` - underlying function

        """
        return self.state.get_history(self.key, PASSIVE_NO_INITIALIZE)

    def load_history(self):
        """Return the current **pre-flush** change history for
        this attribute, via the :class:`.History` interface.

        This method **will** emit loader callables if the value of the
        attribute is unloaded.

        .. note::

            The attribute history system tracks changes on a **per flush
            basis**. Each time the :class:`.Session` is flushed, the history
            of each attribute is reset to empty.   The :class:`.Session` by
            default autoflushes each time a :class:`_query.Query` is invoked.
            For
            options on how to control this, see :ref:`session_flushing`.

        .. seealso::

            :attr:`.AttributeState.history`

            :func:`.attributes.get_history` - underlying function

        .. versionadded:: 0.9.0

        """
        return self.state.get_history(self.key, PASSIVE_OFF ^ INIT_OK)


class PendingCollection(object):
    """A writable placeholder for an unloaded collection.

    Stores items appended to and removed from a collection that has not yet
    been loaded. When the collection is loaded, the changes stored in
    PendingCollection are applied to it to produce the final result.

    """

    def __init__(self):
        self.deleted_items = util.IdentitySet()
        self.added_items = util.OrderedIdentitySet()

    def append(self, value):
        if value in self.deleted_items:
            self.deleted_items.remove(value)
        else:
            self.added_items.add(value)

    def remove(self, value):
        if value in self.added_items:
            self.added_items.remove(value)
        else:
            self.deleted_items.add(value)
