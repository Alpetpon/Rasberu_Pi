import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import user_handlers
from middlewares.middlewares import LimitsMiddleware, BannedUserResponse


# Функция конфигурирования и запуска бота
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
    user_handlers.router.message.middleware(LimitsMiddleware())
    user_handlers.router.message.middleware(BannedUserResponse())
    # Регистрируем роутеры в диспетчер
    dp.include_router(user_handlers.router)
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
