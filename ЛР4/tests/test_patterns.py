import unittest
from decimal import Decimal
from unittest.mock import Mock
from lab_python_patterns.orders import (
    Coffee, Tea, CoffeeCafe, TeaCafe, Milk, Order, StudentDiscount,
)


class TestPatterns(unittest.TestCase):
    def test_factory_products(self):
        self.assertIsInstance(CoffeeCafe().create_product(), Coffee)
        self.assertIsInstance(TeaCafe().create_product(), Tea)
        self.assertEqual(TeaCafe().order_price(), Decimal("100"))

    def test_decorator(self):
        coffee = Coffee()
        self.assertEqual(Milk(coffee).price(), Decimal("180"))
        self.assertEqual(coffee.price(), Decimal("150"))

    def test_nested_decorator(self):
        self.assertEqual(Milk(Milk(Coffee())).price(), Decimal("210"))

    def test_strategy(self):
        order = Order(Milk(Coffee()), StudentDiscount())
        self.assertEqual(order.total(), Decimal("162.00"))

    def test_default_strategy(self):
        self.assertEqual(Order(Coffee()).total(), Decimal("150"))

    def test_mock_strategy(self):
        strategy = Mock()
        strategy.apply.return_value = Decimal("1")
        self.assertEqual(Order(Coffee(), strategy).total(), Decimal("1"))
        strategy.apply.assert_called_once_with(Decimal("150"))

    def test_mock_product(self):
        product = Mock(spec=Coffee)
        product.price.return_value = Decimal("200")
        self.assertEqual(Milk(product).price(), Decimal("230"))
        product.price.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
