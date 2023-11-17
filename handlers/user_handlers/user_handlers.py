from aiogram import types
from aiogram.dispatcher import FSMContext  # Состояния пользователя
from loguru import logger  # Логирование с помощью loguru

from keyboards.user_keyboards import create_greeting_keyboard  # Клавиатуры поста приветствия
from system.dispatcher import dp, bot  # Подключение к боту и диспетчеру пользователя
import sqlite3


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    try:
        # Получаем информацию о пользователе
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        join_date = message.date.strftime("%Y-%m-%d %H:%M:%S")
        # Записываем информацию о пользователе в базу данных
        conn = sqlite3.connect("your_database.db")  # Замените "your_database.db" на имя вашей базы данных
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users_start (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT, join_date TEXT)''')
        cursor.execute("INSERT OR REPLACE INTO users_start (user_id, username, first_name, last_name, join_date) "
                       "VALUES (?, ?, ?, ?, ?)", (user_id, username, first_name, last_name, join_date))
        conn.commit()
        conn.close()
        logger.info(f"Пользователь нажавший /start: {user_id}, {username}, {first_name}, {last_name}, {join_date}")
        await state.finish()  # Завершаем текущее состояние машины состояний
        await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию
        from_user_name = message.from_user.first_name  # Получаем фамилию пользователя
        greeting_post = f"{from_user_name}, Вас приветствует чат-бот 🤖 @TeaBetNY_bot"
        keyboards_greeting = create_greeting_keyboard()  # Клавиатуры поста приветствия 👋
        await message.answer(greeting_post, reply_markup=keyboards_greeting,
                             parse_mode=types.ParseMode.HTML)  # Текст в HTML-разметки
    except Exception as error:
        logger.exception(error)


@dp.callback_query_handler(lambda c: c.data == "disagree")
async def disagree_handler(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await state.finish()  # Завершаем текущее состояние машины состояний
        await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию
        from_user_name = callback_query.from_user.first_name  # Получаем фамилию пользователя
        greeting_message = f"{from_user_name}, Вас приветствует чат-бот"
        keyboards_greeting = create_greeting_keyboard()  # Клавиатуры поста приветствия 👋
        await bot.send_message(callback_query.from_user.id,  # ID пользователя
                               caption=greeting_message,  # Текст для приветствия 👋
                               reply_markup=keyboards_greeting,  # Клавиатура приветствия 👋
                               parse_mode=types.ParseMode.HTML)  # Текст в HTML-разметки
    except Exception as error:
        logger.exception(error)


def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(greeting)  # Обработчик команды /start, он же пост приветствия 👋
    dp.register_message_handler(disagree_handler)
