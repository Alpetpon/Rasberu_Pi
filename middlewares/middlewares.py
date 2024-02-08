import asyncio
import time
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import Update, User, Message
from datetime import datetime
from database.database import get_banned_id



class LimitsMiddleware(BaseMiddleware):
    def __init__(self):
        self.messages = []

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        this_user: User = data.get("event_from_user")
        text : Update = data.get('event_update')
        message_text = text.message.text
        if message_text == 'Действие 1' or message_text == 'Действие 2':
            self.messages.append(datetime.now().second)
        if len(self.messages) == 2:
            await data['event_update'].message.answer('Превышен лимит нажатий, подождите 40 секунд.')
            time.sleep(5)
        if len(self.messages) == 3:
            await data['event_update'].message.answer('Превышен лимит нажатий, подождите 5 минут.')
            time.sleep(10)
            self.messages = []
        return await handler(event, data)

class BannedUserResponse(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        this_user: User = data.get("event_from_user")
        user_id = this_user.id
        banned_ids = await get_banned_id()
        print(banned_ids)
        print(user_id)
        if user_id in [i[0] for i in banned_ids]:
            await data['event_update'].message.answer('Вы забанены')
            raise asyncio.CancelledError()
        return await handler(event, data)

