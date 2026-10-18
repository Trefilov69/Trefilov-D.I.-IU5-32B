"""Фабричный метод, Декоратор и Стратегия в одной предметной области."""
from abc import ABC, abstractmethod
from decimal import Decimal


class Product(ABC):
    @abstractmethod
    def price(self):
        """Стоимость позиции."""


class Coffee(Product):
    def price(self):
        return Decimal("150")


class Tea(Product):
    def price(self):
        return Decimal("100")


class Cafe(ABC):
    """Создатель: подклассы переопределяют фабричный метод."""
    @abstractmethod
    def create_product(self):
        """Создать продукт."""

    def order_price(self):
        return self.create_product().price()


class CoffeeCafe(Cafe):
    def create_product(self):
        return Coffee()


class TeaCafe(Cafe):
    def create_product(self):
        return Tea()


class Milk(Product):
    """Структурный Декоратор сохраняет интерфейс оборачиваемого объекта."""
    def __init__(self, product):
        self.product = product

    def price(self):
        return self.product.price() + Decimal("30")


class PricingStrategy(ABC):
    @abstractmethod
    def apply(self, amount):
        """Применить правило расчета."""


class RegularPrice(PricingStrategy):
    def apply(self, amount):
        return amount


class StudentDiscount(PricingStrategy):
    def apply(self, amount):
        return (amount * Decimal("0.90")).quantize(Decimal("0.01"))


class Order:
    def __init__(self, product, strategy=None):
        self.product = product
        self.strategy = strategy if strategy is not None else RegularPrice()

    def total(self):
        return self.strategy.apply(self.product.price())
