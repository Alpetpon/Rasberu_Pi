import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import Update, User

class LimitsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        this_user: User = data.get("event_from_user")
        text : Update = data.get('event_update')
        user_id = int(this_user.id)
        username = this_user.username
        message = text.message.text
        return await handler(event, data)