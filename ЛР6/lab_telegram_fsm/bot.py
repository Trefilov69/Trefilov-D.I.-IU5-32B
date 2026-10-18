import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, filters,
)
from .calculator import SHAPES, calculate

SHAPE, DIMENSIONS, CONFIRM = range(3)


def shape_keyboard():
    return ReplyKeyboardMarkup([[name] for name in SHAPES], resize_keyboard=True,
                               one_time_keyboard=True)


async def start(update, context):
    context.user_data.clear()
    await update.effective_message.reply_text(
        "Выберите фигуру. /cancel — отменить расчет.", reply_markup=shape_keyboard()
    )
    return SHAPE


async def choose_shape(update, context):
    shape = update.effective_message.text.strip()
    if shape not in SHAPES:
        await update.effective_message.reply_text("Выберите фигуру кнопкой.")
        return SHAPE
    context.user_data["shape"] = shape
    prompt = "Введите две стороны через пробел:" if shape == "Прямоугольник" else (
        "Введите радиус:" if shape == "Круг" else "Введите сторону:")
    await update.effective_message.reply_text(prompt, reply_markup=ReplyKeyboardRemove())
    return DIMENSIONS


async def enter_dimensions(update, context):
    shape = context.user_data["shape"]
    try:
        values, area = calculate(shape, update.effective_message.text)
    except ValueError as exc:
        await update.effective_message.reply_text(f"Ошибка: {exc}. Повторите ввод.")
        return DIMENSIONS
    context.user_data.update(values=values, area=area)
    await update.effective_message.reply_text(
        f"{shape}; размеры: {', '.join(map(str, values))}. Подтвердить?",
        reply_markup=ReplyKeyboardMarkup([["Да", "Заново"]], resize_keyboard=True),
    )
    return CONFIRM


async def confirm(update, context):
    text = update.effective_message.text.strip().casefold()
    if text == "заново":
        return await start(update, context)
    if text != "да":
        await update.effective_message.reply_text("Нажмите Да или Заново.")
        return CONFIRM
    await update.effective_message.reply_text(
        f"Площадь: {context.user_data['area']:.2f}\nНовый расчет: /start",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update, context):
    context.user_data.clear()
    await update.effective_message.reply_text(
        "Расчет отменен. Новый расчет: /start", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def build_application(token):
    # ConversationHandler требует последовательной обработки обновлений.
    app = Application.builder().token(token).concurrent_updates(False).build()
    private_text = filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND
    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start, filters=filters.ChatType.PRIVATE)],
        states={
            SHAPE: [MessageHandler(private_text, choose_shape)],
            DIMENSIONS: [MessageHandler(private_text, enter_dimensions)],
            CONFIRM: [MessageHandler(private_text, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(conversation)
    return app


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Задайте переменную окружения TELEGRAM_BOT_TOKEN из BotFather.")
    build_application(token).run_polling()
