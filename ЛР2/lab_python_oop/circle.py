import math

from lab_python_oop.geometric_figure import GeometricFigure
from lab_python_oop.figure_color import FigureColor


class Circle(GeometricFigure):

    FIGURE_TYPE = "Круг"

    def __init__(self, radius, color):
        self.radius = radius
        self.fc = FigureColor(color)

    def square(self):
        return math.pi * self.radius ** 2

    @classmethod
    def get_figure_type(cls):
        return cls.FIGURE_TYPE

    def __repr__(self):
        return "{}: радиус = {}, цвет = {}, площадь = {:.2f}".format(
            self.get_figure_type(),
            self.radius,
            self.fc.color,
            self.square()
        )
