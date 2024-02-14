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
config: Config = load_config()

class CnangeComment(StatesGroup):
    username = State()
    comment = State()

class CnangeRole(StatesGroup):
    username = State()
    role = State()

class CnangeLimits(StatesGroup):
    username = State()
    daily_limit = State()
    monthly_limit = State()
    yearly_limit = State()

@router.message(CommandStart())
async def process_start_command(message: Message):
    current_time = datetime.now().isoformat()
    await db.create_users()
    await db.create_logs()
    await db.create_all_users()
    await db.create_banned()
    await db.create_reg_word()
    time.sleep(3)
    await db.add_user_to_all_user_table(str(message.from_user.id), message.from_user.username)
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    if message.from_user.id == int(config.tg_bot.admin_id):
        await message.answer(
            text=LEXICON_RU['admin_panel'],
            reply_markup=create_standard_kb(2, 'BUTTONS_USER1', 'BUTTONS_USER2', 'BUTTONS_ADMIN',
                                             'BUTTONS_ALL_USERS', 'Генерация фразы')
        )
        await db.add_user_to_users_table(str(message.from_user.id),
                                         message.from_user.username, 'Admin', 'Administrator', current_time, '1,2')
    else:
        if message.from_user.username not in [i[0] for i in (await db.if_username_in_user_table())]:
            await message.answer(LEXICON_RU['no_admin_user'])
        else:
            all_info_about_user = await db.get_permissions_info_from_users(message.from_user.id)
            if all_info_about_user[0][-1] == '1,2':
                await message.answer(LEXICON_RU['yes_admin_user'],
                                     reply_markup=create_standard_kb(2, 'BUTTONS_USER1', 'BUTTONS_USER2'))
            if all_info_about_user[0][-1] == '1':
                await message.answer(LEXICON_RU['yes_admin_user'],
                                     reply_markup=create_standard_kb(2, 'BUTTONS_USER1'))
            if all_info_about_user[0][-1] == '2':
                await message.answer(LEXICON_RU['yes_admin_user'],
                                     reply_markup=create_standard_kb(2, 'BUTTONS_USER2'))

