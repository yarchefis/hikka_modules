import logging
from telethon import events
from telethon.tl.types import DocumentAttributeAudio
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class VoiceLinkMod(loader.Module):
    """Модуль для пересылки голосового сообщения в тот же чат."""

    strings = {
        "name": "VoiceLinkMod",
        "no_voice_message": "⚠️ Это не голосовое сообщение. Ответьте на голосовое сообщение, чтобы получить ссылку на него."
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    @loader.ratelimit
    async def gslcmd(self, message):
        """Переслать голосовое сообщение."""
        if message.is_reply and message.reply_to_msg_id:
            reply_message = await message.get_reply_message()
            if reply_message.voice:
                # Скачиваем голосовое сообщение
                file_path = await self.client.download_media(reply_message, file="voice_note.ogg")

                # Отправляем голосовое сообщение обратно в чат
                await self.client.send_file(
                    message.chat_id,
                    file_path,
                    voice_note=True,
                    attributes=reply_message.document.attributes
                )

                await message.delete()
            else:
                await message.edit(self.strings["no_voice_message"])
        else:
            await message.edit(self.strings["no_voice_message"])
