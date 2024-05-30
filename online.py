from .. import loader
from asyncio import sleep

@loader.tds
class OnlineMod(loader.Module):
    """Вечный онлайн."""
    strings = {'name': 'Online'}

    async def client_ready(self, client, db):
        self.db = db

    async def onlinecmd(self, message):
        """Включить вечный онлайн."""
        if not self.db.get("Eternal Online", "status"):
            self.db.set("Eternal Online", "status", True)
            await message.edit("Вечный онлайн включен.")
            while self.db.get("Online", "status"):
                await message.client(__import__("telethon").functions.account.UpdateStatusRequest(offline=False))
                await sleep(40)

        else:
            self.db.set("Online", "status", False)
            await message.edit("Вечный онлайн выключен.")