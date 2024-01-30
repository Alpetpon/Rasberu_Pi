from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button1: KeyboardButton = KeyboardButton(text='1')
button2: KeyboardButton = KeyboardButton(text='2')
button3: KeyboardButton = KeyboardButton(text='3')

main_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button1], [button2], [button3]],
                                                          resize_keyboard=True)



