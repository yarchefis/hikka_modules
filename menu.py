import logging
from telethon.tl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class TestModule(loader.Module):
    """Модуль с тестовой командой и кнопкой."""
    strings = {
        "name": "TestModule",
        "test_message": "тест"
    }

    async def client_ready(self, client, db):
        self.client = client

    async def test(self, message: Message):
        """Команда для тестирования с кнопкой"""
        await self.inline.form(
            self.strings["test_message"],
            message=message,
            reply_markup={
                "text": "Нажми меня",
                "callback": self.handle_button_click
            }
        )

    async def handle_button_click(self, call):
        await call.answer("Кнопка нажата!")
