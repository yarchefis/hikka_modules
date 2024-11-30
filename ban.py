import logging
from telethon import events
from .. import loader  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class SimpleResponderMod(loader.Module):
    """Модуль для автоматического ответа на сообщения."""

    strings = {
        "name": "SimpleResponder",
        "response_message": "Извини, но меня поставили сюда следить за сообщениями. По правилам я не могу продолжать разговор."
    }

    async def client_ready(self, client, db):
        self.client = client
        logger.info("SimpleResponderMod загружен и готов к работе.")

    @loader.watcher(incoming=True, only_messages=True)
    async def watcher(self, message):
        if message.is_private and message.sender_id != (await self.client.get_me()).id:
            logger.info(f"Ответ отправлен пользователю: {message.sender_id}")
            await message.reply(self.strings["response_message"])
