import logging
from telethon.tl.types import Message
from telethon.tl.functions.messages import ForwardMessagesRequest
from .. import loader, utils  # type: ignore
from time import time, localtime, strftime
import difflib  # Для работы с похожестью строк

logger = logging.getLogger(__name__)

@loader.tds
class yMenuMod(loader.Module):
    """Модуль личный помощник."""

    strings = {
        "name": "yMenu",
        "config_response": "Держи конфиг. Обрати внимание это автоматическое сообщение. Если у тебя есть вопрос, просто напиши его.\n Пожалуйста, не задавайте мета вопросы! Изучи: http://nometa.xyz <emoji document_id=5274196681024348149>😊</emoji>",
        "spam_warning": "<emoji document_id=5447644880824181073>⚠️</emoji> Пожалуйста, не спамьте. Подождите немного перед повторной отправкой сообщения. <emoji document_id=5386367538735104399>⌛</emoji>",
        "no_greeting_warning": "Приветствие не помешало бы перед тем, как просить конфиг! Будьте вежливы <emoji document_id=5447644880824181073>⚠️</emoji>",
        "file_chat_id": -1002163297996,  # ID чата
        "file_message_id": 6,  # ID сообщения
        "spam_wait_time": 20  # Время ожидания в секундах между сообщениями
    }

    keywords = [
        "конфиг", "кфг", "варп", "config", "warp", "kfg",
        "конфигурация", "configuration", "конфигурационный", "конфигуратор", "кoнфиг", "kфг"
    ]

    greetings = [
        "привет", "здравствуйте", "добрый день", "доброе утро", "добрый вечер",
        "здарова", "здрасте", "салам", "хай", "hello", "hi", "hey"
    ]

    def __init__(self):
        self.last_sent = {}  # Словарь для отслеживания времени последней отправки сообщения каждому пользователю
        self.spam_warned = {}  # Словарь для отслеживания предупреждений пользователей
        self.greeted_today = {}  # Словарь для отслеживания приветствий за текущий день

    async def client_ready(self, client, db):
        self.client = client
        self.me = await client.get_me()  # Получаем информацию о себе

    def is_keyword_match(self, text):
        """Проверка на соответствие текста любому из ключевых слов с учетом опечаток."""
        for keyword in self.keywords:
            # Используем difflib для поиска похожих слов с порогом похожести
            if difflib.SequenceMatcher(None, keyword, text).ratio() > 0.8:
                return True
        return False

    def is_greeting(self, text):
        """Проверка на наличие приветствия в сообщении с учетом опечаток."""
        for greeting in self.greetings:
            if difflib.SequenceMatcher(None, greeting, text).ratio() > 0.8:
                return True
        return False

    def get_current_date(self):
        """Возвращает текущую дату в формате ГГГГ-ММ-ДД."""
        return strftime("%Y-%m-%d", localtime())

    async def watcher(self, message: Message):
        if message.is_private and message.sender_id != self.me.id:  # Проверяем, что сообщение не от самого себя
            message_text = message.raw_text.lower()

            # Проверяем дату последнего приветствия
            current_date = self.get_current_date()
            last_greeted = self.greeted_today.get(message.sender_id)

            # Сброс данных о приветствии, если день сменился
            if last_greeted and last_greeted != current_date:
                self.greeted_today.pop(message.sender_id)

            # Если сообщение содержит приветствие, запоминаем это
            if self.is_greeting(message_text):
                self.greeted_today[message.sender_id] = current_date

            # Проверяем на наличие ключевого слова
            elif self.is_keyword_match(message_text):
                # Проверяем, поприветствовал ли пользователь сегодня
                if message.sender_id not in self.greeted_today:
                    await message.reply(self.strings["no_greeting_warning"])
                else:
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

                # Отправляем подтверждение о прочтении
                await message.client.send_read_acknowledge(
                    message.chat_id, clear_mentions=True
                )

    @loader.command()
    async def meta(self, message: Message):
        """мета команда"""
        meta_link = '<a href="http://nometa.xyz">перейди по ссылке и изучи!</a>'
        text = f'Пожалуйста, не задавайте мета вопросы! {meta_link}'
        await utils.answer(message, text)