@router.message(F.text == 'ADMIN')
async def process_username(message: Message):
    current_time = datetime.now().isoformat()
    await db.add_logs(int(message.from_user.id), message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    await message.answer(LEXICON_RU['waiting_for_username'])


@router.message(F.text == 'Все пользователи')
async def response_all_users_button(message: Message):
    current_time = datetime.now().isoformat()
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    users = await db.all_info_about_users_button()
    for i in users:
        await message.answer(
            text=f'<b>User_id</b>: {i[0]} \n <b>Username</>: {i[1]} \n <b>Comment</>: {i[2]} \n <b>Role</b>: {i[3]} \n <b>Daily limit</b>: {i[4]} \n <b>Monthly limit</b>: {i[5]} \n <b>Yearly limit</b>: {i[6]} \n <b>Last action</b>: {i[7]} \n <b>Permissions</b>: {i[8]}',
            reply_markup=create_inline_kb(1, f'Изменить комментарий у {i[1]}', f'Изменить роль у {i[1]}', f'Изменить лимиты у {i[1]}', f'Удалить и заблокировать {i[1]}'))


#Вот здесь нужно вставить код для работы кнопки действие 1, т.е чтоб выполнялся скрипт rasberu pi
@router.message(F.text == "Действие 1")
async def handler_button_1(message: Message):
    current_time = datetime.now().isoformat()
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    await message.answer(f'Кнопка отвечает за действие 1')


#Вот здесь нужно вставить код для работы кнопки действие 2, т.е чтоб выполнялся скрипт rasberu pi
@router.message(F.text == "Действие 2")
async def handler_button_2(message: Message):
    current_time = datetime.now().isoformat()
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    await message.answer(f'Кнопка отвечает за действие 2')

@router.callback_query(StateFilter(None), F.data.contains('Изменить комментарий'))
async def command_response(callback: CallbackQuery, state: FSMContext):
    username = callback.data.replace('Изменить комментарий у ', '')
    await state.update_data(username=username)
    await callback.message.answer('Введите новый комментарий')
    await state.set_state(CnangeComment.comment)

@router.message(CnangeComment.comment, F.text)
async def user_id_entered(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    username = data["username"]
    comment = data['comment']
    await db.change_comment_in_table_users(username, comment)
    await message.answer(text = f'У {data["username"]} обновлен комментарий: {data["comment"]}')
    await state.clear()

@router.callback_query(StateFilter(None), F.data.contains('Изменить роль'))
async def change_role(callback: CallbackQuery, state: FSMContext):
    username = callback.data.replace('Изменить роль у ', '')
    await state.update_data(username=username)
    await callback.message.answer('Введите роль')
    await state.set_state(CnangeRole.role)

@router.message(CnangeRole.role, F.text)
async def role_entered(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    data = await state.get_data()
    username = data["username"]
    role = data['role']
    await db.change_role_in_table_users(username, role)
    await message.answer(text = f'У {data["username"]} обновлена роль: {data["role"]}')
    await state.clear()

@router.callback_query(StateFilter(None), F.data.contains('Изменить лимиты'))
async def change_role(callback: CallbackQuery, state: FSMContext):
    username = callback.data.replace('Изменить лимиты у ', '')
    await state.update_data(username=username)
    await callback.message.answer('Введите дневной лимит')
    await state.set_state(CnangeLimits.daily_limit)

@router.message(CnangeLimits.daily_limit, F.text)
async def role_entered(message: Message, state: FSMContext):
    await state.update_data(daily_limit=message.text)
    await message.answer('Введите месячный лимит')
    await state.set_state(CnangeLimits.monthly_limit)

@router.message(CnangeLimits.monthly_limit, F.text)
async def role_entered(message: Message, state: FSMContext):
    await state.update_data(monthly_limit=message.text)
    await message.answer('Введите годовой лимит')
    await state.set_state(CnangeLimits.yearly_limit)

@router.message(CnangeLimits.yearly_limit, F.text)
async def role_entered(message: Message, state: FSMContext):
    await state.update_data(yearly_limit=message.text)
    data = await state.get_data()
    print(data)
    await db.change_limits_in_table_users(data['username'], data['daily_limit'], data['monthly_limit'], data['yearly_limit'])
    await message.answer(f'У пользователя {data["username"]} изменены лемиты: \n <b>дневной:</b> {data["daily_limit"]} \n <b>месячный:</b> {data["monthly_limit"]} \n <b>годовой:</b> {data["yearly_limit"]}')
    await state.clear()

@router.callback_query(F.data.contains('Удалить и заблокировать'))
async def delete_user(callback: CallbackQuery):
    username = callback.data.replace('Удалить и заблокировать ', '')
    print(username)
    await db.add_banned_user(username)
    await db.delete_user(username)
    await callback.message.answer('Пользователь удален и заблокирован')

@router.message(F.text.contains('/'))
async def append_user_to_user_table(message: Message):
    current_time = datetime.now().isoformat()
    username_comment_perms = message.text.split('/')
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    user_id_by_username = await db.get_user_id_from_all_users_table(username_comment_perms[0])
    await db.add_user_by_admin_to_user_table(user_id_by_username, username_comment_perms[0],
                                                 username_comment_perms[1], username_comment_perms[2],
                                                 current_time, username_comment_perms[3])
    await message.answer(f"Пользователь {username_comment_perms[0]} успешно зарегистрирован.")

@router.message(F.text == 'Генерация фразы')
async def change_role(message: Message):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '../middlewares/russian.txt')
    with open(file_path, mode = 'r') as file:
        random_line = random.choice(file.readlines())
    words = await db.select_word()
    if words == []:
        await db.add_reg_word(word=random_line)
    else:
        await db.update_word(random_line)
    await message.answer(f'Слово для регистрации: <b>{random_line}</b>')

@router.message(F.text)
async def musor(message:Message):
    await message.answer(f'Команда <b>{message.text}</b> не поддерживается')
