"""Общий расчет для команды Telegram и ручного ввода в консоли."""
import math


def calculate(shape, text):
    if shape not in ("square", "rectangle", "circle"):
        raise ValueError("Фигура: square, rectangle или circle")
    values = [float(value.replace(",", ".")) for value in text.split()]
    count = 2 if shape == "rectangle" else 1
    if len(values) != count:
        raise ValueError(f"Введите размеров: {count}")
    if any(not math.isfinite(x) or x <= 0 for x in values):
        raise ValueError("Нужны конечные положительные размеры")
    try:
        area = values[0] * values[1] if shape == "rectangle" else values[0] ** 2
        if shape == "circle":
            area *= math.pi
    except OverflowError as exc:
        raise ValueError("Размеры слишком велики") from exc
    if not math.isfinite(area) or area <= 0:
        raise ValueError("Размеры вне поддерживаемого диапазона")
    return area
