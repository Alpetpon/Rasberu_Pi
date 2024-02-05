from datetime import datetime

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import database as db


from config_data.config import Config, load_config
from keyboards.Keyboards import create_standard_kb
from aiogram.types import ReplyKeyboardRemove
from lexicon.lexicon_ru import LEXICON_RU

router = Router()
config: Config = load_config()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await db.create_database()
    await db.add_user_to_all_user_table(str(message.from_user.id), message.from_user.username)
    if message.from_user.id == config.tg_bot.admin_id:
        await message.answer(
            text=LEXICON_RU['admin_panel'],
            reply_markup=create_standard_kb(2, 'BUTTONS_USER1', 'BUTTONS_USER2', 'BUTTONS_ADMIN',
                                            'BUTTONS_WORD_GENERATION', 'BUTTONS_ALL_USERS')
        )
        current_time = datetime.now().isoformat()
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
    await message.answer(LEXICON_RU['waiting_for_username'],
                         reply_markup=ReplyKeyboardRemove())


@router.message(F.text == 'ВСЕ ПОЛЬЗОВАТЕЛИ')
async def response_all_users_button(message: Message):
    users = await db.all_info_about_users_button()
    for i in users:
        await message.answer(text=', '.join(i))


@router.message(F.text)
async def append_user_to_user_table(message: Message):
    if '/' in message.text:
        username_comment_perms = message.text.split('/')
        current_time = datetime.now().isoformat()
        user_id_by_username = await db.get_user_id_from_all_users_table(username_comment_perms[0])
        await db.add_user_by_admin_to_user_table(user_id_by_username, username_comment_perms[0],
                                                 username_comment_perms[1], username_comment_perms[2],
                                                 current_time, username_comment_perms[3])
        await message.answer(f"Пользователь {username_comment_perms[0]} успешно зарегистрирован.")


# Обработчик для кнопки "Действие 1"
# @router.message(F.text == "Действие 1")
# async def handler_button_1(message: Message):
#     await message.answer(f'Кнопка отвечает за действие 1')


# # Обработчик для кнопки "Действие 2"
# @router.message(F.text == "Действие 2")
# async def handler_button_2(message: Message):
#     await message.answer(f'Кнопка отвечает за действие 2')
