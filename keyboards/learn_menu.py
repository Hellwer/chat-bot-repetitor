from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def learn_menu_kb():
    keyboard = [
        [KeyboardButton(text="по предложениям"), KeyboardButton(text="по абзацам")],
        [KeyboardButton(text="Вернуться в меню")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
