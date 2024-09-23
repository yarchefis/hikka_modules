import time
from datetime import datetime, timedelta
from telethon.tl.types import Message
from .. import loader, utils

class SleepResponder(loader.Module):
    """Автоматический ответчик на сообщения в ночное время"""
    
    strings = {
        "name": "SleepResponder",
        "reply_message": (
            "Человек, которому вы пишите, спит!\n"
            "Напишите ваш вопрос еще раз после 9 утра МСК.\n\n"
            "Все сообщения ниже будут удалены. В случае спама я вас заблокирую."
        )
    }

    async def client_ready(self, client, db):
        self.client = client

    async def message_handler(self, message: Message):
        current_time = datetime.now()
        start_night = current_time.replace(hour=20, minute=0, second=0, microsecond=0)
        end_night = current_time.replace(hour=9, minute=0, second=0, microsecond=0)

        # Проверка на время
        if start_night <= current_time or current_time < end_night:
            await message.reply(self.strings["reply_message"])

            # Удаление сообщения через 5 секунд
            await utils.sleep(1)
            await self.client.delete_messages(message.chat_id, message.id)

            # Проверка на спам
            await self.check_spam(message)

    async def check_spam(self, message: Message):
        # Логика антиспама
        user_id = message.from_id
        if user_id in self.spam_users:
            self.spam_users[user_id] += 1
            if self.spam_users[user_id] > 7:  # Максимум 3 сообщения
                await self.client.block(user_id)
                await message.reply("Вы были заблокированы за спам.")
        else:
            self.spam_users[user_id] = 1

    def __init__(self):
        self.spam_users = {}  # Словарь для отслеживания пользователей
