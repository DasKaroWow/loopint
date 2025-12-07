# 4) Ты хочешь делегировать и скрыть механику
# Например, можно добавить в класс методы:
# нормализация весов,
# объединение объектов,
# вычисление итогового веса,
# сравнение с приблизительным равенством,
# поддержка больших наборов.

from typing import SupportsFloat, override


class WeightedValue(SupportsFloat):
    def __init__(self, value: float, weight: float, /) -> None:
        self.__value = float(value)
        self.__weight = float(weight)

    @property
    def value(self) -> float:
        return self.__value

    @property
    def weight(self) -> float:
        return self.__weight

    @override
    def __float__(self) -> float:
        return self.value * self.weight

    @override
    def __hash__(self) -> int:
        return hash(float(self))

    

a = WeightedValue(2, 0.5)