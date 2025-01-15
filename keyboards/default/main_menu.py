from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🏢Biz haqimizda"),
            KeyboardButton(text="💭 Biz bilan bog'laning"),
        ],
        [
            KeyboardButton(text="💼Bo'sh ish o'rinlari")
        ],
        [
            KeyboardButton(text="📞Kontaktlar"),
            KeyboardButton(text="🇬🇧/🇺🇿 Tilni o'zgartirish"),
        ]
    ]
)

main_menu_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🏢 О нас"),
            KeyboardButton(text="💭 Обратная связь"),
        ],
        [
            KeyboardButton(text="💼 Вакансии")
        ],
        [
            KeyboardButton(text="📞 Контакты"),
            KeyboardButton(text="🇷🇺/🇺🇿 Сменить язык"),
        ]
    ]
)

back_or_main_default_keyboard_uzb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🏠 Asosiy menyu"),
            KeyboardButton(text="⬅️ Ortga")
        ]
    ]
)

back_or_main_default_keyboard_rus = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🏠 Главное меню"),
            KeyboardButton(text="⬅️ Назад")
        ]
    ]
)
