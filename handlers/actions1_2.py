import time
from datetime import datetime
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from database import database as db
from config_data.config import Config, load_config
from keyboards.Keyboards import create_standard_kb
from keyboards.inline_keyboard import create_inline_kb
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncio
import random
import os


router = Router()
#Вот здесь нужно вставить код для работы кнопки действие 1, т.е чтоб выполнялся скрипт rasberu pi
@router.message(F.text == "Действие 1")
async def handler_button_1(message: Message):
    current_time = datetime.now().isoformat()
    await db.down_limits(message.from_user.id)
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    await message.answer('Кнопка отвечает за действие 1')


#Вот здесь нужно вставить код для работы кнопки действие 2, т.е чтоб выполнялся скрипт rasberu pi
@router.message(F.text == "Действие 2")
async def handler_button_2(message: Message):
    current_time = datetime.now().isoformat()
    await db.down_limits(message.from_user.id)
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    await message.answer(f'Кнопка отвечает за действие 2')