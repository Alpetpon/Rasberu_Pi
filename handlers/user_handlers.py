from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from database import database as db
from keyboards import Keyboards as kb

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
@router.message(CommandStart())
async def process_start_command(message: Message):
    user_id = message.from_user.id

    # Проверяем, зарегистрирован ли пользователь в базе данных
    if not db.user_exists(user_id):
        # Регистрируем нового пользователя в базе данных
        db.add_user(user_id, message.from_user.username, "No comment")
        await message.answer("Бот работает только для зарегистрированных пользователей.")
        await log_message(user_id, message.text)

    await message.reply(text="ghbdtn", reply_markup=kb.main_keyboard)

async def log_message(user_id, action):
    db.add_log(user_id,db.get_username(user_id), action)

@router.message_handler(lambda message: message.text == "Действие 1")
async def action_1(message: Message):
    user_id = message.from_user.id
    await process_action(message, "Действие 1", user_id)


