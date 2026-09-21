"""
ЛР №2. Решение биквадратного уравнения A*x^4 + B*x^2 + C = 0.
Процедурная реализация.

Запуск без параметров - коэффициенты вводятся с клавиатуры.
Запуск с параметрами командной строки:
    python biquadratic.py -a <A> -b <B> -c <C>
Если какой-либо параметр не задан или задан некорректно (не приводится
к действительному числу), он игнорируется, и значение запрашивается
с клавиатуры (повторно, пока не будет введено корректное число).
"""

import argparse
import math


def parse_args():
    parser = argparse.ArgumentParser(
        description="Решение биквадратного уравнения A*x^4 + B*x^2 + C = 0"
    )
    parser.add_argument("-a", type=str, default=None, help="коэффициент A")
    parser.add_argument("-b", type=str, default=None, help="коэффициент B")
    parser.add_argument("-c", type=str, default=None, help="коэффициент C")
    return parser.parse_args()


def to_float(value):
    """Пытается преобразовать значение в float. Возвращает None при неудаче."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def read_coefficient(name, cli_value=None):
    """
    Возвращает корректное значение коэффициента name.
    Сначала пробует cli_value (параметр командной строки), если он некорректен
    или отсутствует - запрашивает значение с клавиатуры, пока оно не будет
    успешно преобразовано в действительное число.
    """
    value = to_float(cli_value)
    if cli_value is not None and value is None:
        print(f"Некорректное значение параметра командной строки для {name} "
              f"('{cli_value}'). Значение будет запрошено с клавиатуры.")

    while value is None:
        raw = input(f"Введите коэффициент {name}: ")
        value = to_float(raw)
        if value is None:
            print("Ошибка: значение должно быть действительным числом. Повторите ввод.")

    return value


def solve_quadratic_for_t(a, b, c):
    """
    Решает вспомогательное квадратное уравнение a*t^2 + b*t + c = 0
    (в общем случае может вырождаться в линейное или тождество).
    Возвращает список действительных корней t (без дубликатов).
    """
    roots = []

    if a == 0:
        if b == 0:
            return "infinite" if c == 0 else []
        roots.append(-c / b)
        return roots

    d = b * b - 4 * a * c
    if d < 0:
        return roots
    if d == 0:
        roots.append(-b / (2 * a))
    else:
        sqrt_d = math.sqrt(d)
        roots.append((-b + sqrt_d) / (2 * a))
        roots.append((-b - sqrt_d) / (2 * a))
    return roots


def solve_biquadratic(a, b, c):
    """
    Решает биквадратное уравнение a*x^4 + b*x^2 + c = 0.
    Возвращает (discriminant, x_roots), где discriminant - дискриминант
    вспомогательного квадратного уравнения (None, если a == 0),
    x_roots - отсортированный список действительных корней x (без дубликатов).
    """
    discriminant = None if a == 0 else b * b - 4 * a * c

    t_roots = solve_quadratic_for_t(a, b, c)

    if t_roots == "infinite":
        return discriminant, "infinite"

    x_roots = set()
    for t in t_roots:
        if t > 0:
            sqrt_t = math.sqrt(t)
            x_roots.add(sqrt_t)
            x_roots.add(-sqrt_t)
        elif t == 0:
            x_roots.add(0.0)

    return discriminant, sorted(x_roots)


def main():
    args = parse_args()

    a = read_coefficient("A", args.a)
    b = read_coefficient("B", args.b)
    c = read_coefficient("C", args.c)

    discriminant, x_roots = solve_biquadratic(a, b, c)

    print()
    print(f"Уравнение: {a}*x^4 + {b}*x^2 + {c} = 0")
    if discriminant is not None:
        print(f"Дискриминант вспомогательного уравнения: D = {discriminant}")
    else:
        print("Коэффициент A равен 0, уравнение вырождается (не является биквадратным).")

    if x_roots == "infinite":
        print("Уравнение имеет бесконечное множество решений (тождество 0 = 0).")
    elif not x_roots:
        print("Действительных корней нет.")
    else:
        roots_str = ", ".join(f"x{i + 1} = {x:.6g}" for i, x in enumerate(x_roots))
        print(f"Действительные корни: {roots_str}")


if __name__ == "__main__":
    main()
