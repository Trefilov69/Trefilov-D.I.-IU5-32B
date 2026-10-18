"""Справочник геометрических фигур с inline-клавиатурой."""
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

FIGURES = {
    "square": ("Квадрат", "S = a². При a = 5: S = 25."),
    "rectangle": ("Прямоугольник", "S = a × b. При a = 5, b = 4: S = 20."),
    "circle": ("Круг", "S = π × r². При r = 5: S ≈ 78.54."),
}


def keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(title, callback_data=key)]
        for key, (title, _) in FIGURES.items()
    ])


async def start(update, context):
    await update.effective_message.reply_text(
        "Справочник площадей. Выберите фигуру:", reply_markup=keyboard()
    )


async def help_command(update, context):
    await update.effective_message.reply_text(
        "/start — открыть кнопки\n/help — справка\n"
        "Нажмите кнопку, чтобы узнать формулу и пример расчета."
    )


async def choose_figure(update, context):
    query = update.callback_query
    await query.answer()
    figure = FIGURES.get(query.data)
    text = "Неизвестная фигура. Выберите кнопку ниже."
    if figure is not None:
        text = f"{figure[0]}\n{figure[1]}"
    await query.edit_message_text(text, reply_markup=keyboard())


def build_application(token):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(choose_figure))
    return app


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Задайте переменную окружения TELEGRAM_BOT_TOKEN из BotFather.")
    build_application(token).run_polling()
