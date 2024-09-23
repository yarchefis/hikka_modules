import logging
from telethon.tl.types import Message, ReplyKeyboardMarkup, KeyboardButton
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class TestModule(loader.Module):
    """Модуль с тестовой командой и кнопкой."""
    strings = {
        "name": "TestModule",
        "test_message": "тест"
    }

    def __init__(self):
        pass

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def test(self, message: Message):
        """Команда для тестирования с кнопкой"""
        button = KeyboardButton("Нажми меня")
        markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)

        await message.reply(self.strings["test_message"], reply_markup=markup)
