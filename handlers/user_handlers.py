from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_RU

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
@router.message(CommandStart())
async def process_start_command(message: Message):
    user_id = message.from_user.id
    await message.answer(LEXICON_RU[message.text])
    if user_id not in






# @dp.message_handler(commands=['start'])
# async def cmd_start(message: types.Message):
#     user_id = message.from_user.id
#
#     if user_id not in registered_users:
#         registered_users.add(user_id)
#         user_info[user_id] = {'comments': [], 'rights': 'user', 'clicks': 0, 'last_click_time': 0}
#
#         await message.answer("Бот работает только для зарегистрированных пользователей.")
#         await log_message(user_id, message.text)
#
#     await show_actions_keyboard(message)