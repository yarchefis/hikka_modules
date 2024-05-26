import logging
import requests
from telethon import events
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class WikiMod(loader.Module):
    """Модуль для поиска информации на Википедии."""

    strings = {
        "name": "WikiMod",
        "processing": "🔍 Ищем информацию на Википедии...",
        "not_found": "❌ Информация не найдена.",
        "error": "⚠️ Произошла ошибка при запросе к Википедии."
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def wikicmd(self, message):
        """Ищет информацию на Википедии. Использование: .wiki <запрос>"""
        args = utils.get_args_raw(message)
        if not args:
            await message.reply("❓ Укажите запрос для поиска.")
            return

        await message.reply(self.strings["processing"])
        query = args
        url = f"https://ru.wikipedia.org/w/api.php?action=query&titles={query}&prop=extracts&exintro=true&explaintext=true&format=json"

        try:
            response = requests.get(url)
            data = response.json()

            pages = data.get("query", {}).get("pages", {})
            if not pages:
                await message.reply(self.strings["not_found"])
                return

            page = next(iter(pages.values()))
            extract = page.get("extract", self.strings["not_found"])

            await message.reply(extract)
        except Exception as e:
            logger.error(f"Error fetching data from Wikipedia: {e}")
            await message.reply(self.strings["error"])
