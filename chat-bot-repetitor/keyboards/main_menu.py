from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    keyboard = [
        [KeyboardButton(text="Прогресс")],
        [KeyboardButton(text="Учить")],
        [KeyboardButton(text="Список текстов")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
