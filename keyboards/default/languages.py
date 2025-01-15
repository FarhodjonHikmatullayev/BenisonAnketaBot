from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

languages_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🇷🇺 Русский"),
            KeyboardButton(text="🇺🇿 O'zbekcha"),
        ],
        [
            KeyboardButton(text="🔙 Orqaga")
        ],
    ]
)

languages_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🇷🇺 Русский"),
            KeyboardButton(text="🇺🇿 O'zbekcha"),
        ],
        [
            KeyboardButton(text="🔙 Назад")
        ],
    ]
)
