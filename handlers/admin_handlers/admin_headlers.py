import os
import sqlite3

from aiogram import types
from aiogram.dispatcher.filters import Command
from openpyxl import Workbook

from system.dispatcher import dp, ADMIN_CHAT_ID  # Подключение к боту и диспетчеру пользователя


# Функция для создания и отправки файла Excel с данными из базы данных
async def send_data_as_excel(message: types.Message):
    # Создаем временный файл Excel
    excel_filename = "Зарегистрированные пользователи.xlsx"
    # Создаем рабочую книгу Excel
    wb = Workbook()
    ws = wb.active
    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    # Выполняем SQL-запрос для извлечения данных
    cursor.execute("SELECT * FROM users")
    user_data = cursor.fetchall()
    # Заголовки столбцов
    ws.append(["User ID Telegram", "Имя", "Фамилия", "Город", "Номер телефона", "Дата регистрации"])
    # Добавляем данные в таблицу
    for row in user_data:
        ws.append(row)
    # Сохраняем книгу Excel
    wb.save(excel_filename)
    # Закрываем соединение с базой данных
    conn.close()
    # Отправляем файл пользователю
    with open(excel_filename, "rb") as excel_file:
        await message.reply_document(excel_file, caption="Данные зарегистрированных пользователей в боте")
    # Удаляем временный файл Excel
    os.remove(excel_filename)


async def get_users_send_data_as_excel(message: types.Message):
    # Создаем временный файл Excel
    excel_filename = "Активные_пользователи.xlsx"
    # Создаем рабочую книгу Excel
    wb = Workbook()
    ws = wb.active
    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    # Выполняем SQL-запрос для извлечения данных
    cursor.execute("SELECT * FROM users_start")
    user_data = cursor.fetchall()
    # Заголовки столбцов
    ws.append(["User ID", "Username", "First Name", "Last Name", "Join Date"])
    # Добавляем данные в таблицу
    for row in user_data:
        ws.append(row)
    # Сохраняем книгу Excel
    wb.save(excel_filename)
    # Закрываем соединение с базой данных
    conn.close()
    # Отправляем файл пользователю
    with open(excel_filename, "rb") as excel_file:
        await message.answer_document(excel_file, caption="Данные зарегистрированных пользователей в боте")
    # Удаляем временный файл Excel get_users   get_users_info
    os.remove(excel_filename)


# Функция для проверки, является ли пользователь администратором
def is_admin_user(user_id):
    return user_id == ADMIN_CHAT_ID


# Обработчик команды /get_users
@dp.message_handler(Command("get_users"))
async def get_users_info(message: types.Message):
    user_id = message.from_user.id
    if is_admin_user(user_id):
        await get_users_send_data_as_excel(message)
    else:
        await message.answer("Эта команда доступна только для администраторов.")


# Обработчик команды /get_data
@dp.message_handler(Command("get_data"))
async def get_data_command(message: types.Message):
    user_id = message.from_user.id
    if is_admin_user(user_id):
        await send_data_as_excel(message)
    else:
        await message.answer("Эта команда доступна только для администраторов.")


def send_data_as_excel_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(get_data_command)
    dp.register_message_handler(get_users_info)
