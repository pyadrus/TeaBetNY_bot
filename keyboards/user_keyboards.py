from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def create_greeting_keyboard():
    """Создает клавиатуру для приветственного сообщения 👋"""
    greeting_keyboard = InlineKeyboardMarkup()
    my_details_button = InlineKeyboardButton(text='ℹ️ Мои данные', callback_data='my_details')

    greeting_keyboard.row(my_details_button)  # Мои данные
    return greeting_keyboard


def stock_keyboard():
    """Клавиатура с акциями"""
    stock_keyboard = InlineKeyboardMarkup()
    happy_parents_button = InlineKeyboardButton(text="Счастливые родители", callback_data='happy_parents')
    second_opinion_of_fertility_specialists = InlineKeyboardButton(text="Второе мнение репродуктологов БЕСПЛАТНО", callback_data='second_opinion_of_fertility_specialists')
    the_second_opinion_of_the_operators = InlineKeyboardButton(text="Второе мнение оперирующих гинекологов БЕСПЛАТНО", callback_data='the_second_opinion_of_the_operators')
    stock_keyboard.row(happy_parents_button)
    stock_keyboard.row(second_opinion_of_fertility_specialists)
    stock_keyboard.row(the_second_opinion_of_the_operators)
    return stock_keyboard


def create_my_details_keyboard():
    """Создает клавиатуру для кнопки 'Мои данные'"""
    my_details_keyboard = InlineKeyboardMarkup()
    my_details_button = InlineKeyboardButton(text='Мои данные', callback_data='my_details')

    my_details_keyboard.row(my_details_button)  # Связаться с оператором
    return my_details_keyboard


def create_sign_up_keyboard():
    """Создает клавиатуру для кнопок 'Согласен' и 'Не согласен'"""
    sign_up_keyboard = InlineKeyboardMarkup()
    agree_button = InlineKeyboardButton(text='👍 Согласен', callback_data='agree')
    disagree_button = InlineKeyboardButton(text='👎 Не согласен', callback_data='disagree')

    sign_up_keyboard.row(agree_button, disagree_button)
    return sign_up_keyboard


def appointment_selection_keypad():
    """Создает клавиатуру для выбора способа связи"""
    appointment_selection_key = InlineKeyboardMarkup()
    call_button = InlineKeyboardButton(text="Позвонить", callback_data="call_us")
    callback_button = InlineKeyboardButton(text="Заказать обратный звонок", callback_data="callback_key")
    chat_with_operator_button = InlineKeyboardButton(text="Чат с оператором", url="https://t.me/pk_alina")

    appointment_selection_key.row(call_button, callback_button)
    appointment_selection_key.row(chat_with_operator_button)
    return appointment_selection_key


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
    edit_city_button = InlineKeyboardButton("✏️Изменить Город", callback_data="edit_city")
    edit_phone_button = InlineKeyboardButton("✏️Изменить Номер 📱 ", callback_data="edit_phone")
    start_button = InlineKeyboardButton("↩️ Вернуться в начальное меню", callback_data="disagree")

    data_modification_keyboard.row(edit_name_button, edit_surname_button)
    data_modification_keyboard.row(edit_city_button, edit_phone_button)
    data_modification_keyboard.row(start_button)
    return data_modification_keyboard


if __name__ == '__main__':
    create_greeting_keyboard()
    create_sign_up_keyboard()
    appointment_selection_keypad()
    create_contact_keyboard()
    create_my_details_keyboard()
    create_data_modification_keyboard()
    stock_keyboard()
