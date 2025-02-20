from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def texts_menu_kb():
    keyboard = [
        [KeyboardButton(text="добавить текст"), KeyboardButton(text="перейти по текстам")],
        [KeyboardButton(text="Вернуться в меню")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
