"""Ручная проверка всех семи задач через консольное меню."""
import json
import math
from pathlib import Path
from .field import field
from .gen_random import gen_random
from .unique import Unique
from .print_result import print_result
from .cm_timer import cm_timer_1, cm_timer_2
from .process_data import f1, f2, f3, f4


def read_list(prompt):
    value = json.loads(input(prompt))
    if not isinstance(value, list):
        raise ValueError("Нужен JSON-массив в квадратных скобках")
    return value


def process(choice):
    if choice == "1":
        print('Пример данных: [{"title": "Ковер", "price": 2000}, {"title": "Диван"}]')
        items = read_list("Список словарей JSON: ")
        if any(not isinstance(item, dict) for item in items):
            raise ValueError("Каждый элемент должен быть словарем")
        keys = input("Имена полей через пробел (например title price): ").split()
        if not keys:
            raise ValueError("Укажите хотя бы одно поле")
        print("Результат:", list(field(items, *keys)))
    elif choice == "2":
        count = int(input("Количество чисел (0–10000): "))
        begin = int(input("Минимум: "))
        end = int(input("Максимум: "))
        if not 0 <= count <= 10000:
            raise ValueError("Количество должно быть от 0 до 10000")
        print("Результат:", list(gen_random(count, begin, end)))
    elif choice == "3":
        print('Пример: ["a", "A", "b", "B", 1, 1]')
        items = read_list("Данные JSON: ")
        answer = input("Игнорировать регистр? (да/нет): ").strip().casefold()
        if answer not in ("да", "нет"):
            raise ValueError("Ответьте да или нет")
        print("Результат:", list(Unique(items, ignore_case=answer == "да")))
    elif choice == "4":
        values = [float(x.replace(",", ".")) for x in input("Числа через пробел: ").split()]
        if any(not math.isfinite(x) for x in values):
            raise ValueError("Нужны конечные числа")
        print("Без lambda:", sorted(values, key=abs, reverse=True))
        print("С lambda:", sorted(values, key=lambda x: abs(x), reverse=True))
    elif choice == "5":
        print('Примеры: [1, 2] или {"a": 1} или "текст" или 42')
        value = json.loads(input("Результат функции в формате JSON: "))

        @print_result
        def user_function():
            return value

        user_function()
    elif choice == "6":
        count = int(input("Количество итераций суммирования (0–10000000): "))
        if not 0 <= count <= 10000000:
            raise ValueError("Количество должно быть от 0 до 10000000")
        with cm_timer_1():
            print("Класс, сумма:", sum(range(count)))
        with cm_timer_2():
            print("contextlib, сумма:", sum(range(count)))
    elif choice == "7":
        path = input("Путь к JSON вакансий (Enter — data_demo.json): ").strip().strip('"')
        path = Path(path) if path else Path(__file__).resolve().parents[1] / "data_demo.json"
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
            raise ValueError("Файл должен содержать список словарей с полем job-name")
        if any(item.get("job-name") is not None and not isinstance(item["job-name"], str) for item in data):
            raise ValueError("Поле job-name должно содержать строку или null")
        with cm_timer_1():
            f4(f3(f2(f1(data))))


def main():
    while True:
        print("\n1 — field: выбор полей\n2 — gen_random: случайные числа"
              "\n3 — Unique: удаление повторов\n4 — Сортировка по модулю"
              "\n5 — Декоратор print_result\n6 — Таймеры\n7 — Обработка вакансий\n0 — Выход")
        choice = input("Выберите задачу: ").strip()
        if choice == "0":
            return
        if choice not in tuple("1234567"):
            print("Введите номер от 0 до 7.")
            continue
        try:
            process(choice)
        except (ValueError, OSError, OverflowError) as exc:
            print(f"Ошибка: {exc}. Попробуйте снова.")
