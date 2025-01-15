from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_level_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Past(tushunmayman va gapirmayman)"),
            KeyboardButton(text="O'rta(tushunaman, lekin yomon gapiraman)")
        ],
        [
            KeyboardButton(text="Ilg'or(men ravon gapiraman va tushunaman)"),
        ],
        [
            KeyboardButton(text="🏠 Asosiy menyu"),
            KeyboardButton(text="⬅️ Ortga")
        ]
    ]
)

language_level_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Низкий (не понимаю и не говорю)"),
            KeyboardButton(text="Средний (понимаю, но плохо говорю)")
        ],
        [
            KeyboardButton(text="Продвинутый (свободно говорю и понимаю)"),
        ],
        [
            KeyboardButton(text="🏠 Главное меню"),
            KeyboardButton(text="⬅️ Назад")
        ]
    ]
)
