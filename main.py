from aiogram import executor
from loguru import logger

from handlers.admin_handlers.admin_headlers import send_data_as_excel_handler
from handlers.user_handlers.my_details_handlers import register_my_details_handler
from handlers.user_handlers.user_handlers import greeting_handler
from system.dispatcher import dp

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


def main() -> None:
    """Запуск бота https://t.me/TeaBetNY_bot"""
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as error:
        logger.exception(error)

    greeting_handler()  # Пост приветствие
    register_my_details_handler()  # Мои данные
    send_data_as_excel_handler()


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        logger.exception(e)
