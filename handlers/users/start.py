from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_menu import main_menu_default_keyboard_uzb, main_menu_default_keyboard_rus
from loader import dp, db
from states.resume import ResumeState


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.region)
@dp.message_handler(text=["🏠 Главное меню", "🏠 Asosiy menyu"], state="*")
@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
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
        role = users[0]['role']
        language = users[0]['language']
    markup = main_menu_default_keyboard_uzb if language == 'uzb' else main_menu_default_keyboard_rus
    if role == 'user':
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
    else:
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
