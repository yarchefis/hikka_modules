import logging
from telethon import events
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class AutoMessageMod(loader.Module):
    """Модуль для автоматической отправки сообщения при присоединении пользователей"""

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

        # Идентификатор чата, который будем отслеживать (замените на свой)
        self.target_chat = -1001234567890

        # Регистрируем событие для отслеживания присоединения пользователей
        self.client.add_event_handler(self.user_joined, events.NewMessage(incoming=True, chats=[self.target_chat]))

    async def user_joined(self, event):
        try:
            message = event.message
            if message.user_id != event.chat_id:
                return

            user = await event.get_user()
            user_id = user.id

            # Отправляем приветственное сообщение пользователю
            await self.client.send_message(self.target_chat, f"Добро пожаловать, {user.username}!")

            logger.info(f"Отправлено приветственное сообщение пользователю {user_id}")

        except Exception as e:
            logger.error(f"Ошибка при обработке присоединения пользователя: {e}")
