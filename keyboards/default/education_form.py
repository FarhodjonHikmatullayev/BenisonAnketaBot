from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

education_form_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Kunduzgi"),
            KeyboardButton(text="Sirtqi")
        ],
        [
            KeyboardButton(text="Kechki"),
            KeyboardButton(text="Masofaviy")
        ],
        [
            KeyboardButton(text="🏠 Asosiy menyu"),
            KeyboardButton(text="⬅️ Ortga")
        ]
    ]
)

education_form_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Очное"),
            KeyboardButton(text="Заочное")
        ],
        [
            KeyboardButton(text="Вечернее"),
            KeyboardButton(text="Дистанционное")
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
            KeyboardButton(text="⬅️ Назад")
        ]
    ]
)
