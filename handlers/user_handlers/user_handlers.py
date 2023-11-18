import logging
import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup
from loguru import logger  # Логирование с помощью loguru

from keyboards.user_keyboards import create_greeting_keyboard, subscription_keyboard  # Клавиатуры поста приветствия
from system.dispatcher import dp, bot  # Подключение к боту и диспетчеру пользователя


# Команда для добавления канала в базу данных
class SomeState(StatesGroup):
    AddingChannel = State()
    RemovingChannel = State()


def read_channels_from_database():
    try:
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()
        # Execute a SELECT query to fetch all channel usernames
        cursor.execute("SELECT channel_username FROM channels")
        rows = cursor.fetchall()
        # Extract the channel usernames from the fetched rows
        CHANNEL_USERNAMES = [row[0] for row in rows]
        return CHANNEL_USERNAMES
    except Exception as e:
        print(f"Error reading data from the database: {e}")
        return []
    finally:
        conn.close()


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    """Команда для проверки подписки"""
    help_text = ("Добро пожаловать!😊\n"
                 "Команды:\n\n"
                 "/help — справка📝\n"
                 "/add_group_id — добавить канал в базу данных🔬\n"
                 "/remove_group_id — удалить канал из базы данных🔨\n"
                 "/start — проверить подписку🔍")
    await message.reply(help_text)


async def is_user_subscribed(user_id):
    """Функция для проверки подписки пользователя на несколько каналов"""
    CHANNEL_USERNAMES = read_channels_from_database()
    try:
        for channel_username in CHANNEL_USERNAMES:
            user = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
            if user.status not in ('member', 'administrator', 'creator'):
                return False
        return True
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        return False


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
        cursor.execute('''CREATE TABLE IF NOT EXISTS users_start (user_id INTEGER PRIMARY KEY, 
                                                                  username TEXT, 
                                                                  first_name TEXT, 
                                                                  last_name TEXT, 
                                                                  join_date TEXT)''')
        cursor.execute('''INSERT OR REPLACE INTO users_start (user_id, 
                                                                   username, 
                                                                   first_name, 
                                                                   last_name, 
                                                                   join_date)
                       VALUES (?, ?, ?, ?, ?)''', (user_id, username, first_name, last_name, join_date))
        conn.commit()
        conn.close()
        logger.info(f"Пользователь нажавший /start: {user_id}, {username}, {first_name}, {last_name}, {join_date}")
        await state.finish()  # Завершаем текущее состояние машины состояний
        await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию
        if await is_user_subscribed(user_id):
            from_user_name = message.from_user.first_name  # Получаем фамилию пользователя
            greeting_post = f"{from_user_name}, Вас приветствует чат-бот 🤖 @TeaBetNY_bot"
            keyboards_greeting = create_greeting_keyboard()  # Клавиатуры поста приветствия 👋
            await message.answer(greeting_post, reply_markup=keyboards_greeting,
                                 parse_mode=types.ParseMode.HTML)  # Текст в HTML-разметки
        else:
            subscription_keyboars = subscription_keyboard()
            await message.answer("Вас приветствует бот-помощник 🤖 TeaBet для участия в конкурсе.\n\n"
                                "Вам необходимо подписаться на канал: https://t.me/tea_flow и оставить свои контактные данные",
                                disable_web_page_preview=True,
                                reply_markup=subscription_keyboars,
                                parse_mode=types.ParseMode.HTML)

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


@dp.message_handler(commands=['add_group_id'])
async def cmd_add_group_id(message: types.Message):
    user_id = message.from_user.id
    if message.chat.type == types.ChatType.PRIVATE:
        await message.reply("Введите username канала, который вы хотите добавить в базу данных:")
        await SomeState.AddingChannel.set()
    else:
        await message.reply("Эта команда доступна только в личных сообщениях (DM).")


@dp.message_handler(state=SomeState.AddingChannel)
async def process_channel_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['channel_username'] = message.text
        try:
            # Попробуйте подключиться к базе данных и добавить username канала
            conn = sqlite3.connect("your_database.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS channels (channel_username)")
            cursor.execute("INSERT INTO channels (channel_username) VALUES (?)", (data['channel_username'],))
            conn.commit()
            conn.close()
            await message.reply(f"Канал {data['channel_username']} добавлен в базу данных.")
        except Exception as e:
            logging.error(f"Error adding channel to database: {e}")
            await message.reply("Произошла ошибка при добавлении канала в базу данных. Попробуйте позже.")
        await state.finish()


async def remove_channel_from_database(channel_username):
    try:
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM channels WHERE channel_username = ?", (channel_username,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Error removing channel from database: {e}")
        return False


@dp.message_handler(commands=['remove_group_id'])
async def cmd_remove_group_id(message: types.Message):
    user_id = message.from_user.id
    if message.chat.type == types.ChatType.PRIVATE:
        await message.reply("Введите username канала, который вы хотите удалить из базы данных:")
        await SomeState.RemovingChannel.set()
    else:
        await message.reply("Эта команда доступна только в личных сообщениях (DM).")


@dp.message_handler(state=SomeState.RemovingChannel)
async def process_remove_channel_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        channel_username = message.text
        if await remove_channel_from_database(channel_username):
            await message.reply(f"Канал {channel_username} удален из базы данных.")
        else:
            await message.reply("Произошла ошибка при удалении канала из базы данных. Попробуйте позже.")
        await state.finish()


def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(greeting)  # Обработчик команды /start, он же пост приветствия 👋
    dp.register_message_handler(disagree_handler)
