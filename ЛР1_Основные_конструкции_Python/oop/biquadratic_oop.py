"""
ЛР №2. Решение биквадратного уравнения A*x^4 + B*x^2 + C = 0.
Объектно-ориентированная реализация.

Запуск без параметров - коэффициенты вводятся с клавиатуры.
Запуск с параметрами командной строки:
    python biquadratic_oop.py -a <A> -b <B> -c <C>
Если какой-либо параметр не задан или задан некорректно (не приводится
к действительному числу), он игнорируется, и значение запрашивается
с клавиатуры (повторно, пока не будет введено корректное число).
"""

import argparse
import math


class CoefficientReader:
    """Отвечает за получение корректного значения коэффициента."""

    @staticmethod
    def to_float(value):
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def read(self, name, cli_value=None):
        value = self.to_float(cli_value)
        if cli_value is not None and value is None:
            print(f"Некорректное значение параметра командной строки для {name} "
                  f"('{cli_value}'). Значение будет запрошено с клавиатуры.")

        while value is None:
            raw = input(f"Введите коэффициент {name}: ")
            value = self.to_float(raw)
            if value is None:
                print("Ошибка: значение должно быть действительным числом. Повторите ввод.")

        return value


class BiquadraticEquation:
    """Представляет биквадратное уравнение A*x^4 + B*x^2 + C = 0 и его решение."""

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.discriminant = None
        self.x_roots = []

    def _solve_quadratic_for_t(self):
        a, b, c = self.a, self.b, self.c

        if a == 0:
            if b == 0:
                return "infinite" if c == 0 else []
            return [-c / b]

        self.discriminant = b * b - 4 * a * c
        d = self.discriminant

        if d < 0:
            return []
        if d == 0:
            return [-b / (2 * a)]

        sqrt_d = math.sqrt(d)
        return [(-b + sqrt_d) / (2 * a), (-b - sqrt_d) / (2 * a)]

    def solve(self):
        """Вычисляет дискриминант и действительные корни уравнения."""
        t_roots = self._solve_quadratic_for_t()

        if t_roots == "infinite":
            self.x_roots = "infinite"
            return self.x_roots

        roots = set()
        for t in t_roots:
            if t > 0:
                sqrt_t = math.sqrt(t)
                roots.add(sqrt_t)
                roots.add(-sqrt_t)
            elif t == 0:
                roots.add(0.0)

        self.x_roots = sorted(roots)
        return self.x_roots

    def report(self):
        lines = [f"Уравнение: {self.a}*x^4 + {self.b}*x^2 + {self.c} = 0"]

        if self.a != 0:
            lines.append(f"Дискриминант вспомогательного уравнения: D = {self.discriminant}")
        else:
            lines.append("Коэффициент A равен 0, уравнение вырождается (не является биквадратным).")

        if self.x_roots == "infinite":
            lines.append("Уравнение имеет бесконечное множество решений (тождество 0 = 0).")
        elif not self.x_roots:
            lines.append("Действительных корней нет.")
        else:
            roots_str = ", ".join(f"x{i + 1} = {x:.6g}" for i, x in enumerate(self.x_roots))
            lines.append(f"Действительные корни: {roots_str}")

        return "\n".join(lines)


class Application:
    """Управляет вводом коэффициентов и выводом результата."""

    def __init__(self):
        self.reader = CoefficientReader()

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Решение биквадратного уравнения A*x^4 + B*x^2 + C = 0"
        )
        parser.add_argument("-a", type=str, default=None, help="коэффициент A")
        parser.add_argument("-b", type=str, default=None, help="коэффициент B")
        parser.add_argument("-c", type=str, default=None, help="коэффициент C")
        return parser.parse_args()

    def run(self):
        args = self.parse_args()

        a = self.reader.read("A", args.a)
        b = self.reader.read("B", args.b)
        c = self.reader.read("C", args.c)

        equation = BiquadraticEquation(a, b, c)
        equation.solve()

        print()
        print(equation.report())


if __name__ == "__main__":
    Application().run()
