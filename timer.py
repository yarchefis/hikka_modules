import logging
import asyncio
from datetime import timedelta, datetime
from telethon import events
from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class TimerMod(loader.Module):
    """Модуль для запуска таймера."""

    strings = {
        "name": "TimerMod",
        "invalid_time_format": "⚠️ Неправильный формат времени. Используйте формат .timer ЧЧ:ММ:СС",
        "time_up": "⏰ Время вышло!"
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def timercmd(self, message):
        """Запускает таймер. Использование: .timer ЧЧ:ММ:СС"""
        args = utils.get_args_raw(message)
        try:
            hours, minutes, seconds = map(int, args.split(":"))
            timer_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            await message.edit(self.strings["invalid_time_format"])
            return

        end_time = datetime.now() + timer_duration

        while datetime.now() < end_time:
            remaining_time = end_time - datetime.now()
            await message.edit(f"⏳ Осталось времени: {str(remaining_time).split('.')[0]}")  # Отображаем без микросекунд
            await asyncio.sleep(5)

        await message.edit(self.strings["time_up"])
