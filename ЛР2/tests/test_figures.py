import unittest
import math

from lab_python_oop.rectangle import Rectangle
from lab_python_oop.circle import Circle
from lab_python_oop.square import Square


class TestFigures(unittest.TestCase):

    def test_rectangle_square(self):
        rectangle = Rectangle(5, 4, "синий")
        self.assertEqual(rectangle.square(), 20)

    def test_square_square(self):
        square = Square(5, "красный")
        self.assertEqual(square.square(), 25)

    def test_circle_square(self):
        circle = Circle(5, "зеленый")
        self.assertAlmostEqual(circle.square(), math.pi * 25)


if __name__ == "__main__":
    unittest.main()
