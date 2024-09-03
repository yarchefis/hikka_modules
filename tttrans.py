import logging
import re
import requests
from telethon.tl.types import Message
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

class TranslationHandlerMod(loader.Module):
    """Модуль для перевода сообщений с использованием MyMemory API."""

    strings = {
        "name": "TranslationHandler"
    }

    special_letters = "Ғғ Җ җ Ҙҙ Ҡҡ ң Өө ҫ Үү Һһ Әә"
    chat_id = 831408739
    api_url = "https://api.mymemory.translated.net/get"

    async def client_ready(self, client, db):
        self.client = client
        self.me = await client.get_me()

    async def watcher(self, message: Message):
        if message.chat_id == self.chat_id and message.sender_id != self.me.id:
            text = message.raw_text
            if any(letter in text for letter in self.special_letters):
                # Отправляем весь текст на перевод
                response = requests.get(self.api_url, params={
                    'q': text,
                    'langpair': 'tt|ru'
                }).json()
                translated_text = response.get('responseData', {}).get('translatedText', None)
                if translated_text:
                    await message.reply(translated_text)
            else:
                # Берем первые два слова и определяем язык
                first_two_words = ' '.join(text.split()[:2])
                response = requests.get(self.api_url, params={
                    'q': first_two_words,
                    'langpair': 'autodetect|ru'
                }).json()
                detected_language = response.get('responseData', {}).get('detectedLanguage', 'unknown')

                if detected_language in ['ba', 'tt']:
                    # Переводим весь текст, но сохраняем язык tt
                    response = requests.get(self.api_url, params={
                        'q': text,
                        'langpair': 'tt|ru'
                    }).json()
                    translated_text = response.get('responseData', {}).get('translatedText', None)
                    if translated_text:
                        await message.reply(translated_text)
                else:
                    # Иначе не отвечаем
                    pass
