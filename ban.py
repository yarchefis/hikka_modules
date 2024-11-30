import logging
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from .. import loader  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class SimpleBanResponderMod(loader.Module):
    """Модуль для автоматического ответа, бана и удаления истории у себя."""

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
            logger.info(f"Сообщение от пользователя {sender_id}. Отправляю ответ, блокирую и удаляю историю у себя...")

            try:
                # Отправляем сообщение
                await message.reply(self.strings["response_message"])
                
                # Блокируем пользователя
                await self.client(BlockRequest(sender_id))
                
                # Удаляем историю только у себя
                await self.client(DeleteHistoryRequest(peer=sender_id, just_clear=True, revoke=False))
                
                logger.info(f"Пользователь {sender_id} заблокирован. История удалена только у бота.")
            except Exception as e:
                logger.error(f"Ошибка при обработке пользователя {sender_id}: {e}")
