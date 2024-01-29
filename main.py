import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from Token import token
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.webhook import SendMessage


logging.basicConfig(level=logging.INFO)

# Настройки базы данных SQLite
DATABASE_URL = 'sqlite:///mydatabase.db'


# Инициализация бота и диспетчера
bot = Bot(token=token)
dp = Dispatcher(bot)

# Массив для хранения зарегистрированных пользователей
registered_users = set()

# Словарь для хранения комментариев и прав пользователей
user_info = {}

# Параметры для лимитов нажатий и блокировки спама
click_limits = {
    'day': 10,
    'month': 50,
    'year': 200
}

spam_interval = 300  # 5 минут в секундах


# Команда для старта бота
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    if user_id not in registered_users:
        registered_users.add(user_id)
        user_info[user_id] = {'comments': [], 'rights': 'user', 'clicks': 0, 'last_click_time': 0}

        await message.answer("Бот работает только для зарегистрированных пользователей.")
        await log_message(user_id, message.text)

    await show_actions_keyboard(message)


# Функция для отображения клавиатуры с действиями
async def show_actions_keyboard(message: types.Message):
    user_id = message.from_user.id
    user_rights = user_info[user_id]['rights']

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user_rights == 'user':
        keyboard.add(types.KeyboardButton("Действие 1"), types.KeyboardButton("Действие 2"))
    elif user_rights == 'admin':
        keyboard.add(types.KeyboardButton("Действие 1"), types.KeyboardButton("Действие 2"),
                     types.KeyboardButton("Админка"))

    await message.answer("Выберите действие:", reply_markup=keyboard)


# Обработка действия 1
@dp.message_handler(lambda message: message.text == "Действие 1")
async def action_1(message: types.Message):
    user_id = message.from_user.id
    await process_action(message, "Действие 1", user_id)


# Обработка действия 2
@dp.message_handler(lambda message: message.text == "Действие 2")
async def action_2(message: types.Message):
    user_id = message.from_user.id
    await process_action(message, "Действие 2", user_id)


# Обработка админского действия
@dp.message_handler(lambda message: message.text == "Админка")
async def admin_panel(message: types.Message):
    user_id = message.from_user.id
    if user_info[user_id]['rights'] == 'admin':
        await show_admin_panel(message)
    else:
        await message.answer("У вас нет прав на выполнение этого действия.")


# Функция для обработки действия
async def process_action(message: types.Message, action: str, user_id: int):
    user_info[user_id]['clicks'] += 1

    if user_info[user_id]['clicks'] > click_limits['day']:
        await message.answer("Превышен дневной лимит действий.")
        return

    if user_info[user_id]['clicks'] > click_limits['month']:
        await message.answer("Превышен месячный лимит действий.")
        return

    if user_info[user_id]['clicks'] > click_limits['year']:
        await message.answer("Превышен годовой лимит действий.")
        return

    current_time = int(time.time())
    if current_time - user_info[user_id]['last_click_time'] < spam_interval:
        await message.answer("Вы слишком часто нажимаете кнопки. Подождите некоторое время.")
        return

    user_info[user_id]['last_click_time'] = current_time

    await message.answer(f"Вы выбрали: {action}")
    await log_message(user_id, f"Выбрано действие: {action}")


# Функция для отображения админской панели
async def show_admin_panel(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Все пользователи"))

    await message.answer("Выберите действие из админки:", reply_markup=keyboard)


# Функция для логирования сообщения в базу данных
async def log_message(user_id: int, text: str):
    # Здесь должен быть код для записи сообщения в базу данных (используйте SQLAlchemy или другую библиотеку)

    pass


if __name__ == '__main__':
    from aiogram import executor
    from aiogram.dispatcher.webhook import GetMe, SendBotStart

    # Установка соединения с базой данных
    # Здесь должен быть код для инициализации базы данных

    # Запуск бота
    loop = asyncio.get_event_loop()
    loop.create_task(dp.send_message(12345678, "/start"))  # Отправляем боту команду /start
    loop.create_task(dp.send_message(12345678, "/getme"))  # Получаем информацию о боте
    executor.start_polling(dp, skip_updates=True)
