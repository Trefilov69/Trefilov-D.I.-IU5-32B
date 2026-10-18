import math
import sys
from lab_python_test.figures import Rectangle, Square, Circle, print_area


def demo():
    for figure in (Rectangle(5, 4), Square(5), Circle(5)):
        print(type(figure).__name__)
        print_area(figure)


def main():
    while True:
        print("\n1 — Прямоугольник\n2 — Квадрат\n3 — Круг\n0 — Выход")
        choice = input("Выберите фигуру: ").strip()
        if choice == "0":
            return
        try:
            if choice == "1":
                width = input("Ширина: ").replace(",", ".")
                height = input("Высота: ").replace(",", ".")
                figure = Rectangle(width, height)
            elif choice == "2":
                figure = Square(input("Сторона: ").replace(",", "."))
            elif choice == "3":
                figure = Circle(input("Радиус: ").replace(",", "."))
            else:
                print("Введите номер от 0 до 3.")
                continue
            if not math.isfinite(figure.square()) or figure.square() <= 0:
                raise ValueError("Размеры вне поддерживаемого диапазона")
            print_area(figure)
        except (ValueError, OverflowError) as exc:
            print(f"Ошибка: {exc}. Попробуйте снова.")


if __name__ == "__main__":
    try:
        demo() if "--demo" in sys.argv else main()
    except (EOFError, KeyboardInterrupt):
        print("\nПрограмма завершена.")
