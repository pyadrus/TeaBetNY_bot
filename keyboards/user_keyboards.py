from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def create_greeting_keyboard():
    """Создает клавиатуру для приветственного сообщения 👋"""
    greeting_keyboard = InlineKeyboardMarkup()
    my_details_button = InlineKeyboardButton(text='ℹ️ Мои данные', callback_data='my_details')

    greeting_keyboard.row(my_details_button)  # Мои данные
    return greeting_keyboard


def create_sign_up_keyboard():
    """Создает клавиатуру для кнопок 'Согласен' и 'Не согласен'"""
    sign_up_keyboard = InlineKeyboardMarkup()
    agree_button = InlineKeyboardButton(text='👍 Согласен(а)', callback_data='agree')
    disagree_button = InlineKeyboardButton(text='👎 Не согласен(а)', callback_data='disagree')

    sign_up_keyboard.row(agree_button, disagree_button)
    return sign_up_keyboard


def create_contact_keyboard():
    """Создает клавиатуру для отправки контакта"""
    contact_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    send_contact_button = KeyboardButton("📱 Отправить", request_contact=True)

    contact_keyboard.add(send_contact_button)
    return contact_keyboard


def create_data_modification_keyboard():
    """Создает клавиатуру для изменения данных"""
    data_modification_keyboard = InlineKeyboardMarkup()
    edit_name_button = InlineKeyboardButton("✏️Изменить Имя", callback_data="edit_name")
    edit_surname_button = InlineKeyboardButton("✏️Изменить Фамилию", callback_data="edit_surname")
    edit_phone_button = InlineKeyboardButton("✏️Изменить Номер 📱 ", callback_data="edit_phone")
    start_button = InlineKeyboardButton("↩️ Вернуться в начальное меню", callback_data="return_to_start_menu")

    data_modification_keyboard.row(edit_name_button)
    data_modification_keyboard.row(edit_surname_button)
    data_modification_keyboard.row(edit_phone_button)
    data_modification_keyboard.row(start_button)
    return data_modification_keyboard


def subscription_keyboard():
    """Клавиатура подписки"""
    subscription_keyboars = InlineKeyboardMarkup()
    subscribe_button = InlineKeyboardButton("Подписаться", url="https://t.me/tea_flow")
    i_subscribed_button = InlineKeyboardButton("Я подписался", callback_data="i_subscribed")
    subscription_keyboars.row(subscribe_button)
    subscription_keyboars.row(i_subscribed_button)
    return subscription_keyboars


if __name__ == '__main__':
    create_greeting_keyboard()
    create_sign_up_keyboard()
    create_contact_keyboard()
    create_data_modification_keyboard()
    subscription_keyboard()  # Клавиатура подписки
