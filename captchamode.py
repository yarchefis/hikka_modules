import logging
from telethon import events
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class AutoMuteMod(loader.Module):
    """Модуль для автоматического выдачи мута при присоединении пользователей"""

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

        # Идентификатор чата, который будем отслеживать (замените на свой)
        self.target_chat = -1001234567890

        # Регистрируем событие для отслеживания присоединения пользователей
        self.client.add_event_handler(self.user_joined, events.ChatAction(func=lambda e: e.user_joined and e.chat_id == self.target_chat))

    async def user_joined(self, event):
        try:
            user = await event.get_user()
            user_id = user.id

            # Проверяем, является ли пользователь администратором
            is_admin = await utils.is_user_admin(self.client, self.target_chat, user_id)

            # Если пользователь не администратор, выдаем ему мут
            if not is_admin:
                await self.client.edit_permissions(self.target_chat, user_id, send_messages=False)
                logger.info(f"Выдан мут пользователю {user_id}")

        except Exception as e:
            logger.error(f"Ошибка при обработке присоединения пользователя: {e}")

    async def shutdown(self):
        # Удаляем обработчик событий при завершении модуля
        self.client.remove_event_handler(self.user_joined)

    async def mutecmd(self, message):
        """Команда для выдачи мута пользователю вручную"""
        target_chat = self.target_chat
        args = utils.get_args_raw(message)

        if args:
            try:
                user_id = int(args)
                await self.client.edit_permissions(target_chat, user_id, send_messages=False)
                await message.edit(f"Пользователь с ID {user_id} получил мут в чате.")
            except ValueError:
                await message.edit("Неверный формат ID пользователя.")
            except Exception as e:
                await message.edit(f"Произошла ошибка: {e}")
        else:
            await message.edit("Укажите ID пользователя для выдачи мута.")
