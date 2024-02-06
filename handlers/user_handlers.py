from datetime import datetime
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from database import database as db
from config_data.config import Config, load_config
from keyboards.Keyboards import create_standard_kb
from keyboards.inline_keyboard import create_inline_kb
from aiogram.types import ReplyKeyboardRemove
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


router = Router()
config: Config = load_config()

class CnangeComment(StatesGroup):
    comment = State()



@router.message(CommandStart())
async def process_start_command(message: Message):
    current_time = datetime.now().isoformat()
    await db.create_database()
    await db.add_user_to_all_user_table(str(message.from_user.id), message.from_user.username)
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    if message.from_user.id == int(config.tg_bot.admin_id):
        await message.answer(
            text=LEXICON_RU['admin_panel'],
            reply_markup=create_standard_kb(2, 'BUTTONS_USER1', 'BUTTONS_USER2', 'BUTTONS_ADMIN',
                                            'BUTTONS_WORD_GENERATION', 'BUTTONS_ALL_USERS')
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
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    await message.answer(LEXICON_RU['waiting_for_username'],
                         reply_markup=ReplyKeyboardRemove())


@router.message(F.text == 'ВСЕ ПОЛЬЗОВАТЕЛИ')
async def response_all_users_button(message: Message):
    current_time = datetime.now().isoformat()
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    users = await db.all_info_about_users_button()
    for i in users:
        await message.answer(
            text=f'<b>User_id</b>: {i[0]} \n <b>Username</>: {i[1]} \n <b>Comment</>: {i[2]} \n <b>Role</b>: {i[3]} \n <b>Daily limit</b>: {i[4]} \n <b>Monthly limit</b>: {i[5]} \n <b>Yearly limit</b>: {i[6]} \n <b>Last action</b>: {i[7]} \n <b>Permissions</b>: {i[8]}',
            reply_markup=create_inline_kb(1, f'Изменить комментарий у {i[1]}', 'Изменить роль', 'Изменить лимиты'))


@router.message(F.text == "Действие 1")
async def handler_button_1(message: Message):
    current_time = datetime.now().isoformat()
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    await message.answer(f'Кнопка отвечает за действие 1')


@router.message(F.text == "Действие 2")
async def handler_button_2(message: Message):
    current_time = datetime.now().isoformat()
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await db.change_last_action_in_users_table(message.from_user.id, current_time)
    await message.answer(f'Кнопка отвечает за действие 2')

@router.callback_query(StateFilter(None), F.data == 'Изменить комментарий')
async def command_response(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите новый комментарий')
    await state.set_state(CnangeComment.comment)

@router.message(CnangeComment.comment, F.text)
async def user_id_entered(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    print(data)
    await message.answer(text = data['comment'])
    await state.clear()

@router.message(F.text)
async def append_user_to_user_table(message: Message):
    current_time = datetime.now().isoformat()
    if '/' in message.text:
        username_comment_perms = message.text.split('/')
        await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
        user_id_by_username = await db.get_user_id_from_all_users_table(username_comment_perms[0])
        await db.add_user_by_admin_to_user_table(user_id_by_username, username_comment_perms[0],
                                                 username_comment_perms[1], username_comment_perms[2],
                                                 current_time, username_comment_perms[3])
        await message.answer(f"Пользователь {username_comment_perms[0]} успешно зарегистрирован.")
    else:
        await message.answer(text=f'Команда {message.text} не распознана')
        await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
        await db.change_last_action_in_users_table(message.from_user.id, current_time)а
