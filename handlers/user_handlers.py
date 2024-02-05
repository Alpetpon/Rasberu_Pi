from datetime import datetime
from aiogram import F, Router, Bot
from aiogram.filters import  CommandStart, Command
from aiogram.types import Message
from database import database as db
from Token import *
from keyboards.Keyboards import create_standard_kb
from aiogram.types import ReplyKeyboardRemove
from lexicon.lexicon_ru import LEXICON_RU

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await db.create_database()
    await db.add_user_to_all_user_table(str(message.from_user.id), message.from_user.username)
    if message.from_user.id == admin_matvey_id:
        await message.answer(
            text=LEXICON_RU['admin_panel'],
            reply_markup=create_standard_kb(2, 'BUTTONS_USER1', 'BUTTONS_USER2', 'BUTTONS_ADMIN', 'Генерация слова', 'Все юзеры')
        )
        current_time = datetime.now().isoformat()
        await db.add_user_to_users_table(str(message.from_user.id), message.from_user.username, 'Admin', 'Administrator', current_time, '1,2')
    else:
        if message.from_user.username not in [i[0] for i in (await db.if_username_in_user_table())]:
            await message.answer(LEXICON_RU['no_admin_user'])
        else:
            all_info_about_user = await db.get_permissions_info_from_users(message.from_user.id)
            if all_info_about_user[0][-1] == '1,2':
                await message.answer(LEXICON_RU['yes_admin_user'],  reply_markup=create_standard_kb(2, 'BUTTONS_USER1', 'BUTTONS_USER2'))
            if all_info_about_user[0][-1] == '1':
                await message.answer(LEXICON_RU['yes_admin_user'],  reply_markup=create_standard_kb(2, 'BUTTONS_USER1'))
            if all_info_about_user[0][-1] == '2':
                await message.answer(LEXICON_RU['yes_admin_user'],  reply_markup=create_standard_kb(2, 'BUTTONS_USER2'))

@router.message(F.text == 'ADMIN')
async def process_username(message: Message):
    current_time = datetime.now().isoformat()
    await db.change_last_action_in_table_users(message.from_user.id, current_time)
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await message.answer('Напишите имя пользователя, комментарий, роль, и разрешения какие действия ему можно делать в формате: username/comment/role/1 или 2 или 1,2')


@router.message(F.text == 'Все юзеры')
async def response_all_users_button(message: Message):
    users = await db.all_info_about_users_button()
    for i in users:
        await message.answer(text = ', '.join(i))

@router.message(F.text == "Действие 1")
async def handler_button_1(message: Message):
    current_time = datetime.now().isoformat()
    await message.answer(f'Вы нажали на кнопку <b>Действие 1</b>')
    await db.change_last_action_in_table_users(message.from_user.id, current_time)
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)

@router.message(F.text == "Действие 2")
async def handler_button_2(message: Message):
    current_time = datetime.now().isoformat()
    await message.answer(f'Вы нажали на кнопку <b>Действие 2</b>')
    await db.change_last_action_in_table_users(message.from_user.id, current_time)
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)

@router.message(F.text)
async def append_user_to_user_table(message: Message):
    if '/' in message.text:
        username_comment_perms = message.text.split('/')
        current_time = datetime.now().isoformat()
        user_id_by_username = await db.get_user_id_from_all_users_table(username_comment_perms[0])
        await db.add_user_by_admin_to_user_table(user_id_by_username, username_comment_perms[0], username_comment_perms[1], username_comment_perms[2], current_time, username_comment_perms[3])
        await db.change_last_action_in_table_users(message.from_user.id, current_time)
        await message.answer(f"Пользователь {username_comment_perms[0]} успешно зарегистрирован.")
    else:
        current_time = datetime.now().isoformat()
        await db.change_last_action_in_table_users(message.from_user.id, current_time)
        await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
        await message.answer(f'Команды {message.text} не существует. \n\nНажмите на "/help" или "/main"')



