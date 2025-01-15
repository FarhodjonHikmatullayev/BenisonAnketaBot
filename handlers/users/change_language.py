from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.languages import languages_default_keyboard_uzb, languages_default_keyboard_rus
from keyboards.default.main_menu import main_menu_default_keyboard_uzb, main_menu_default_keyboard_rus
from loader import dp, db


@dp.message_handler(text=["🇬🇧/🇺🇿 Tilni o'zgartirish", "🇷🇺/🇺🇿 Сменить язык"], state="*")
async def contacts_function(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)

    if not users:
        full_name = message.from_user.full_name
        username = message.from_user.username
        user = await db.create_user(
            username=username,
            full_name=full_name,
            telegram_id=user_telegram_id
        )
        role = user['role']
        language = user['language']
    else:
        language = users[0]['language']
    if language == 'uzb':
        text = "Tilni o'zgartirish"
        markup = languages_default_keyboard_uzb
    else:
        text = "Смена языка"
        markup = languages_default_keyboard_rus

    await message.answer(text=text, reply_markup=markup)


@dp.message_handler(text="🇺🇿 O'zbekcha", state="*")
async def change_language_to_uzb(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass

    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)

    if not users:
        full_name = message.from_user.full_name
        username = message.from_user.username
        user = await db.create_user(
            username=username,
            full_name=full_name,
            telegram_id=user_telegram_id
        )
        user_id = user['id']
    else:
        user_id = users[0]['id']
        user = users[0]

    # change language algorithm
    user = await db.update_user(user_id=user_id, language='uzb')

    markup = main_menu_default_keyboard_uzb if user['language'] == 'uzb' else main_menu_default_keyboard_rus
    await message.answer_photo(caption="👋🏻 Assalomu alaykum, men «UZUM» kompaniyasining botiman.\n"
                                       "\n"
                                       "🤖Men:\n"
                                       "- sizga kompaniya va biz bilan ishlashning afzalliklari haqida gapirib beraman;\n"
                                       "- mavjud vakansiyalarni topishga va so'rovnomani to'ldirishga yordam beraman.\n"
                                       "\n"
                                       "🔺 «UZUM» jamoasiga xush kelibsiz ‼️\n"
                                       "\n"
                                       "------------------------------------\n"
                                       "\n"
                                       "👋🏻 Приветствую Вас, я бот-сайт «UZUM».\n"
                                       "\n"
                                       "🤖Я:\n"
                                       "- расскажу Вам о компании и о преимуществах работы у нас;\n"
                                       "- помогу найти актуальные вакансии и заполнить анкету.\n"
                                       "\n"
                                       "🔺 Добро пожаловать в «UZUM» ‼️",
                               photo="AgACAgIAAxkBAAMHZ4JGrQH1WX9E5FsPhnA0zoRVJgQAAuXwMRtgPBFIKJ2Wmb4IBIUBAAMCAAN4AAM2BA",
                               reply_markup=markup)


@dp.message_handler(text="🇷🇺 Русский", state="*")
async def change_language_to_rus(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass

    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)

    if not users:
        full_name = message.from_user.full_name
        username = message.from_user.username
        user = await db.create_user(
            username=username,
            full_name=full_name,
            telegram_id=user_telegram_id
        )
        user_id = user['id']
    else:
        user_id = users[0]['id']

    # change language algorithm
    user = await db.update_user(user_id=user_id, language='rus')

    markup = main_menu_default_keyboard_uzb if user['language'] == 'uzb' else main_menu_default_keyboard_rus
    await message.answer_photo(caption="👋🏻 Assalomu alaykum, men «UZUM» kompaniyasining botiman.\n"
                                       "\n"
                                       "🤖Men:\n"
                                       "- sizga kompaniya va biz bilan ishlashning afzalliklari haqida gapirib beraman;\n"
                                       "- mavjud vakansiyalarni topishga va so'rovnomani to'ldirishga yordam beraman.\n"
                                       "\n"
                                       "🔺 «UZUM» jamoasiga xush kelibsiz ‼️\n"
                                       "\n"
                                       "------------------------------------\n"
                                       "\n"
                                       "👋🏻 Приветствую Вас, я бот-сайт «UZUM».\n"
                                       "\n"
                                       "🤖Я:\n"
                                       "- расскажу Вам о компании и о преимуществах работы у нас;\n"
                                       "- помогу найти актуальные вакансии и заполнить анкету.\n"
                                       "\n"
                                       "🔺 Добро пожаловать в «UZUM» ‼️",
                               photo="AgACAgIAAxkBAAMHZ4JGrQH1WX9E5FsPhnA0zoRVJgQAAuXwMRtgPBFIKJ2Wmb4IBIUBAAMCAAN4AAM2BA",
                               reply_markup=markup)


@dp.message_handler(text=["🔙 Назад", "🔙 Orqaga"], state="*")
async def change_language_to_rus(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass

    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)

    if not users:
        full_name = message.from_user.full_name
        username = message.from_user.username
        user = await db.create_user(
            username=username,
            full_name=full_name,
            telegram_id=user_telegram_id
        )
        user_id = user['id']
    else:
        user_id = users[0]['id']
        user = users[0]

    markup = main_menu_default_keyboard_uzb if user['language'] == 'uzb' else main_menu_default_keyboard_rus
    await message.answer_photo(caption="👋🏻 Assalomu alaykum, men «UZUM» kompaniyasining botiman.\n"
                                       "\n"
                                       "🤖Men:\n"
                                       "- sizga kompaniya va biz bilan ishlashning afzalliklari haqida gapirib beraman;\n"
                                       "- mavjud vakansiyalarni topishga va so'rovnomani to'ldirishga yordam beraman.\n"
                                       "\n"
                                       "🔺 «UZUM» jamoasiga xush kelibsiz ‼️\n"
                                       "\n"
                                       "------------------------------------\n"
                                       "\n"
                                       "👋🏻 Приветствую Вас, я бот-сайт «UZUM».\n"
                                       "\n"
                                       "🤖Я:\n"
                                       "- расскажу Вам о компании и о преимуществах работы у нас;\n"
                                       "- помогу найти актуальные вакансии и заполнить анкету.\n"
                                       "\n"
                                       "🔺 Добро пожаловать в «UZUM» ‼️",
                               photo="AgACAgIAAxkBAAMHZ4JGrQH1WX9E5FsPhnA0zoRVJgQAAuXwMRtgPBFIKJ2Wmb4IBIUBAAMCAAN4AAM2BA",
                               reply_markup=markup)
