from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

computer_level_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Bilmayman"),
            KeyboardButton(text="O'rtacha daraja")
        ],
        [
            KeyboardButton(text="Foydalanuvchi"),
            KeyboardButton(text="Mutaxasis")
        ],
        [
            KeyboardButton(text="🏠 Asosiy menyu"),
            KeyboardButton(text="⬅️ Ortga")
        ]
    ]
)

computer_level_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Не владею"),
            KeyboardButton(text="Средний уровень")
        ],
        [
            KeyboardButton(text="Пользователь"),
            KeyboardButton(text="Эксперт")
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
            KeyboardButton(text="⬅️ Назад")
        ]
    ]
)
