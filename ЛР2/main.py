from colorama import Fore, Style, init

import math
import sys
from lab_python_oop.rectangle import Rectangle
from lab_python_oop.circle import Circle
from lab_python_oop.square import Square


def demo():
    init()

    n = 5

    rectangle = Rectangle(n, n, "синий")
    circle = Circle(n, "зеленый")
    square = Square(n, "красный")

    print(rectangle)
    print(circle)
    print(square)

    print(
        Fore.CYAN +
        "Внешний пакет colorama успешно работает."
        + Style.RESET_ALL
    )


def read_size(prompt):
    value = float(input(prompt).replace(",", "."))
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Размер должен быть конечным положительным числом")
    return value


def main():
    init()
    while True:
        print("\n1 — Прямоугольник\n2 — Квадрат\n3 — Круг\n0 — Выход")
        choice = input("Выберите фигуру: ").strip()
        if choice == "0":
            return
        if choice not in ("1", "2", "3"):
            print("Введите номер от 0 до 3.")
            continue
        try:
            if choice == "1":
                dimensions = (read_size("Ширина: "), read_size("Высота: "))
                constructor = Rectangle
            else:
                dimensions = (read_size("Радиус: " if choice == "3" else "Сторона: "),)
                constructor = Circle if choice == "3" else Square
            color = input("Цвет (Enter — синий): ").strip() or "синий"
            figure = constructor(*dimensions, color)
            if not math.isfinite(figure.square()) or figure.square() <= 0:
                raise ValueError("Размеры вне поддерживаемого диапазона")
            print(Fore.CYAN + str(figure) + Style.RESET_ALL)
        except (ValueError, OverflowError) as exc:
            print(f"Ошибка: {exc}. Попробуйте снова.")


if __name__ == "__main__":
    try:
        demo() if "--demo" in sys.argv else main()
    except (EOFError, KeyboardInterrupt):
        print("\nПрограмма завершена.")
