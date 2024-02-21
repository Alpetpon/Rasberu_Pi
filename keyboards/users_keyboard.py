from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import database as db



def get_keyboard_fab(users):
    builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for i in range(len(users)):
        buttons.append(InlineKeyboardButton(text = f'Показать {users[i][1]}', callback_data = f'Показать {users[i][1]}'))
    builder.row(*buttons, width=1)
    return builder.as_markup()

