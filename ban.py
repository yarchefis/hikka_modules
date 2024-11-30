import logging
from telethon.tl.functions.contacts import BlockRequest
from .. import loader  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class SimpleBanResponderMod(loader.Module):
    """Модуль для ответа, бана и удаления истории только у себя."""

    strings = {
        "name": "SimpleBanResponder",
        "response_message": "Личное общение не приветствуется."
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "whitelist", [
                263857209, 831408739, 1628112862, 1512882126, 1905781428, 
                8027906376, 5155780630, 1123987810, 5112436679, 1515756886, 
                5234377340, 1113636161, 1988845082, 6939483738, 5606889636, 
                388246260, 359373252, 6593286426, 651143395, 1336120316, 
                1230376051, 5142620829, 5857445517, 5731587578, 1219923771, 
                675929550, 6180493535
            ],  # Полный список user_id
            "Список user_id пользователей, которых нельзя блокировать"
        )

    async def client_ready(self, client, db):
        self.client = client
        logger.info("SimpleBanResponderMod загружен и готов к работе.")

    @loader.watcher(incoming=True, only_messages=True)
    async def watcher(self, message):
        if message.is_private and message.sender_id != (await self.client.get_me()).id:
            sender_id = message.sender_id

            # Проверяем, есть ли пользователь в вайтлисте
            if sender_id in self.config["whitelist"]:
                logger.info(f"Пользователь {sender_id} находится в вайтлисте. Пропускаем.")
                return

            logger.info(f"Получено сообщение от {sender_id}. Обрабатываю...")

            try:
                # Отправляем сообщение
                await message.reply(self.strings["response_message"])
                
                # Блокируем пользователя
                result = await self.client(BlockRequest(id=sender_id))
                logger.info(f"Пользователь {sender_id} заблокирован. Результат: {result}")
            except Exception as e:
                logger.error(f"Ошибка при обработке пользователя {sender_id}: {e}")
