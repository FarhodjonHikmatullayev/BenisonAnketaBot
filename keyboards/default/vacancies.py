from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def vacancy_keyboard_uzb(region_id, category_id, branch_id):
    vacancies = await db.select_vacancy(region_id=region_id, category_id=category_id, branch_id=branch_id)
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.resize_keyboard = True
    for vacancy in vacancies:
        markup.insert(KeyboardButton(text=f"{vacancy['title_uzb']}"))

    markup.add(KeyboardButton(text="🏠 Asosiy menyu"), KeyboardButton(text="⬅️ Ortga"))

    return markup


async def vacancy_keyboard_rus(region_id, category_id, branch_id):
    vacancies = await db.select_vacancy(region_id=region_id, category_id=category_id, branch_id=branch_id)
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.resize_keyboard = True
    for vacancy in vacancies:
        markup.insert(KeyboardButton(text=f"{vacancy['title_rus']}"))

    markup.add(KeyboardButton(text="🏠 Главное меню"), KeyboardButton(text="⬅️ Назад"))

    return markup
