from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from database import database as db
from keyboards import Keyboards as kb
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Token import *

router = Router()


class Bot(StatesGroup):
    start = State()
    push_1 = State()
    push_2 = State()


# Этот хэндлер будет срабатывать на команду "/start" -
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if message.from_user.id == int(admin_alex_id):
        await message.answer(
            "Вы авторизовались как администратор!",
            reply_markup=kb.admin_panel
        )
        await state.set_state(Bot.admin_panel)
    else:
        await message.answer(text.greet.format(
            name=message.from_user.full_name),
            reply_markup=kb.start_keyboard
        )

    # Проверяем, зарегистрирован ли пользователь в базе данных
    if not db.user_exists(user_id):
        # Регистрируем нового пользователя в базе данных
        db.add_user(user_id, message.from_user.username, "No comment")
        await message.answer("Бот работает только для зарегистрированных пользователей.")
        await log_message(user_id, message.text)

    await state.set_state(Bot.start)
    await message.answer(reply_markup=kb.main_keyboard)

async def log_message(user_id, action):
    db.add_log(user_id,db.get_username(user_id), action)

@router.message_handler(lambda message: message.text == "Действие 1")
async def action_1(message: Message):
    await message.answer(text='Вы перешли в Действие 1')
    await state.set_state(Bot.push_1)


