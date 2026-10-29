# -*- coding: utf-8 -*-
"""РК №1. Вариант запросов Б, предметная область 21."""

from operator import itemgetter


class Operator:
    """Оператор: ID, название, число применений, ID языка."""

    def __init__(self, id, name, usage_count, language_id):
        self.id = id
        self.name = name
        self.usage_count = usage_count
        self.language_id = language_id


class Language:
    """Язык программирования."""

    def __init__(self, id, name):
        self.id = id
        self.name = name


class OperatorLanguage:
    """Связь оператора и языка: многие-ко-многим."""

    def __init__(self, operator_id, language_id):
        self.operator_id = operator_id
        self.language_id = language_id


languages = [
    Language(1, "Python"),
    Language(2, "C++"),
    Language(3, "Pascal"),
]

operators = [
    Operator(1, "Вызов", 120, 1),
    Operator(2, "Сдвиг разрядов", 25, 2),
    Operator(3, "Присваивание", 200, 1),
]

operator_languages = [
    OperatorLanguage(1, 1),
    OperatorLanguage(1, 2),
    OperatorLanguage(2, 1),
    OperatorLanguage(2, 2),
    OperatorLanguage(3, 3),
]


def solve():
    """Вычислить результаты трех запросов варианта Б."""
    one_to_many = [
        (op.name, lang.name)
        for op in operators
        for lang in languages
        if op.language_id == lang.id
    ]
    many_to_many = [
        (op.id, op.name, lang.name)
        for link in operator_languages
        for op in operators
        for lang in languages
        if link.operator_id == op.id
        and link.language_id == lang.id
    ]

    # Б1: пары (оператор, язык), по названию оператора.
    result_b1 = sorted(one_to_many, key=itemgetter(0))

    # Б2: число операторов каждого языка, по возрастанию.
    result_b2 = sorted(
        [
            (lang.name, sum(
                1 for op in operators
                if op.language_id == lang.id
            ))
            for lang in languages
        ],
        key=itemgetter(1),
    )

    # Б3: операторы на "ов" и связанные с ними языки.
    result_b3 = {
        op.name: [
            name for op_id, _, name in many_to_many
            if op_id == op.id
        ]
        for op in operators
        if op.name.casefold().endswith("ов")
    }
    return result_b1, result_b2, result_b3


def main():
    result_b1, result_b2, result_b3 = solve()
    print("Задание Б1")
    for name, language in result_b1:
        print(f"{name} - {language}")
    print("\nЗадание Б2")
    for language, count in result_b2:
        print(f"{language}: {count}")
    print("\nЗадание Б3")
    for name, names in result_b3.items():
        print(f"{name}: {', '.join(names)}")


if __name__ == "__main__":
    main()
