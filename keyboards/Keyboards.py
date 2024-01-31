from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button1: KeyboardButton = KeyboardButton(text='1')
button2: KeyboardButton = KeyboardButton(text='2')

main_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button1], [button2]],
                                                          resize_keyboard=True)

admin_button: KeyboardButton = KeyboardButton(text = "Admin")

admin_panel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button1], [button2], [admin_button]], resize_keyboard=True)


Append_user: KeyboardButton = KeyboardButton(text = "Append user")
admin_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard = [[Append_user]])
