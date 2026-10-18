import contextlib
import io
import unittest
from unittest.mock import patch
from lab_python_fp.field import field
from lab_python_fp.gen_random import gen_random
from lab_python_fp.unique import Unique
from lab_python_fp.print_result import print_result
from lab_python_fp.cm_timer import cm_timer_1, cm_timer_2
from lab_python_fp.process_data import f1, f2, f3, f4


class TestFunctional(unittest.TestCase):
    def test_field_one(self):
        self.assertEqual(list(field([{}, {"x": None}, {"x": 0}, {"x": ""}], "x")), [0, ""])

    def test_field_many(self):
        self.assertEqual(list(field([{}, {"x": 1, "y": None}, {"y": 2}], "x", "y")),
                         [{"x": 1}, {"y": 2}])
        with self.assertRaises(AssertionError):
            list(field([]))

    def test_random_boundaries(self):
        self.assertEqual(list(gen_random(3, 2, 2)), [2, 2, 2])
        values = list(gen_random(100, 1, 3))
        self.assertEqual(len(values), 100)
        self.assertTrue(all(1 <= x <= 3 for x in values))

    def test_unique(self):
        self.assertEqual(list(Unique(iter(["a", "A", "b", "B"]), ignore_case=True)), ["a", "b"])
        self.assertEqual(list(Unique(["a", "A", "a"])), ["a", "A"])
        self.assertEqual(list(Unique([[1], [1], [2]])), [[1], [2]])

    def test_decorator(self):
        @print_result
        def example(x, y=0):
            return {"sum": x + y}
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(example(2, y=3), {"sum": 5})
        self.assertEqual(stream.getvalue(), "example\nsum = 5\n")
        self.assertEqual(example.__name__, "example")

    def test_timers_propagate_exception(self):
        for timer in (cm_timer_1, cm_timer_2):
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                with self.assertRaisesRegex(RuntimeError, "test"):
                    with timer():
                        raise RuntimeError("test")
            self.assertTrue(stream.getvalue().startswith("time: "))

    def test_pipeline(self):
        data = [{"job-name": "Программист C#"}, {"job-name": "программист c#"},
                {"job-name": "Аналитик"}, {"job-name": None}, {}]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(f1(data), ["Аналитик", "Программист C#"])
            with patch("lab_python_fp.gen_random.randint", return_value=150000):
                self.assertEqual(f4(f3(f2(f1(data)))),
                                 ["Программист C# с опытом Python, зарплата 150000 руб."])


if __name__ == "__main__":
    unittest.main()
