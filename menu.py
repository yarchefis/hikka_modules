import logging
from telethon.tl.types import Message
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class TestModule(loader.Module):
    """Модуль с тестовой командой."""
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
        """Команда для тестирования"""
        await utils.answer(message, self.strings["test_message"])
