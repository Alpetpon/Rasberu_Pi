import asyncio
import time
import datetime
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import Update, User, Message
from database.database import get_banned_id
from database import database as db
from config_data.config import Config, load_config
from keyboards.Keyboards import create_standard_kb
from aiogram.types import ReplyKeyboardRemove
import random
import calendar


config: Config = load_config()
class LimitsMiddleware(BaseMiddleware):
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
        if message_text == 'Действие 1' or message_text ==  'Действие 2':
            await db.add_user_to_antiflood_table(user_id, datetime.datetime.now().second + datetime.datetime.now().minute * 60)
            times = await db.select_time_from_antiflood(user_id)
            if times:
                if len(times) == 1:
                    await handler(event, data)
                    await event.answer('Следующее нажатие возможно через 40 секунд')
                else:
                    if int(times[-1][0]) - int(times[0][0]) <= 40:
                        return
                    else:
                        await db.add_user_to_antiflood5_table(user_id, datetime.datetime.now().second + datetime.datetime.now().minute * 60)
            times5 = await db.select_time_from_antiflood5(user_id)
            if times5:
                if len(times5) == 1:
                    await handler(event, data)
                    await event.answer('Слудующее нажатие возможно через 5 минут')
                else:
                    if int(times5[-1][0]) - int(times5[0][0]) <= 300:
                        return
                    else:
                        await handler(event, data)
                        await event.answer('Следующее нажатие возможно через 40 секунд')
                        await db.delete_user_from_antiflood(user_id)
                        await db.delete_user_from_antiflood5(user_id)
                        await db.add_user_to_antiflood_table(user_id, datetime.datetime.now().second + datetime.datetime.now().minute * 60)
        else:
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
        if banned_ids != []:
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
        current_time = datetime.datetime.now().isoformat()
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
        limits = await db.select_limits(user_id)
        def_limits = await db.def_limits(user_id)
        if int(limits[0][0]) == 0 and limits[0][1] != 0 and limits[0][2] != 0:
            now = datetime.datetime.now() # Получаем текущую дату и время
            end_of_day = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1) # Получаем полночь следующего дня
            seconds_until_end_of_day = (end_of_day - now).total_seconds() # Вычисляем разницу во времени между текущим моментом и концом текущих суток в секундах
            await data['event_update'].message.answer(r'Вы превысили свой дневной лимит нажатий')
            await asyncio.sleep(seconds_until_end_of_day)
            if def_limits[0][0] >= limits[0][1]:
                await db.if_d_l_more_m_l(user_id)
            else:
                await db.update_d_limit(user_id)
            raise asyncio.CancelledError()
        elif limits[0][1] == 0 and limits[0][0] == 0 and limits[0][2] != 0:
            now = datetime.datetime.now()            # Определяем последний день текущего месяца
            last_day_of_month = calendar.monthrange(now.year, now.month)[1] # Определяем последний день текущего месяца
            end_of_month = datetime.datetime(now.year, now.month, last_day_of_month)             # Получаем дату и время конца текущего месяца
            seconds_until_end_of_month = (end_of_month - now).total_seconds()            # Вычисляем разницу во времени между текущим временем и концом текущего месяца в секундах
            await data['event_update'].message.answer(r'Вы превысили свой месячный лимит нажатий')
            await asyncio.sleep(seconds_until_end_of_month)
            if def_limits[0][1] >= limits[0][2]:
                await db.if_m_l_more_y_l(user_id)
            else:
                await db.update_m_limit(user_id)
            raise asyncio.CancelledError()
        if limits[0][0] == 0 and limits[0][1] == 0 and limits[0][2] == 0:
            now = datetime.datetime.now()             # Получаем текущую дату и время
            end_of_year = datetime.datetime(now.year + 1, 1, 1)            # Получаем дату и время полуночи 1 января следующего года
            seconds_until_end_of_year = (end_of_year - now).total_seconds()             # Вычисляем разницу во времени между текущим моментом и концом года в секундах
            await data['event_update'].message.answer(r'Вы превысили свой годовой лимит нажатий')
            await asyncio.sleep(seconds_until_end_of_year)
            await db.update_d_limit(user_id)
            await db.update_m_limit(user_id)
            await db.update_y_limit(user_id)
            raise asyncio.CancelledError()
        print(limits)
        return await handler(event, data)
