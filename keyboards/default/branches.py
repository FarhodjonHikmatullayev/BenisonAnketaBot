from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def branch_keyboard_uzb(region_id, category_id):
    branches = await db.select_all_branches()
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.resize_keyboard = True
    for branch in branches:
        vacancies = await db.select_vacancy(region_id=region_id, category_id=category_id, branch_id=branch['id'])
        if vacancies:
            markup.insert(KeyboardButton(text=f"{branch['title_uzb']}"))

    markup.add(KeyboardButton(text="🏠 Asosiy menyu"), KeyboardButton(text="⬅️ Ortga"))

    return markup


async def branch_keyboard_rus(region_id, category_id):
    branches = await db.select_all_branches()
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.resize_keyboard = True
    for branch in branches:
        vacancies = await db.select_vacancy(region_id=region_id, category_id=category_id, branch_id=branch['id'])
        if vacancies:
            markup.insert(KeyboardButton(text=f"{branch['title_rus']}"))

    markup.add(KeyboardButton(text="🏠 Главное меню"), KeyboardButton(text="⬅️ Назад"))

    return markup
