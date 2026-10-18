import math
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from telegram.ext import ConversationHandler
from lab_telegram_fsm.calculator import calculate
from lab_telegram_fsm.bot import (
    SHAPE, DIMENSIONS, CONFIRM, start, choose_shape, enter_dimensions,
    confirm, cancel, build_application,
)


class TestCalculator(unittest.TestCase):
    def test_shapes(self):
        self.assertEqual(calculate("Квадрат", "5")[1], 25)
        self.assertEqual(calculate("Прямоугольник", "5 4")[1], 20)
        self.assertAlmostEqual(calculate("Круг", "5")[1], math.pi * 25)
        self.assertEqual(calculate("Квадрат", "2,5")[1], 6.25)

    def test_invalid_input(self):
        for text in ("", "abc", "0", "-1", "nan", "inf", "5 4", "1e308", "1e-300"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                calculate("Квадрат", text)


class TestFSM(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.message = SimpleNamespace(text="", reply_text=AsyncMock())
        self.update = SimpleNamespace(effective_message=self.message)
        self.context = SimpleNamespace(user_data={})

    async def call(self, handler, text):
        self.message.text = text
        return await handler(self.update, self.context)

    async def test_full_dialogue(self):
        self.assertEqual(await self.call(start, "/start"), SHAPE)
        self.assertEqual(await self.call(choose_shape, "Прямоугольник"), DIMENSIONS)
        self.assertEqual(await self.call(enter_dimensions, "5 4"), CONFIRM)
        self.assertEqual(await self.call(confirm, "Да"), ConversationHandler.END)
        self.assertIn("20.00", self.message.reply_text.call_args.args[0])
        self.assertEqual(self.context.user_data, {})

    async def test_errors_preserve_state(self):
        await self.call(start, "/start")
        self.assertEqual(await self.call(choose_shape, "Треугольник"), SHAPE)
        await self.call(choose_shape, "Круг")
        self.assertEqual(await self.call(enter_dimensions, "-5"), DIMENSIONS)
        await self.call(enter_dimensions, "5")
        self.assertEqual(await self.call(confirm, "нет"), CONFIRM)

    async def test_restart(self):
        await self.call(start, "/start")
        await self.call(choose_shape, "Квадрат")
        await self.call(enter_dimensions, "5")
        self.assertEqual(await self.call(confirm, "Заново"), SHAPE)
        self.assertEqual(self.context.user_data, {})

    async def test_cancel_from_each_state(self):
        for state in (SHAPE, DIMENSIONS, CONFIRM):
            self.context.user_data.update(shape="Круг", area=20)
            self.assertEqual(await self.call(cancel, "/cancel"), ConversationHandler.END)
            self.assertEqual(self.context.user_data, {})

    async def test_users_are_isolated(self):
        other = SimpleNamespace(user_data={"shape": "Круг"})
        await self.call(start, "/start")
        await self.call(choose_shape, "Квадрат")
        self.assertEqual(other.user_data, {"shape": "Круг"})
        self.assertEqual(self.context.user_data, {"shape": "Квадрат"})

    async def test_exactly_three_states(self):
        app = build_application("123456:LOCAL_TEST_TOKEN")
        self.assertEqual(set(app.handlers[0][0].states), {SHAPE, DIMENSIONS, CONFIRM})
        self.assertEqual(app.update_processor.max_concurrent_updates, 1)


if __name__ == "__main__":
    unittest.main()
