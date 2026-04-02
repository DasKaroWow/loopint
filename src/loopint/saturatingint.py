from __future__ import annotations

from typing import SupportsIndex, override, Self, SupportsInt
import operator

class SaturatingInt(SupportsIndex, SupportsInt):
    def __init__(self, value: SupportsIndex, /, right: SupportsIndex, *, left: SupportsIndex = 0) -> None:
        value = operator.index(value)
        left = operator.index(left)
        right = operator.index(right)
        if right - left <= 0:
            raise ValueError("Left border must be less than right border")

        value = min(max(value, left), right - 1)

        self._value = value
        self._left = left
        self._right = right

    @property
    def value(self) -> int:
        return self._value

    @property
    def left(self) -> int:
        return self._left

    @property
    def right(self) -> int:
        return self._right

    @override
    def __index__(self) -> int:
        return self.value

    @override
    def __int__(self) -> int:
        return self.value

    def __neg__(self) -> Self:
        value = operator.index(self)
        return type(self)(-value, left=self._left, right=self._right)

    def __add__(self, other: SupportsIndex, /) -> Self:
        try:
            other = operator.index(other)
        except TypeError:
            return NotImplemented
        value = operator.index(self)
        return type(self)(value + other, left=self._left, right=self._right)

    def __radd__(self, other: SupportsIndex, /) -> Self:
        return self + other

    def __sub__(self, other: SupportsIndex, /) -> Self:
        try:
            other = operator.index(other)
        except TypeError:
            return NotImplemented
        value = operator.index(self)
        return type(self)(value - other, left=self._left, right=self._right)

    def __rsub__(self, other: SupportsIndex, /) -> Self:
        return -(self - other)

    def __mul__(self, other: SupportsIndex, /) -> Self:
        try:
            other = operator.index(other)
        except TypeError:
            return NotImplemented
        value = operator.index(self)
        return type(self)(value * other, left=self._left, right=self._right)

    def __rmul__(self, other: SupportsIndex, /) -> Self:
        return self * other
