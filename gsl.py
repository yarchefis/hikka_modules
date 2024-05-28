import logging
from telethon import events
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class VoiceLinkMod(loader.Module):
    """Модуль для отправки ссылки на голосовое сообщение в Telegram."""

    strings = {
        "name": "VoiceLinkMod",
        "no_voice_message": "⚠️ Это не голосовое сообщение. Ответьте на голосовое сообщение, чтобы получить ссылку на него."
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    @loader.ratelimit
    async def gslcmd(self, message):
        """Отправить ссылку на голосовое сообщение."""
        if message.is_reply and message.reply_to_msg_id:
            reply_message = await message.get_reply_message()
            if reply_message.voice:
                voice_msg = reply_message.voice
                # Формируем ссылку на голосовое сообщение
                voice_link = f"https://t.me/c/{voice_msg.chat_id}/{voice_msg.id}"
                await message.reply(f"🔊 [Голосовое сообщение]({voice_link})")
            else:
                await message.reply(self.strings["no_voice_message"])
        else:
            await message.reply(self.strings["no_voice_message"])

