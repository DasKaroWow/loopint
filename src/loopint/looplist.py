"""
LoopList — a cyclic list implementation with modulo-wrapped indexing.

This module provides the `LoopList` class, a drop-in replacement for Python's
built-in `list` that extends index semantics: all integer indices are wrapped
modulo the list length. This makes it possible to access elements in a circular
fashion, simplifying algorithms that rely on cyclical data structures.

Behavior summary:
- Integer indexing is wrapped using `index % len(self)`.
- Slice operations behave like a normal list and return a new LoopList.
- Methods such as pop(), insert(), __setitem__(), and __delitem__() all use
  cyclic indexing.
- A ZeroDivisionError (e.g., modulo on an empty list) triggers automatic
  fallback to the corresponding built-in list method, preserving Python’s
  standard semantics for empty lists.

Example:
    >>> from looplist import LoopList
    >>> ll = LoopList([10, 20, 30])

    # Cyclic positive indexing
    >>> ll[5]
    30  # because 5 % 3 == 2

    # Cyclic negative indexing
    >>> ll[-4]
    30  # because -4 % 3 == 2

    # Cyclic assignment
    >>> ll[7] = 99
    >>> ll
    [10, 99, 30]

The class is fully type-annotated and compatible with Python's static type
checkers (Pyright, Mypy), including overloads and Self types.
"""


from __future__ import annotations

import functools
import operator
from collections.abc import Callable, Iterable
from typing import Self, SupportsIndex, overload, override


class LoopList[T](list[T]):
    """
    A cyclic list implementation that wraps integer indices modulo the list length.

    LoopList behaves like a normal list, except all index-based operations
    (getitem, setitem, pop, insert, delitem) accept any integer index and
    transparently wrap it around the list length. Slice operations behave
    identically to the built-in list.

    The class also provides a decorator that catches ZeroDivisionError raised
    when modulo operations are applied on an empty list, falling back to the
    original list behavior.
    """

    @staticmethod
    def __list_zerodivision_fallback[**P, R](func: Callable[P, R]) -> Callable[P, R]:
        """
        Decorator that intercepts ZeroDivisionError caused by modulo operations
        (typically when operating on an empty LoopList) and falls back to the
        corresponding method from the built-in list.

        This ensures that empty-list behavior stays consistent with Python's
        standard list API while still allowing modulo-wrapped indexing for
        non-empty lists.
        """

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except ZeroDivisionError:
                base_method: Callable[P, R] = getattr(list, func.__name__)
                return base_method(*args, **kwargs)

        return wrapper

    @staticmethod
    def __check_int_like(obj: SupportsIndex) -> int:
        """
        Convert a SupportsIndex-compatible object into a real `int` using
        `operator.index()`.

        Raises:
            TypeError: If the object does not implement `__index__()`.
        """

        return operator.index(obj)

    def __init__(self, iterable: Iterable[T] = (), /) -> None:
        """
        Initialize the LoopList with elements from the given iterable.

        Args:
            iterable: Optional iterable providing the initial elements.
        """

        super().__init__(iterable)

    @__list_zerodivision_fallback
    @override
    def pop(self, index: SupportsIndex = -1, /) -> T:
        """
        Remove and return an item at the given cyclic index.

        The index is wrapped modulo the list length. If the list is empty,
        falls back to `list.pop()` behavior.

        Args:
            index: Index of the element to remove (cyclic).

        Returns:
            The removed element.
        """

        return super().pop(LoopList.__check_int_like(index) % len(self))

    @__list_zerodivision_fallback
    @override
    def insert(self, index: SupportsIndex, object: T, /) -> None:
        """
        Insert an element at a cyclic position.

        The insertion index is wrapped modulo the list length. If the list
        is empty, falls back to `list.insert()` behavior.

        Args:
            index: Position at which to insert (cyclic).
            object: Element to insert.
        """

        super().insert(LoopList.__check_int_like(index) % len(self), object)

    @overload
    def __getitem__(self, s: SupportsIndex, /) -> T: ...

    @overload
    def __getitem__(self, s: slice, /) -> Self: ...

    @__list_zerodivision_fallback
    @override
    def __getitem__(self, key: SupportsIndex | slice, /) -> T | Self:
        """
        Retrieve an element or a slice.

        - For integer-like indices, returns the element at `index % len(self)`.
        - For slices, returns a new LoopList containing the slice.

        Args:
            key: Index or slice.

        Returns:
            The element or a new LoopList with sliced contents.
        """

        if isinstance(key, slice):
            return type(self)(super().__getitem__(key))

        index = LoopList.__check_int_like(key)
        return super().__getitem__(index % len(self))

    @overload
    def __setitem__(self, key: SupportsIndex, value: T, /) -> None: ...
    @overload
    def __setitem__(self, key: slice, value: Iterable[T], /) -> None: ...

    @__list_zerodivision_fallback
    @override
    def __setitem__(self, key: SupportsIndex | slice, value: T | Iterable[T]) -> None:
        """
        Assign to a cyclic index or a slice.

        - For integer-like indices, assigns to `index % len(self)`.
        - For slices, delegates directly to list.__setitem__.

        Args:
            key: Index or slice.
            value: Single element or iterable, depending on the key.
        """

        if isinstance(key, slice):
            super().__setitem__(key, value)  # pyright: ignore[reportArgumentType, reportCallIssue]
            return

        index = LoopList.__check_int_like(key)
        super().__setitem__(index % len(self), value)  # pyright: ignore[reportArgumentType, reportCallIssue]

    @__list_zerodivision_fallback
    @override
    def __delitem__(self, key: SupportsIndex | slice, /) -> None:
        """
        Delete an item or a slice.

        - For integer-like indices, deletes the element at `index % len(self)`.
        - For slices, delegates directly to list.__delitem__.

        Args:
            key: Index or slice to delete.
        """

        if isinstance(key, slice):
            super().__delitem__(key)
            return

        index = LoopList.__check_int_like(key)
        super().__delitem__(index % len(self))
