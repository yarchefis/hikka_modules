# ---------------------------------------------------------------------------------
#  /\_/\  🌐 author web site https://yarchefis.ru
# ( o.o )  🔓 Not licensed.
#  > ^ <  
# ---------------------------------------------------------------------------------
# Name: yMenu
# Description: Модуль личный помощник.
# Author: yarchefis
# ---------------------------------------------------------------------------------

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
        "config_response": "Держи конфиг. Обрати внимание это автоматическое сообщение. Если у тебя есть вопрос, просто напиши его.\n Пожалуйста, не задавайте мета вопросы! Изучи: http://nometa.xyz <emoji document_id=5274196681024348149>😊</emoji>",
        "spam_warning": "<emoji document_id=5447644880824181073>⚠️</emoji> Пожалуйста, не спамьте. Подождите немного перед повторной отправкой сообщения. <emoji document_id=5386367538735104399>⌛</emoji>",
        "not_delivered": 'Ваше сообщение не доставлено! если вы хотите задать вопрос пожалуйста напишите его <a href="http://t.me/yarchefis_hikka_bot?start=feedback">боту</a>',
        "file_chat_id": -1002244812198,  # ID чата
        "file_message_id": 3,  # ID сообщения
        "spam_wait_time": 20  # Время ожидания в секундах между сообщениями
    }

    keywords = [
        "конфиг", "кфг", "варп", "config", "warp", "kfg",
        "конфигурация", "configuration", "конфигурационный", "конфигуратор", "кoнфиг", "kфг"
    ]

    whitelist = [6180493535]  # Замените на реальные ID пользователей, которых нужно добавить в whitelist

    def __init__(self):
        self.last_sent = {}  # Словарь для отслеживания времени последней отправки сообщения каждому пользователю
        self.spam_warned = {}  # Словарь для отслеживания предупреждений пользователей
        self.not_delivered_warned = set()  # Множество для отслеживания, кому уже было отправлено предупреждение о недоставленном сообщении

    async def client_ready(self, client, db):
        self.client = client
        self.me = await client.get_me()  # Получаем информацию о себе

    async def watcher(self, message: Message):
        if message.is_private and message.sender_id != self.me.id:  # Проверяем, что сообщение не от самого себя
            if message.sender_id in self.whitelist:
                # Отправляем подтверждение о прочтении
                await message.client.send_read_acknowledge(
                    message.chat_id, clear_mentions=True
                )
                return  # Игнорируем сообщения от пользователей из whitelist

            if any(keyword in message.raw_text.lower() for keyword in self.keywords):
                now = time()
                if message.sender_id not in self.last_sent or now - self.last_sent[message.sender_id] > self.strings["spam_wait_time"]:
                    self.last_sent[message.sender_id] = now
                    self.spam_warned.pop(message.sender_id, None)  # Сбрасываем предупреждение при успешной отправке
                    await message.reply(self.strings["config_response"])
                    # Пересылаем сообщение
                    await self.client(ForwardMessagesRequest(
                        from_peer=self.strings["file_chat_id"],
                        id=[self.strings["file_message_id"]],
                        to_peer=message.chat_id,
                        with_my_score=False
                    ))
                else:
                    if message.sender_id not in self.spam_warned:
                        self.spam_warned[message.sender_id] = True
                        await message.reply(self.strings["spam_warning"])
                    logger.info(f"Spam protection: Ignored message from {message.sender_id}")
            else:
                if message.sender_id not in self.not_delivered_warned:
                    self.not_delivered_warned.add(message.sender_id)
                    await message.reply(self.strings["not_delivered"])

            # Отправляем подтверждение о прочтении
            await message.client.send_read_acknowledge(
                message.chat_id, clear_mentions=True
            )

    @loader.command()
    async def meta(self, message: Message):
        """Редактирует сообщение с мета вопросами."""
        meta_link = '<a href="http://nometa.xyz">перейди по ссылке и изучи!</a>'
        text = f'Пожалуйста, не задавайте мета вопросы! {meta_link}'
        await utils.answer(message, text)
