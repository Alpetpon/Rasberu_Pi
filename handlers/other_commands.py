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

@router.message(F.text)
async def other_comms(message: Message):
    await message.answer(f'Команда {message.text} не поддерживается')