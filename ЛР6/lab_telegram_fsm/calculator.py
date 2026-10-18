import math

SHAPES = {"Квадрат": 1, "Прямоугольник": 2, "Круг": 1}


def calculate(shape, text):
    """Разбор размеров и вычисление площади без зависимости от Telegram."""
    if shape not in SHAPES:
        raise ValueError("Неизвестная фигура")
    try:
        values = [float(part.replace(",", ".")) for part in text.split()]
    except ValueError as exc:
        raise ValueError("Введите числа через пробел") from exc
    if len(values) != SHAPES[shape]:
        raise ValueError(f"Количество размеров: {SHAPES[shape]}")
    if any(not math.isfinite(x) or x <= 0 for x in values):
        raise ValueError("Размеры должны быть конечными положительными числами")
    try:
        if shape == "Квадрат":
            area = values[0] ** 2
        elif shape == "Круг":
            area = math.pi * values[0] ** 2
        else:
            area = values[0] * values[1]
    except OverflowError as exc:
        raise ValueError("Размеры слишком велики") from exc
    if not math.isfinite(area) or area <= 0:
        raise ValueError("Размеры вне поддерживаемого диапазона")
    return values, area
