"""Площади фигур из ЛР2 без зависимости от консольного интерфейса."""
import math
from dataclasses import dataclass


def positive(value):
    """Размер фигуры должен быть конечным положительным числом."""
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Размер должен быть конечным положительным числом")
    return value


@dataclass
class Rectangle:
    width: float
    height: float
    color: str = "синий"

    def __post_init__(self):
        self.width = positive(self.width)
        self.height = positive(self.height)

    def square(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side, color="красный"):
        super().__init__(side, side, color)


@dataclass
class Circle:
    radius: float
    color: str = "зеленый"

    def __post_init__(self):
        self.radius = positive(self.radius)

    def square(self):
        return math.pi * self.radius ** 2


def print_area(figure, output=print):
    """Внедрение зависимости позволяет заменить вывод Mock-объектом."""
    output(f"Площадь: {figure.square():.2f}")
