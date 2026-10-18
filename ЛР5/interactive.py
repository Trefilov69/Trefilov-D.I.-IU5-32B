"""Ручной вызов тех же обработчиков, которые использует Telegram."""
import asyncio
from types import SimpleNamespace
from demo import display, answer
from lab_telegram_bot.bot import start, choose_figure, area_command


async def interactive():
    print("Локальный режим без токена Telegram. Вводите номера кнопок.")
    query = SimpleNamespace(data="", answer=answer, edit_message_text=display)
    update = SimpleNamespace(effective_message=SimpleNamespace(reply_text=display),
                             callback_query=query)
    context = SimpleNamespace(args=[])
    await start(update, context)
    while True:
        choice = input("\n1 — Квадрат; 2 — Прямоугольник; 3 — Круг; 0 — Выход: ").strip()
        if choice == "0":
            return
        shape = {"1": "square", "2": "rectangle", "3": "circle"}.get(choice)
        if shape is None:
            print("Введите номер от 0 до 3.")
            continue
        query.data = shape
        await choose_figure(update, context)
        text = input("Две стороны через пробел: " if shape == "rectangle" else
                     "Радиус: " if shape == "circle" else "Сторона: ")
        context.args = [shape, *text.split()]
        await area_command(update, context)


def run():
    asyncio.run(interactive())
