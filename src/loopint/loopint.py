"""
LoopInt: a cyclic integer with range semantics [left; right).

This class behaves like an integer that wraps around within a fixed span.
Arithmetic operations (+, -, +=, -=) apply modular arithmetic over the interval
[left; right). Comparison, hashing, formatting and indexing behave like an `int`.

Examples:
    >>> x = LoopInt(0, right=5)
    >>> int(x)
    0
    >>> x += 7
    >>> int(x)
    2
    >>> x == 2
    True
"""

from __future__ import annotations

import operator
from copy import copy
from typing import Self, SupportsIndex, SupportsInt, override


class LoopInt(SupportsInt, SupportsIndex):
    """A cyclic integer constrained to the interval [left; right).

    The internal value wraps modulo `span = right - left`. All public integer-like
    behaviors (int(), index(), hashing, equality, formatting) reflect the
    "visible" integer value: `left + (internal_value % span)`.
    """

    @staticmethod
    def __check_int_like(obj: SupportsIndex) -> int:
        """Convert an index-like object into a real integer using operator.index()."""
        return operator.index(obj)

    def __init__(self, current_number: SupportsIndex, /, right: SupportsIndex, *, left: SupportsIndex = 0) -> None:
        """Initialize a LoopInt.

        Args:
            current_number: Any integer-like object specifying the starting value.
            right: The exclusive upper bound of the interval.
            left: The inclusive lower bound of the interval.

        Raises:
            ValueError: If `right <= left`, producing a non-positive span.
        """
        self.__offset = LoopInt.__check_int_like(left)
        self.__span = LoopInt.__check_int_like(right) - self.__offset
        self.__current_number = LoopInt.__check_int_like(current_number) - self.__offset
        if self.__span <= 0:
            raise ValueError("Left border must be less than right border")
        self.__current_number %= self.__span

    @property
    def __with_offset(self) -> int:
        """Internal helper returning the fully normalized visible value."""
        return self.__current_number + self.__offset

    @override
    def __int__(self) -> int:
        """Return the visible integer value of this LoopInt."""
        return self.__with_offset

    @override
    def __hash__(self) -> int:
        """Hash consistent with the visible integer value."""
        return hash(int(self))

    def to_string(self) -> str:
        """Return the value cast to string (same as str(int(self)))."""
        return str(int(self))

    @override
    def __index__(self) -> int:
        """Return the integer value for sequence indexing operations."""
        return int(self)

    @override
    def __eq__(self, other: object, /) -> bool:
        """Equality is defined by comparing the visible integer value.

        LoopInt compares equal to:
        - another LoopInt with the same visible value,
        - an int with the same value,
        - any object where `int(self) == other` is True.
        """
        return int(self) == other

    @property
    def value(self) -> int:
        """The visible integer value of this LoopInt."""
        return int(self)

    @property
    def left(self) -> int:
        """The inclusive lower bound of the interval."""
        return self.__offset

    @property
    def right(self) -> int:
        """The exclusive upper bound of the interval."""
        return self.__span + self.__offset

    @property
    def span(self) -> int:
        """The size of the interval (right - left)."""
        return self.__span

    @override
    def __repr__(self) -> str:
        """Return a detailed representation including bounds and current value."""
        return f"{type(self).__name__}(current_number={int(self)}, left_border={self.left}, right_border={self.right})"

    @override
    def __format__(self, format_spec: str, /) -> str:
        """Format using the visible integer value."""
        return format(int(self), format_spec)

    def __copy__(self) -> LoopInt:
        """Return a shallow copy preserving bounds and current value."""
        return LoopInt(int(self), left=self.left, right=self.right)

    def __neg__(self) -> LoopInt:
        """Return the modular negation of this LoopInt.

        The operation computes the value `-(int(self))` under the same interval
        semantics [left; right). The resulting value is normalized via modular
        arithmetic on the interval span.

        Example:
            x = LoopInt(1, right=5)   # visible value = 1
            y = -x                    # visible value = -1 mod 5 == 4
            assert int(y) == 4

        Returns:
            LoopInt: A new LoopInt instance with the negated modular value.
        """
        return LoopInt(-int(self), left=self.left, right=self.right)

    def __iadd__(self, other: SupportsIndex, /) -> Self:
        """In-place addition with modular wrap-around.

        Raises:
            TypeError: If `other` is a LoopInt (not allowed).
        """
        if isinstance(other, LoopInt):
            raise TypeError("LoopInt cannot be added to LoopInt; only integer-like values allowed")

        other_number = LoopInt.__check_int_like(other)

        self.__current_number = (self.__current_number + other_number) % self.__span

        return self

    def __isub__(self, other: SupportsIndex, /) -> Self:
        """In-place subtraction with modular wrap-around.

        Raises:
            TypeError: If `other` is a LoopInt (not allowed).
        """
        if isinstance(other, LoopInt):
            raise TypeError("LoopInt cannot be added to LoopInt; only integer-like values allowed")

        other_number = LoopInt.__check_int_like(other)

        self.__current_number = (self.__current_number - other_number) % self.__span

        return self

    def __add__(self, other: SupportsIndex, /) -> LoopInt:
        """Return a new LoopInt equal to self + other (non-mutating)."""
        clone = copy(self)
        clone += other
        return clone

    def __radd__(self, other: SupportsIndex, /) -> LoopInt:
        """Support int + LoopInt by delegating to the same interval as self."""
        return self + other

    def __sub__(self, other: SupportsIndex) -> LoopInt:
        """Return a new LoopInt equal to self - other (non-mutating)."""
        clone = copy(self)
        clone -= other
        return clone

    def __rsub__(self, other: SupportsIndex, /) -> LoopInt:
        """Support int - LoopInt by delegating to the same interval as self."""
        return -(self - other)
