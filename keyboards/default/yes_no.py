from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

yes_no_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Ha"),
            KeyboardButton(text="Yo'q")
        ],
        [
            KeyboardButton(text="🏠 Asosiy menyu"),
            KeyboardButton(text="⬅️ Ortga")
        ]
    ]
)

yes_no_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
            KeyboardButton(text="⬅️ Назад")
        ]
    ]
)
