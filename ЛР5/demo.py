"""Локальный вызов настоящих обработчиков без Telegram API и токена."""
import asyncio
from types import SimpleNamespace
from lab_telegram_bot.bot import start, choose_figure, help_command


async def display(text, **kwargs):
    print("Бот:", text)
    markup = kwargs.get("reply_markup")
    if markup:
        print("Кнопки:", ", ".join(b.text for row in markup.inline_keyboard for b in row))


async def answer():
    pass


async def demo():
    print("Локальная демонстрация обработчиков, без подключения к Telegram.")
    message = SimpleNamespace(reply_text=display)
    query = SimpleNamespace(data="square", answer=answer, edit_message_text=display)
    update = SimpleNamespace(effective_message=message, callback_query=query)
    print("Пользователь: /start")
    await start(update, None)
    for key in ("square", "rectangle", "circle"):
        print("Пользователь нажал:", key)
        query.data = key
        await choose_figure(update, None)
    print("Пользователь: /help")
    await help_command(update, None)


def run():
    asyncio.run(demo())


if __name__ == "__main__":
    run()
