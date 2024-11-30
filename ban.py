import logging
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from .. import loader  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class SimpleBanResponderMod(loader.Module):
    """Модуль для ответа, бана и удаления истории только у себя."""

    strings = {
        "name": "SimpleBanResponder",
        "response_message": "Извини, но ты нарушил правила общения. Ты будешь заблокирован."
    }

    async def client_ready(self, client, db):
        self.client = client
        logger.info("SimpleBanResponderMod загружен и готов к работе.")

    @loader.watcher(incoming=True, only_messages=True)
    async def watcher(self, message):
        if message.is_private and message.sender_id != (await self.client.get_me()).id:
            sender_id = message.sender_id
            logger.info(f"Получено сообщение от {sender_id}. Обрабатываю...")

            try:
                # Отправляем сообщение
                await message.reply(self.strings["response_message"])
                
                # Блокируем пользователя
                result = await self.client(BlockRequest(id=sender_id))
                logger.info(f"Пользователь {sender_id} заблокирован. Результат: {result}")

            except Exception as e:
                logger.error(f"Ошибка при обработке пользователя {sender_id}: {e}")
