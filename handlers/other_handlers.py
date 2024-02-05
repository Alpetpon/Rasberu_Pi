from aiogram import Router
from aiogram.types import Message
from database import database as db
from datetime import datetime
from aiogram import F, Router, Bot


router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message(F)
async def send_echo(message: Message):
    current_time = datetime.now().isoformat()
    await db.add_logs(message.from_user.id, message.from_user.username, message.text, current_time)
    await message.answer(f'Команды {message.text} не существует. \n\nНажмите на "/help" или "/main"')
