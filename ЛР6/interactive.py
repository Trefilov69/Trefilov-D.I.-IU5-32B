"""Живой консольный диалог через настоящие обработчики автомата."""
import asyncio
from types import SimpleNamespace
from demo import display
from lab_telegram_fsm.bot import (
    SHAPE, DIMENSIONS, CONFIRM, start, choose_shape, enter_dimensions, confirm, cancel,
)


async def interactive():
    print("Локальный режим без токена Telegram. /exit — выход, /start — сначала, /cancel — отмена.")
    context = SimpleNamespace(user_data={})
    message = SimpleNamespace(text="", reply_text=display)
    update = SimpleNamespace(effective_message=message)
    state = await start(update, context)
    handlers = {SHAPE: choose_shape, DIMENSIONS: enter_dimensions, CONFIRM: confirm}
    while True:
        if state == SHAPE:
            print("1 — Квадрат; 2 — Прямоугольник; 3 — Круг; 0 — Выход")
        elif state == CONFIRM:
            print("1 — Да; 2 — Заново")
        text = input("Вы: ").strip()
        if text == "/exit" or (state in (SHAPE, -1) and text == "0"):
            return
        if text == "/start":
            state = await start(update, context)
        elif text == "/cancel":
            state = await cancel(update, context)
        elif state in handlers:
            if state == SHAPE:
                text = {"1": "Квадрат", "2": "Прямоугольник", "3": "Круг"}.get(text, text)
            elif state == CONFIRM:
                text = {"1": "Да", "2": "Заново"}.get(text, text)
            message.text = text
            state = await handlers[state](update, context)
        else:
            print("Для нового расчета введите /start, для выхода — /exit или 0.")


def run():
    asyncio.run(interactive())
