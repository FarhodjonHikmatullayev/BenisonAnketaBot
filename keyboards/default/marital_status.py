from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

marital_status_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Uylangan/erga tekkan"),
            KeyboardButton(text="Uylanmagan/erga tegmagan")
        ],
        [
            KeyboardButton(text="Ajrashgan"),
            KeyboardButton(text="Beva")
        ],
        [
            KeyboardButton(text="🏠 Asosiy menyu"),
            KeyboardButton(text="⬅️ Ortga")
        ]
    ]
)

marital_status_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Женат/замужем"),
            KeyboardButton(text="Не женат/не замужем")
        ],
        [
            KeyboardButton(text="Разведен/Разведена"),
            KeyboardButton(text="Вдовец/Вдова")
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
            KeyboardButton(text="⬅️ Назад")
        ]
    ]
)
