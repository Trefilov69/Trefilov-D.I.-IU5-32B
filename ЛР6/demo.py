"""Проверяемый локальный диалог через настоящие обработчики."""
import asyncio
from types import SimpleNamespace
from lab_telegram_fsm.bot import start, choose_shape, enter_dimensions, confirm


async def display(text, **kwargs):
    print("Бот:", text)
    markup = kwargs.get("reply_markup")
    if hasattr(markup, "keyboard"):
        print("Кнопки:", ", ".join(b.text for row in markup.keyboard for b in row))


async def demo():
    print("Локальная демонстрация обработчиков, без подключения к Telegram.")
    context = SimpleNamespace(user_data={})
    message = SimpleNamespace(text="", reply_text=display)
    update = SimpleNamespace(effective_message=message)
    for text, handler in (("/start", start), ("Прямоугольник", choose_shape),
                          ("-5 4", enter_dimensions), ("5 4", enter_dimensions),
                          ("Да", confirm)):
        message.text = text
        print("Пользователь:", text)
        state = await handler(update, context)
        print("Состояние:", {0: "SHAPE", 1: "DIMENSIONS", 2: "CONFIRM", -1: "END"}[state])


def run():
    asyncio.run(demo())


if __name__ == "__main__":
    run()
