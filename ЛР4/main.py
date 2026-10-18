import sys
from lab_python_patterns.orders import CoffeeCafe, TeaCafe, Milk, Order, StudentDiscount


def demo():
    print(f"Кофе: {CoffeeCafe().order_price()} руб.")
    print(f"Чай: {TeaCafe().order_price()} руб.")
    coffee = Milk(CoffeeCafe().create_product())
    print(f"Кофе с молоком: {coffee.price()} руб.")
    print(f"Со скидкой студента: {Order(coffee, StudentDiscount()).total()} руб.")


def main():
    while True:
        print("\n1 — Кофе (150 руб.)\n2 — Чай (100 руб.)\n0 — Выход")
        choice = input("Выберите напиток: ").strip()
        if choice == "0":
            return
        if choice not in ("1", "2"):
            print("Введите номер от 0 до 2.")
            continue
        try:
            portions = int(input("Порций молока по 30 руб. (0–10): "))
            if not 0 <= portions <= 10:
                raise ValueError("Количество порций должно быть от 0 до 10")
            discount = input("Скидка студента 10%? (да/нет): ").strip().casefold()
            if discount not in ("да", "нет"):
                raise ValueError("Ответьте да или нет")
            product = (CoffeeCafe() if choice == "1" else TeaCafe()).create_product()
            for _ in range(portions):
                product = Milk(product)
            order = Order(product, StudentDiscount() if discount == "да" else None)
            print(f"Без скидки: {product.price():.2f} руб.")
            print(f"К оплате: {order.total():.2f} руб.")
        except ValueError as exc:
            print(f"Ошибка: {exc}. Попробуйте снова.")


if __name__ == "__main__":
    try:
        demo() if "--demo" in sys.argv else main()
    except (EOFError, KeyboardInterrupt):
        print("\nПрограмма завершена.")
