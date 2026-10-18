import math
from behave import given, when, then
from lab_python_test.figures import Rectangle, Square, Circle


@given("прямоугольник со сторонами {width:g} и {height:g}")
def rectangle(context, width, height):
    context.figure = Rectangle(width, height)


@given("квадрат со стороной {side:g}")
def square(context, side):
    context.figure = Square(side)


@given("круг с радиусом {radius:g}")
def circle(context, radius):
    context.figure = Circle(radius)


@when("вычислена площадь")
def calculate(context):
    context.area = context.figure.square()


@then("площадь равна {expected:g}")
def check(context, expected):
    assert math.isclose(context.area, expected, rel_tol=1e-12)
