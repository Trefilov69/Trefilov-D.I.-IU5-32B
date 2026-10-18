import math
import unittest
from unittest.mock import Mock
from lab_python_test.figures import Rectangle, Square, Circle, print_area


class TestFigures(unittest.TestCase):
    def test_rectangle(self):
        self.assertEqual(Rectangle(5, 4).square(), 20)

    def test_square(self):
        self.assertEqual(Square(5).square(), 25)

    def test_circle(self):
        self.assertAlmostEqual(Circle(5).square(), math.pi * 25)

    def test_invalid_dimensions(self):
        for value in (0, -1, float("nan"), float("inf"), "abc"):
            for constructor in (Circle, Square, lambda x: Rectangle(2, x)):
                with self.subTest(value=value, constructor=constructor):
                    with self.assertRaises(ValueError):
                        constructor(value)

    def test_output_with_mock(self):
        output = Mock()
        print_area(Rectangle(5, 4), output)
        output.assert_called_once_with("Площадь: 20.00")


if __name__ == "__main__":
    unittest.main()
