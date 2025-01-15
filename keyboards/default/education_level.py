from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

education_level_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="O'rta"),
            KeyboardButton(text="O'rta maxsus")
        ],
        [
            KeyboardButton(text="Oliy"),
        ],
        [
            KeyboardButton(text="🏠 Asosiy menyu"),
            KeyboardButton(text="⬅️ Ortga")
        ]
    ]
)

education_level_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Среднее"),
            KeyboardButton(text="Среднее-специальное")
        ],
        [
            KeyboardButton(text="Высшее"),
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
            KeyboardButton(text="⬅️ Назад")
        ]
    ]
)
