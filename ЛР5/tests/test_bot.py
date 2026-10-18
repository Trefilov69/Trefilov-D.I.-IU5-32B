import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from lab_telegram_bot.bot import start, choose_figure, keyboard, build_application, area_command


class TestBot(unittest.IsolatedAsyncioTestCase):
    async def test_start_buttons(self):
        message = SimpleNamespace(reply_text=AsyncMock())
        await start(SimpleNamespace(effective_message=message), None)
        markup = message.reply_text.call_args.kwargs["reply_markup"]
        self.assertEqual(len(markup.inline_keyboard), 3)

    async def test_all_buttons(self):
        for key, expected in (("square", "25"), ("rectangle", "20"), ("circle", "78.54")):
            with self.subTest(key=key):
                query = SimpleNamespace(data=key, answer=AsyncMock(), edit_message_text=AsyncMock())
                await choose_figure(SimpleNamespace(callback_query=query), None)
                query.answer.assert_awaited_once()
                self.assertIn(expected, query.edit_message_text.call_args.args[0])

    async def test_unknown_callback(self):
        query = SimpleNamespace(data="bad", answer=AsyncMock(), edit_message_text=AsyncMock())
        await choose_figure(SimpleNamespace(callback_query=query), None)
        self.assertIn("Неизвестная", query.edit_message_text.call_args.args[0])

    async def test_application_configuration(self):
        app = build_application("123456:LOCAL_TEST_TOKEN")
        self.assertEqual(len(app.handlers[0]), 4)
        self.assertEqual([row[0].callback_data for row in keyboard().inline_keyboard],
                         ["square", "rectangle", "circle"])

    async def test_custom_dimensions(self):
        message = SimpleNamespace(reply_text=AsyncMock())
        for args, expected in ((["rectangle", "6", "7"], "42.00"),
                               (["square", "2,5"], "6.25"),
                               (["circle", "2"], "12.57"),
                               (["square", "nan"], "Ошибка"),
                               (["square", "-2"], "Ошибка"),
                               (["rectangle", "2"], "Ошибка"),
                               (["square", "1e308"], "Ошибка"),
                               ([], "Ошибка")):
            with self.subTest(args=args):
                await area_command(SimpleNamespace(effective_message=message),
                                   SimpleNamespace(args=args))
                self.assertIn(expected, message.reply_text.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
