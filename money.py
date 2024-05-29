import logging
import re
import random
from telethon.tl.types import Message
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class MoneyRequestHandlerMod(loader.Module):
    """Модуль для автоматического ответа на просьбы о деньгах."""

    strings = {
        "name": "Money"
    }

    responses = [
        "Извини, не могу помочь.",
        "Я не занимаю деньги.",
        "Пожалуйста, не проси меня о деньгах.",
        "Нет, у меня нет лишних денег.",
        "Не могу этого сделать.",
        "Я не выдаю займы."
    ]

    keywords = [
        "дай деняг", "дай денег", "дай долг", "займи", "занять", "одолжи", "одолжить", "нужны деньги",
        "мне денег", "можешь занять", "могу занять", "денег в долг", "денег взаймы", "занять денег", "бабки",
        "бабло", "моней", "money", "нужен долг", "мне нужно занять", "займи денег", "дай бабки", "дай бабло",
        "одолжи бабки", "одолжи денег", "одолжи бабло", "одолжи моней", "деньги в долг", "в долг денег",
        "помоги деньгами", "мне нужны деньги", "можешь одолжить", "можешь занять денег", "мне нужно бабло",
        "помоги баблом", "помоги с деньгами", "займи немного денег", "занять немного денег", "нужно бабло",
        "подкинь бабла", "подкинь денег", "финансовая помощь", "дай на время денег", "займи на время денег",
        "займи рубль"
    ]

    async def client_ready(self, client, db):
        self.client = client
        self.me = await client.get_me()  # Получаем информацию о себе

    async def watcher(self, message: Message):
        if message.is_private and message.sender_id != self.me.id:  # Проверяем, что сообщение не от самого себя
            if any(re.search(r'\b' + re.escape(keyword) + r'\b', message.raw_text.lower()) for keyword in self.keywords):
                response = random.choice(self.responses)
                await message.reply(response)
                # Отправляем подтверждение о прочтении
                await message.client.send_read_acknowledge(
                    message.chat_id, clear_mentions=True
                )
