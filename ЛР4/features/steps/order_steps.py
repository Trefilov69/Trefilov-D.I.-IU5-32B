from decimal import Decimal
from behave import given, when, then
from lab_python_patterns.orders import CoffeeCafe, Milk, Order, StudentDiscount


@given("кафе создало кофе")
def coffee(context):
    context.product = CoffeeCafe().create_product()
    context.strategy = None


@given("к напитку добавлено молоко")
def milk(context):
    context.product = Milk(context.product)


@given("выбрана скидка студента")
def discount(context):
    context.strategy = StudentDiscount()


@when("рассчитана стоимость заказа")
def calculate(context):
    context.total = Order(context.product, context.strategy).total()


@then("к оплате {amount} рублей")
def check(context, amount):
    assert context.total == Decimal(amount)
