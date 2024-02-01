from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from database import database as db
from keyboards import Keyboards as kb
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from Token import *
from keyboards.Keyboards import create_standard_kb
from aiogram.types import ReplyKeyboardRemove
from lexicon.lexicon_ru import LEXICON_RU

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
            text=LEXICON_RU['admin_panel'],
            reply_markup=create_standard_kb(2, 'BUTTONS_USER1', 'BUTTONS_USER2', 'BUTTONS_ADMIN')
        )
        username = message.from_user.username
        if not db.user_exists(user_id):
            db.add_user(user_id, username, "Admin_Start")

        await log_message(user_id, message.text, username=username)
        await state.set_state(Bot.admin_panel)
    else:
        username = message.from_user.username
        if not db.user_exists(username):
            await message.answer(LEXICON_RU['no_admin_user'])
            await log_message(user_id, message.text, username=username)
            await state.set_state(Bot.no_admin_user)
        else:
            db.add_user(user_id, username, "No comment")
            await message.answer(LEXICON_RU['yes_admin_user'])
            await state.set_state(Bot.yes_admin_user)

    await state.set_state(Bot.start)
    await message.answer(reply_markup=create_standard_kb(2, 'BUTTONS_USER1', 'BUTTONS_USER2'))


async def log_message(user_id, action):
    db.add_log(user_id,db.get_username(user_id), action)


@router.message(F.text == "Admin")
async def Admin_panel(message: Message):
    if message.from_user.id == int(admin_alex_id):
        await message.answer("Admin", reply_markup=create_standard_kb(2, 'BUTTONS_USER1', 'BUTTONS_USER2'))


@router.message(F.text == "ADMIN")
async def Admin_Append(message: Message , state: FSMContext):
    await message.answer(text=LEXICON_RU['waiting_for_username'],
                         reply_markup=ReplyKeyboardRemove())
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


# Обработчик для кнопки "Действие 1"
@router.message(F.text == "Действие 1")
async def handler_button_1(message: Message, state: FSMContext):
    await message.answer(f'аоаооаоаоаоа213412312')


# Обработчик для кнопки "Действие 2"
@router.message(F.text == "Действие 2")
async def handler_button_2(message: Message, state: FSMContext):
    await message.answer(f'аоаооаоаоаоа')
