from lab_python_patterns.orders import CoffeeCafe, TeaCafe, Milk, Order, StudentDiscount


def main():
    print(f"Кофе: {CoffeeCafe().order_price()} руб.")
    print(f"Чай: {TeaCafe().order_price()} руб.")
    coffee = Milk(CoffeeCafe().create_product())
    print(f"Кофе с молоком: {coffee.price()} руб.")
    print(f"Со скидкой студента: {Order(coffee, StudentDiscount()).total()} руб.")


if __name__ == "__main__":
    main()
