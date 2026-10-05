from lab_python_oop.geometric_figure import GeometricFigure
from lab_python_oop.figure_color import FigureColor


class Rectangle(GeometricFigure):

    FIGURE_TYPE = "Прямоугольник"

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.fc = FigureColor(color)

    def square(self):
        return self.width * self.height

    @classmethod
    def get_figure_type(cls):
        return cls.FIGURE_TYPE

    def __repr__(self):
        return "{}: ширина = {}, высота = {}, цвет = {}, площадь = {}".format(
            self.get_figure_type(),
            self.width,
            self.height,
            self.fc.color,
            self.square()
        )
