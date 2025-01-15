from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

expected_salary_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="1 mln dan 2.5 mln gacha"),
            KeyboardButton(text="2.5 mln dan 4 mln gacha")
        ],
        [
            KeyboardButton(text="4 mln dan 5.5 mln gacha"),
            KeyboardButton(text="5.5 mln va undan ko'p")
        ],
        [
            KeyboardButton(text="🏠 Asosiy menyu"),
            KeyboardButton(text="⬅️ Ortga")
        ]
    ]
)

expected_salary_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="От 1 мл до 2.5 мл"),
            KeyboardButton(text="От 2.5 млн до 4 млн")
        ],
        [
            KeyboardButton(text="От 4 млн до 5.5 млн"),
            KeyboardButton(text="5.5 млн и больше")
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
            KeyboardButton(text="⬅️ Назад")
        ]
    ]
)
