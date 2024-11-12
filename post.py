import random
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDiscussionMessageRequest
from telethon.tl.types import InputPeerChannel
from .. import loader, utils

@loader.tds
class CommentNewPostsMod(loader.Module):
    """Модуль для комментирования новых постов в канале"""

    strings = {"name": "CommentNewPosts"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.target_channel_username = 'yarchefis_channel'  # Юзернейм целевого канала

        # Получаем информацию о канале
        self.channel_entity = await client.get_entity(self.target_channel_username)
        self.channel_id = self.channel_entity.id

        # Массив фраз для комментариев
        self.comments = [
            "Ну и кто теперь тут первый 😎",
            "Заходи не бойся, выходи не плачь :3",
            "Автор ничего не постил уже 1 секунду, всё ясно, скатился :3",
            "Хищник на страже порядке",
            "Постим, живем :3",
            "Ладно",
            "Пока ты читаешь, я уже коммент оставил! Успевай 😈",
            "Кто на чем пишет? Я вот на assembler :3",
            "Хищник на месте 😎",
            "Нулевой тутб :3",
            "Минутка полезной инфы. Сейчас принято считать, что 1МБ = 1000КБ. А 1МиБ = 1024 КиБ. Живи с этим.",
            "С великой силой приходит великая безответственность.",
            "Где-то однажды появился на свет\nС лаем и мяуканьем зверь, каких нет\nИ тут же сбежал, оставив вопрос,\nСобаче-кошачий малыш Котопес\nКотопес, котопес ...\nЕдинственный в мире малыш котопес.",
            "Его не признали в городе родном\nИ все его шпыняют и ночью и днем\nНе стоит огорчаться, не стоит робеть\nА лучше эту песенку вместе пропеть Котопес, котопес,\nЕдинственный в мире малыш котопес!",
            "Есть программисты, а есть ЖСеры пхпхпх"
        ]

    @loader.watcher(incoming=True, chats='yarchefis_channel')
    async def watcher(self, message):
        # Проверяем, что сообщение новое и является постом в канале
        if message.is_channel and message.to_id.channel_id == self.channel_id and not message.out:
            try:
                # Получаем обсуждение поста (комментарии)
                discussion = await self.client(GetDiscussionMessageRequest(
                    peer=InputPeerChannel(self.channel_id, self.channel_entity.access_hash),
                    msg_id=message.id
                ))

                # Выбираем случайную фразу
                comment = random.choice(self.comments)

                # Отправляем комментарий к посту
                await self.client.send_message(
                    entity=discussion.messages[0].to_id,
                    message=comment,
                    reply_to=discussion.messages[0].id
                )
            except Exception as e:
                self.log.error(f"Failed to comment on post: {e}")
