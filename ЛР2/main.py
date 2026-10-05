from colorama import Fore, Style, init

from lab_python_oop.rectangle import Rectangle
from lab_python_oop.circle import Circle
from lab_python_oop.square import Square


def main():
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


if __name__ == "__main__":
    main()
