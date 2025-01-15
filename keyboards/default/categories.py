from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def category_keyboard_uzb(region_id):
    categories = await db.select_all_categories()
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.resize_keyboard = True
    for category in categories:
        vacancies = await db.select_vacancy(region_id=region_id, category_id=category['id'])
        if vacancies:
            markup.insert(KeyboardButton(text=f"{category['title_uzb']}"))

    markup.add(KeyboardButton(text="🏠 Asosiy menyu"), KeyboardButton(text="⬅️ Ortga"))

    return markup


async def category_keyboard_rus(region_id):
    categories = await db.select_all_categories()
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.resize_keyboard = True
    for category in categories:
        vacancies = await db.select_vacancy(region_id=region_id, category_id=category['id'])
        if vacancies:
            markup.insert(KeyboardButton(text=f"{category['title_rus']}"))

    markup.add(KeyboardButton(text="🏠 Главное меню"), KeyboardButton(text="⬅️ Назад"))

    return markup
