from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def region_keyboard_uzb():
    regions = await db.select_all_regions()
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.resize_keyboard = True
    for region in regions:
        vacancies = await db.select_vacancy(region_id=region['id'])
        if vacancies:
            markup.insert(KeyboardButton(text=f"{region['name_uzb']}"))

    markup.add(KeyboardButton(text="🏠 Asosiy menyu"), KeyboardButton(text="⬅️ Ortga"))

    return markup


async def region_keyboard_rus():
    regions = await db.select_all_regions()
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.resize_keyboard = True
    for region in regions:
        vacancies = await db.select_vacancy(region_id=region['id'])
        if vacancies:
            markup.insert(KeyboardButton(text=f"{region['name_rus']}"))

    markup.add(KeyboardButton(text="🏠 Главное меню"), KeyboardButton(text="⬅️ Назад"))

    return markup
