import os
import sqlite3

from aiogram import types
from aiogram.dispatcher.filters import Command
from openpyxl import Workbook

from system.dispatcher import dp, ADMIN_CHAT_ID  # Подключение к боту и диспетчеру пользователя


async def send_data_as_excel(message: types.Message):
    """Функция для создания и отправки файла Excel с данными из базы данных"""
    excel_filename = "Зарегистрированные пользователи.xlsx"  # Создаем временный файл Excel
    wb = Workbook()  # Создаем рабочую книгу Excel
    ws = wb.active
    conn = sqlite3.connect("your_database.db")  # Подключаемся к базе данных SQLite
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # Выполняем SQL-запрос для извлечения данных
    user_data = cursor.fetchall()
    # Заголовки столбцов
    ws.append(["User ID Telegram", "Имя", "Фамилия", "Номер телефона", "Дата регистрации"])
    for row in user_data:  # Добавляем данные в таблицу
        ws.append(row)
    wb.save(excel_filename)  # Сохраняем книгу Excel
    conn.close()  # Закрываем соединение с базой данных
    with open(excel_filename, "rb") as excel_file:  # Отправляем файл пользователю
        await message.reply_document(excel_file, caption="Данные зарегистрированных пользователей в боте")
    os.remove(excel_filename)  # Удаляем временный файл Excel


async def get_users_send_data_as_excel(message: types.Message):
    excel_filename = "Активные_пользователи.xlsx"  # Создаем временный файл Excel
    wb = Workbook()  # Создаем рабочую книгу Excel
    ws = wb.active
    conn = sqlite3.connect("your_database.db")  # Подключаемся к базе данных SQLite
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_start")  # Выполняем SQL-запрос для извлечения данных
    user_data = cursor.fetchall()
    ws.append(["User ID", "Username", "First Name", "Last Name", "Join Date"])  # Заголовки столбцов
    for row in user_data:  # Добавляем данные в таблицу
        ws.append(row)
    wb.save(excel_filename)  # Сохраняем книгу Excel
    conn.close()  # Закрываем соединение с базой данных
    with open(excel_filename, "rb") as excel_file:  # Отправляем файл пользователю
        await message.answer_document(excel_file, caption="Данные зарегистрированных пользователей в боте")
    os.remove(excel_filename)  # Удаляем временный файл Excel get_users   get_users_info


def is_admin_user(user_id):
    """Функция для проверки, является ли пользователь администратором"""
    return user_id == ADMIN_CHAT_ID


@dp.message_handler(Command("get_users"))
async def get_users_info(message: types.Message):
    """Обработчик команды /get_users"""
    user_id = message.from_user.id
    if is_admin_user(user_id):
        await get_users_send_data_as_excel(message)
    else:
        await message.answer("Эта команда доступна только для администраторов.")


@dp.message_handler(Command("get_data"))
async def get_data_command(message: types.Message):
    """Обработчик команды /get_data"""
    user_id = message.from_user.id
    if is_admin_user(user_id):
        await send_data_as_excel(message)
    else:
        await message.answer("Эта команда доступна только для администраторов.")


def send_data_as_excel_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(get_data_command)
    dp.register_message_handler(get_users_info)
