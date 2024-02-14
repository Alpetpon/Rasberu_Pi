import asyncio
import time
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import Update, User, Message
from datetime import datetime
from database.database import get_banned_id
from database import database as db
from config_data.config import Config, load_config
import os
import random

config: Config = load_config()

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
            time.sleep(40)
            raise asyncio.CancelledError()
        if len(self.messages) == 3:
            await data['event_update'].message.answer('Превышен лимит нажатий, подождите 5 минут.')
            time.sleep(300)
            self.messages = []
            raise asyncio.CancelledError()
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
        if banned_ids:
            if user_id in [i[0] for i in banned_ids]:
                await data['event_update'].message.answer('Вы забанены')
                raise asyncio.CancelledError()
        return await handler(event, data)

class GeneratorWords(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        this_user: User = data.get("event_from_user")
        user_id = this_user.id
        username = this_user.username
        text : Update = data.get('event_update')
        message_text = text.message.text
        current_time = datetime.now().isoformat()
        word = await db.select_word()
        if word != []:
            if message_text == word[0][0].rstrip():
                await data['event_update'].message.answer(r'Вы успешно зарегистрировались. Нажмите на /start')
                await db.add_user_to_users_table(str(user_id), username, 'User', 'User', current_time, '1,2')
                await data['bot'].send_message(chat_id = config.tg_bot.admin_id, text = f'Пользователь <B>{username}</B> зарегистрировался по ключу <B>{word[0][0].rstrip()}</B>')
                await db.delete_word()
                raise asyncio.CancelledError()
        return await handler(event, data)


class PersonLimitsMiddleware(BaseMiddleware):
    def __init__(self):
        self.limits = []

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        this_user: User = data.get("event_from_user")
        user_id = this_user.id
        text : Update = data.get('event_update')
        message_text = text.message.text
        current_time = datetime.now().second
        if message_text == 'Действие 1' or message_text == 'Действие 2':
            self.limits.append(message_text)
        limits = await db.select_limits(user_id)
        print(await db.select_limits(user_id))
        if len(self.limits) > int(limits[0][0]) and datetime.now().second - current_time < 10:
            await data['event_update'].message.answer(r'Вы превысили свой дневной лимит нажатий')
            raise asyncio.CancelledError()
        elif len(self.limits) > int(limits[0][1]) and datetime.now().second - current_time < 20:
            await data['event_update'].message.answer(r'Вы превысили свой месячный лимит нажатий')
        elif len(self.limits) > int(limits[0][2]) and datetime.now().second - current_time < 30:
            await data['event_update'].message.answer(r'Вы превысили свой годовой лимит нажатий')
            self.limits = []
            raise asyncio.CancelledError()
        return await handler(event, data)



