# pyright: basic

from enum import Enum
from typing import Self, Any, override
from dataclasses import dataclass
from collections.abc import Sequence, Hashable

@dataclass
class ElementSettings:
    name: Hashable
    aliases: Sequence[Hashable] | None = None
    meta: Any = None

class EvenBetterEnum(Enum):
    raise NotImplemented
    _value_: Hashable
    __aliases: frozenset[Hashable] = frozenset()
    __meta: Any = None

    def __new__(cls, settings: ElementSettings, /) -> Self:
        obj = object.__new__(cls)
        obj._value_ = settings.name

        obj.__aliases = frozenset(settings.aliases or [])
        obj.__meta = settings.meta

        return obj

    @property
    def aliases(self) -> frozenset[Hashable]:
        return self.__aliases

    @override
    def __eq__(self, value: object, /) -> bool:
        return any((self.value == value, value in self.aliases))

    # def __eq__(self, other):
    #     """Сравнение enum с строкой."""
    #     if isinstance(other, str):
    #         return other == self.value or other in self.aliases
    #     return super().__eq__(other)

    # def __str__(self):
    #     return str(self.value)

    # @classmethod
    # def parse(cls, s: str):
    #     """Поиск элемента по строке/алиасу."""
    #     for member in cls:
    #         if s == member.value or s in member.aliases:
    #             return member
    #     raise ValueError(f"{s!r} is not valid for {cls.__name__}")

class Color(EvenBetterEnum):
    RED = ElementSettings("red", [1,2])

print(Color.RED == "red")
