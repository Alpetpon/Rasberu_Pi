from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from database import database as db
from keyboards import Keyboards as kb
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from Token import *

router = Router()


class Bot(StatesGroup):
    start = State()
    admin_panel = State()
    no_admin_user = State()
    yes_admin_user = State()
    waiting_for_username = State()
    push_1 = State()
    push_2 = State()

@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.from_user.id == int(admin_alex_id):
        await message.answer(
            "Вы авторизовались как администратор!",
            reply_markup=kb.admin_panel
        )
        username = message.from_user.username
        if not db.user_exists(user_id):
            db.add_user(user_id, username, "Admin_Start")

        await log_message(user_id, message.text, username=username)
        await state.set_state(Bot.admin_panel)
    else:
        username = message.from_user.username
        if not db.user_exists(username):
            await message.answer("Бот работает только для зарегистрированных пользователей.")
            await log_message(user_id, message.text, username=username)
            await state.set_state(Bot.no_admin_user)
        else:
            db.add_user(user_id, username, "No comment")
            await message.answer("Что-то типо добро пожаловать")
            await state.set_state(Bot.yes_admin_user)

    await state.set_state(Bot.start)
    await message.answer(reply_markup=kb.main_keyboard)


async def log_message(user_id, action):
    db.add_log(user_id,db.get_username(user_id), action)

@router.message(F.text == "Admin")
async def Admin_panel(message: Message):
    if message.from_user.id == int(admin_alex_id):
        await message.answer("Admin", reply_markup=kb.admin_keyboard)

@router.message(F.text == "Append user")
async def Admin_Append(message: Message , state: FSMContext):
    await message.answer("Введите ник пользователя, которого вы хотите зарегистрировать.")
    await state.set_state(Bot.waiting_for_username)

@router.message(StateFilter(Bot.waiting_for_username))
async def process_username(message: Message, state: FSMContext):
    username = message.text

    # Добавить пользователя в базу данных
    user_id = 1
    comment = f"Добавлен через админскую команду"

    db.add_user(user_id, username, comment)

    await message.answer(f"Пользователь {username} успешно зарегистрирован.")

    await state.set_state(Bot.admin_panel)


