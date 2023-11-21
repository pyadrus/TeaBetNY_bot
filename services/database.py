import sqlite3
from loguru import logger  # Логирование с помощью loguru

table_name = '''CREATE TABLE IF NOT EXISTS users (user_order, user_id, name, surname, phone_number, registration_date)'''


def insert_user_data_to_database(user_order, user_id, name, surname, phone_number, registration_date):
    """Записывает данные пользователя в базу данных"""
    try:
        conn = sqlite3.connect("your_database.db")  # Замените "your_database.db" на имя вашей базы данных
        cursor = conn.cursor()
        cursor.execute(table_name)
        cursor.execute("INSERT INTO users (user_order, user_id, name, surname, phone_number, registration_date) "
                       "VALUES (?, ?, ?, ?, ?, ?)",
                       (user_order, user_id, name, surname, phone_number, registration_date))
        conn.commit()
    except sqlite3.Error as e:
        logger.info(f"Ошибка при записи данных в базу данных: {e}")
    finally:
        conn.close()


def get_user_data_from_db(user_id):
    try:
        conn = sqlite3.connect("your_database.db")  # Замените "your_database.db" на имя вашей базы данных
        cursor = conn.cursor()
        cursor.execute(table_name)
        # Выполните SQL-запрос для получения данных о пользователе по его user_id
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()  # Получите данные первой найденной записи
        conn.close()
        # Верните данные о пользователе как словарь, если они существуют, или None, если пользователя нет
        if user_data:
            _, _, name, surname, phone_number, registration_date = user_data
            return {'name': name, 'surname': surname, 'phone_number': phone_number,
                    'registration_date': registration_date}
        else:
            return None
    except Exception as e:
        logger.info(e)


def fetch_user_data_from_db(user_id):
    # Замените "your_database.db" на имя вашей базы данных
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    # Выполните SQL-запрос для получения данных о пользователе по его user_id
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()  # Получите данные первой найденной записи
    conn.close()

    # Верните данные о пользователе как словарь, если они существуют, или None, если пользователя нет
    if user_data:
        user_id, name, surname, phone_number, registration_date = user_data
        return {'user_id': user_id, 'name': name, 'surname': surname, 'phone_number': phone_number,
                'registration_date': registration_date}
    else:
        return None


# Функция для изменения имени в базе данных по ID
def update_name_in_db(user_id, new_name):
    try:
        # Подключаемся к базе данных (предполагается, что она уже существует)
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        # SQL-запрос для обновления имени
        update_query = "UPDATE users SET name = ? WHERE user_id = ?"
        cursor.execute(update_query, (new_name, user_id))
        conn.commit()  # Применяем изменения к базе данных
        conn.close()  # Закрываем соединение с базой данных
        return True  # Возвращаем True в случае успешного обновления
    except Exception as e:
        logger.info("Ошибка при обновлении имени:", str(e))
        return False  # Возвращаем False в случае ошибки


def update_surname_in_db(user_id, new_surname):
    try:
        # Подключаемся к базе данных (предполагается, что она уже существует)
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        # SQL-запрос для обновления имени
        update_query = "UPDATE users SET surname = ? WHERE user_id = ?"
        cursor.execute(update_query, (new_surname, user_id))
        conn.commit()  # Применяем изменения к базе данных
        conn.close()  # Закрываем соединение с базой данных
        return True  # Возвращаем True в случае успешного обновления
    except Exception as e:
        logger.info("Ошибка при обновлении фамилии:", str(e))
        return False  # Возвращаем False в случае ошибки


def update_city_in_db(user_id, new_city):
    try:
        # Подключаемся к базе данных (предполагается, что она уже существует)
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        # SQL-запрос для обновления имени
        update_query = "UPDATE users SET city = ? WHERE user_id = ?"
        cursor.execute(update_query, (new_city, user_id))
        conn.commit()  # Применяем изменения к базе данных
        conn.close()  # Закрываем соединение с базой данных
        return True  # Возвращаем True в случае успешного обновления
    except Exception as e:
        logger.info("Ошибка при обновлении фамилии:", str(e))
        return False  # Возвращаем False в случае ошибки


def update_phone_in_db(user_id, new_phone):
    try:
        # Подключаемся к базе данных (предполагается, что она уже существует)
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        # SQL-запрос для обновления имени
        update_query = "UPDATE users SET phone_number = ? WHERE user_id = ?"
        cursor.execute(update_query, (new_phone, user_id))
        conn.commit()  # Применяем изменения к базе данных
        conn.close()  # Закрываем соединение с базой данных
        return True  # Возвращаем True в случае успешного обновления
    except Exception as e:
        logger.info("Ошибка при обновлении фамилии:", str(e))
        return False  # Возвращаем False в случае ошибки


def count_users_by_order():
    """Возвращает количество пользователей в порядке их добавления"""
    try:
        conn = sqlite3.connect("your_database.db")  # Замените "your_database.db" на имя вашей базы данных
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        logger.info(f"Ошибка при чтении данных из базы данных: {e}")
    finally:
        conn.close()


def check_user_exists_in_db(user_id):
    # Подключитесь к вашей базе данных
    conn = sqlite3.connect("your_database.db")  # Замените "your_database.db" на имя вашей базы данных
    cursor = conn.cursor()
    # Выполните SQL-запрос для проверки наличия пользователя в базе данных по его user_id
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
    # Извлеките результат запроса
    user_count = cursor.fetchone()[0]
    conn.close()
    # Если пользователь с указанным user_id найден (user_count больше 0), верните True, иначе верните False
    return user_count > 0
