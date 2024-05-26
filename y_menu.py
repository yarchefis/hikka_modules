import logging
from telethon.tl.types import Message
from telethon.tl.functions.messages import ForwardMessagesRequest
from .. import loader, utils  # type: ignore
from time import time

logger = logging.getLogger(__name__)

@loader.tds
class yMenuMod(loader.Module):
    """Модуль личный помощник."""

    strings = {
        "name": "yMenu",
        "config_response": "🔍 Найдено совпадение: конфигурационный файл warp. \n Это автоматическое сообщение! Если у тебя есть вопрос, просто напиши его. 😊",
        "spam_warning": "⚠️ Пожалуйста, не спамьте. Подождите немного перед повторной отправкой сообщения. ⌛",
        "file_chat_id": -1002244812198,  # ID чата
        "file_message_id": 3,  # ID сообщения
        "spam_wait_time": 20  # Время ожидания в секундах между сообщениями
    }

    keywords = [
        "конфиг", "кфг", "варп", "config", "warp", "kfg",
        "конфигурация", "configuration", "конфигурационный", "конфигуратор"
    ]

    def __init__(self):
        self.last_sent = {}  # Словарь для отслеживания времени последней отправки сообщения каждому пользователю
        self.spam_warned = {}  # Словарь для отслеживания предупреждений пользователей
        self.contacts = []  # Список контактов

    async def client_ready(self, client, db):
        self.client = client
        self.me = await client.get_me()  # Получаем информацию о себе
        self.contacts = await self.client.get_contacts()

    async def watcher(self, message: Message):
        if message.is_private and message.sender_id != self.me.id:  # Проверяем, что сообщение не от самого себя
            # Проверяем, есть ли отправитель в контактах
            sender_in_contacts = any(
                contact.user_id == message.sender_id for contact in self.contacts
            )
            if sender_in_contacts:
                return  # Не отвечаем, если отправитель в контактах

            # Проверяем время между отправками сообщений
            now = time()
            if message.sender_id in self.last_sent and now - self.last_sent[message.sender_id] <= self.strings["spam_wait_time"]:
                if message.sender_id not in self.spam_warned:
                    self.spam_warned[message.sender_id] = True
                    await message.reply(self.strings["spam_warning"])
                logger.info(f"Spam protection: Ignored message from {message.sender_id}")
                return

            # Обновляем время последней отправки
            self.last_sent[message.sender_id] = now
            self.spam_warned.pop(message.sender_id, None)  # Сбрасываем предупреждение при успешной отправке

            # Проверяем наличие ключевых слов
            for keyword in self.keywords:
                if keyword in message.raw_text.lower():
                    await message.reply(self.strings["config_response"])
                    # Пересылаем сообщение
                    await self.client(ForwardMessagesRequest(
                        from_peer=self.strings["file_chat_id"],
                        id=[self.strings["file_message_id"]],
                        to_peer=message.chat_id,
                        with_my_score=False
                    ))
                    break

            # Отправляем подтверждение о прочтении
            await message.client.send_read_acknowledge(
                message.chat_id, clear_mentions=True
            )
