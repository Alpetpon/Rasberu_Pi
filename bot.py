import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import user_handlers, actions1_2, other_commands
from middlewares.middlewares import BannedUserResponse, GeneratorWords, PersonLimitsMiddleware, LimitsMiddleware
from database import database as db
# Функция конфигурирования и запуска бота



async def start_bot(bot: Bot):
    await db.create_users()
    await db.create_logs()
    await db.create_all_users()
    await db.create_banned()
    await db.create_reg_word()
    await db.create_antiflood_table()
    await db.create_antiflood5_table()
    await db.delete_all_from_antiflood()
    await db.delete_all_from_antiflood5()
    await db.delete_word()


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
      level=logging.DEBUG,
      format='%(filename)s:%(lineno)d #%(levelname)-8s '
             '[%(asctime)s] - %(name)s - %(message)s')

    # Инициализируем логгер
    logger = logging.getLogger(__name__)

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')

    dp = Dispatcher()

    # Настраиваем главное меню бота
    await set_main_menu(bot)
    user_handlers.router.message.middleware(BannedUserResponse())
    user_handlers.router.message.middleware(GeneratorWords())
    dp.message.middleware.register(LimitsMiddleware())
    actions1_2.router.message.middleware(PersonLimitsMiddleware())
    # Регистрируем роутеры в диспетчер
    # dp.include_router(user_handlers.router)
    dp.include_routers(user_handlers.router, actions1_2.router, other_commands.router)
    dp.startup.register(start_bot)
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
