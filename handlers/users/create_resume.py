import os
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.agreement import agreement_default_keyboard_uzb, agreement_default_keyboard_rus
from keyboards.default.branches import branch_keyboard_uzb, branch_keyboard_rus
from keyboards.default.categories import category_keyboard_uzb, category_keyboard_rus
from keyboards.default.computer_level import computer_level_default_keyboard_uzb, computer_level_default_keyboard_rus
from keyboards.default.education_form import education_form_default_keyboard_uzb, education_form_default_keyboard_rus
from keyboards.default.education_level import education_level_default_keyboard_uzb, education_level_default_keyboard_rus
from keyboards.default.expected_salary import expected_salary_default_keyboard_uzb, expected_salary_default_keyboard_rus
from keyboards.default.gender import gender_default_keyboard_uzb, gender_default_keyboard_rus
from keyboards.default.main_menu import back_or_main_default_keyboard_uzb, back_or_main_default_keyboard_rus, \
    main_menu_default_keyboard_rus, main_menu_default_keyboard_uzb
from keyboards.default.marital_status import marital_status_default_keyboard_rus, marital_status_default_keyboard_uzb
from keyboards.default.regions import region_keyboard_uzb, region_keyboard_rus
from keyboards.default.send import send_default_keyboard_uzb, send_default_keyboard_rus
from keyboards.default.source_about_vacancy import source_about_vacancy_default_keyboard_uzb, \
    source_about_vacancy_default_keyboard_rus
from keyboards.default.uzb_language_level import language_level_default_keyboard_uzb, \
    language_level_default_keyboard_rus
from keyboards.default.vacancies import vacancy_keyboard_uzb, vacancy_keyboard_rus
from keyboards.default.yes_no import yes_no_default_keyboard_uzb, yes_no_default_keyboard_rus
from loader import dp, db, bot
from states.resume import ResumeState
from utils.data_validator import validate_date, validate_phone_number, validate_email

PHOTO_DIR = 'media/photos'
if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.category)
@dp.message_handler(text=["💼Bo'sh ish o'rinlari", "💼 Вакансии"], state="*")
async def vacancies(message: types.Message, state: FSMContext):
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
        user_id = user['id']
    else:
        language = users[0]['language']
        user_id = users[0]['id']
    if language == 'uzb':
        text1 = "Keling, rezyumeni yaratishni boshlaylik"
        text2 = "Hududni tanlang."
        markup = await region_keyboard_uzb()
    else:
        text1 = "Приступим к созданию Вашего резюме"
        text2 = "Выберите Регион."
        markup = await region_keyboard_rus()

    await message.answer(text=text1)
    await message.answer(text=text2, reply_markup=markup)
    await ResumeState.region.set()
    await state.update_data(language=language, user_id=user_id)


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.branch)
@dp.message_handler(state=ResumeState.region)
async def get_region(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    region = message.text
    if region not in ["⬅️ Ortga", "⬅️ Назад"]:
        regions = await db.select_region(name_uzb=region) if language == 'uzb' else await db.select_region(
            name_rus=region)
        if not regions:
            if language == 'uzb':
                text1 = "Noto'g'ri ma'lumot kiritildi"
                text2 = "Hududni tanlang."
                markup = await region_keyboard_uzb()
            else:
                text1 = "Введена неверная информация"
                text2 = "Выберите Регион."
                markup = await region_keyboard_rus()
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        region_id = regions[0]['id']
        await state.update_data(region=region_id)
    else:
        region_id = data.get('region')

    text = "Ish yo'nalishini tanlang." if language == 'uzb' else "Выберите направление."
    markup = await category_keyboard_uzb(region_id=region_id) if language == 'uzb' else await category_keyboard_rus(
        region_id=region_id)
    await ResumeState.category.set()
    await message.answer(text=text, reply_markup=markup)


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.vacancy)
@dp.message_handler(state=ResumeState.category)
async def get_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    region_id = data.get('region')
    category = message.text
    if category not in ["⬅️ Ortga", "⬅️ Назад"]:

        categories = await db.select_category(title_uzb=category) if language == 'uzb' else await db.select_category(
            title_rus=category)
        if not categories:
            if language == 'uzb':
                text1 = "Noto'g'ri ma'lumot kiritildi"
                text2 = "Ish yo'nalishini tanlang."
                markup = await category_keyboard_uzb(region_id=region_id)
            else:
                text1 = "Введена неверная информация"
                text2 = "Выберите направление."
                markup = await category_keyboard_rus(region_id=region_id)
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        category_id = categories[0]['id']
        await state.update_data(category=category_id)
    else:
        category_id = data.get('category')

    text = "📍 Filialni tanlang" if language == 'uzb' else "📍 Выберите филиал"
    markup = await branch_keyboard_uzb(region_id=region_id,
                                       category_id=category_id) if language == 'uzb' \
        else await branch_keyboard_rus(
        category_id=category_id,
        region_id=region_id)
    await ResumeState.branch.set()
    await message.answer(text=text, reply_markup=markup)


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.first_name)
@dp.message_handler(state=ResumeState.branch)
async def get_branch(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    region_id = data.get('region')
    category_id = data.get('category')
    branch = message.text

    if branch not in ["⬅️ Ortga", "⬅️ Назад"]:

        branches = await db.select_branch(title_uzb=branch) if language == 'uzb' else await db.select_branch(
            title_rus=branch)
        if not branches:
            if language == 'uzb':
                text1 = "Noto'g'ri ma'lumot kiritildi"
                text2 = "📍 Filialni tanlang."
                markup = await branch_keyboard_uzb(region_id=region_id,
                                                   category_id=category_id)
            else:
                text1 = "Введена неверная информация"
                text2 = "📍 Выберите филиал."
                markup = await branch_keyboard_rus(region_id=region_id,
                                                   category_id=category_id)
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        branch_id = branches[0]['id']
        await state.update_data(branch=branch_id)
    else:
        branch_id = data.get('branch')
    branches = await db.select_branch(id=branch_id)

    text = f"{branches[0]['description_uzb']}" if language == 'uzb' else f"{branches[0]['description_rus']}"
    await message.answer(text=text)
    await message.answer_location(latitude=float(branches[0]['latitude']), longitude=float(branches[0]['longitude']))

    text = "💼 Sizni qiziqtirgan vakansiyani tanlang" if language == 'uzb' else "💼 Выберите интересующую Вас вакансию"
    markup = await vacancy_keyboard_uzb(region_id=region_id,
                                        category_id=category_id,
                                        branch_id=branch_id) if language == 'uzb' \
        else await vacancy_keyboard_rus(
        category_id=category_id,
        region_id=region_id,
        branch_id=branch_id)
    await ResumeState.vacancy.set()
    await message.answer(text=text, reply_markup=markup)


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.last_name)
@dp.message_handler(state=ResumeState.vacancy)
async def get_vacancy(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    region_id = data.get('region')
    category_id = data.get('category')
    branch_id = data.get('branch')
    vacancy = message.text

    if vacancy not in ["⬅️ Ortga", "⬅️ Назад"]:

        vacancies = await db.select_vacancy(title_uzb=vacancy) if language == 'uzb' else await db.select_vacancy(
            title_rus=vacancy)
        if not vacancies:
            if language == 'uzb':
                text1 = "Noto'g'ri ma'lumot kiritildi"
                text2 = "💼 Sizni qiziqtirgan vakansiyani tanlang"
                markup = await vacancy_keyboard_uzb(region_id=region_id,
                                                    category_id=category_id,
                                                    branch_id=branch_id)
            else:
                text1 = "Введена неверная информация"
                text2 = "💼 Выберите интересующую Вас вакансию"
                markup = await vacancy_keyboard_rus(region_id=region_id,
                                                    category_id=category_id,
                                                    branch_id=branch_id)
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        vacancy_id = vacancies[0]['id']
        await state.update_data(vacancy=vacancy_id)
    else:
        vacancy_id = data.get('vacancy')
    if message.text not in ["⬅️ Ortga", "⬅️ Назад"]:
        vacancies = await db.select_vacancy(id=vacancy_id)
        vacancy = vacancies[0]

        text = f"{vacancy['description_uzb']}" if language == 'uzb' else f"{vacancy['description_rus']}"
        if vacancy['photo']:
            photo_path = vacancy['photo']
            photo_path = "media/" + photo_path
            if os.path.isfile(photo_path):
                with open(photo_path, 'rb') as photo_file:
                    await message.answer_photo(photo=photo_file, caption=text)
        else:
            await message.answer(text=text)
    if language == 'uzb':
        text = ("👤 Passport bo'yicha ismingizni kiriting\n"
                "(Misol uchun: Baxodir)")
        markup = back_or_main_default_keyboard_uzb
    else:
        text = ("👤 Введите имя по паспорту\n"
                "(пример:  Baxodir)")
        markup = back_or_main_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.first_name.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.fathers_name)
@dp.message_handler(state=ResumeState.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    first_name = message.text
    if first_name not in ["⬅️ Ortga", "⬅️ Назад"]:
        await state.update_data(first_name=first_name)
    if language == 'uzb':
        text = ("👤 Pasportingiz bo'yicha familiyangizni kiriting\n"
                "(masalan: Baxodirov)")
        markup = back_or_main_default_keyboard_uzb
    else:
        text = ("👤 Введите фамилия по паспорту\n"
                "(пример:  Baxodirov)")
        markup = back_or_main_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.last_name.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.gender)
@dp.message_handler(state=ResumeState.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    last_name = message.text
    if last_name not in ["⬅️ Ortga", "⬅️ Назад"]:
        await state.update_data(last_name=last_name)
    if language == 'uzb':
        text = ("👤 Pasportingizdagi otangiz ismini kiriting\n"
                "(misol: Abdurashidovich)")
        markup = back_or_main_default_keyboard_uzb
    else:
        text = ("👤 Введите отчество по паспорту\n"
                "(пример:  Abdurashidovich)")
        markup = back_or_main_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.fathers_name.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.date_of_birth)
@dp.message_handler(state=ResumeState.fathers_name)
async def get_fathers_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    fathers_name = message.text
    if fathers_name not in ["⬅️ Ortga", "⬅️ Назад"]:
        await state.update_data(fathers_name=fathers_name)
    if language == 'uzb':
        text = "👨‍💼/👩‍🦰 Jinsingizni tanlang"
        markup = gender_default_keyboard_uzb
    else:
        text = "👨‍💼/👩‍🦰 Выберите пол"
        markup = gender_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.gender.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.location)
@dp.message_handler(state=ResumeState.gender)
async def get_gender(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    gender = message.text
    if gender not in ["⬅️ Ortga", "⬅️ Назад"]:
        if gender in ["👩 Ayol", "👩 Женщина", "👨 Erkak", "👨 Мужчина"]:
            gender = gender
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "‍👨‍💼/👩‍🦰 Jinsingizni tanlang" if language == 'uzb' else "👨‍💼/👩‍🦰 Выберите пол"
            markup = gender_default_keyboard_uzb if language == 'uzb' else gender_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(gender=gender)
    if language == 'uzb':
        text = "📅 Tug'ilgan kuningizni kiriting (masalan, dd.mm.yyyy):"
        markup = back_or_main_default_keyboard_uzb
    else:
        text = "📅 Укажите дату своего рождения (пример, дд.мм.гггг):"
        markup = back_or_main_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.date_of_birth.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.phone)
@dp.message_handler(state=ResumeState.date_of_birth)
async def get_date_of_birth(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    date_of_birth = message.text
    if date_of_birth not in ["⬅️ Ortga", "⬅️ Назад"]:
        if await validate_date(date_of_birth):
            await state.update_data(date_of_birth=date_of_birth)
        else:
            text1 = "❌To'g'ri ma'lumotlarni kiriting.❌" if language == "uzb" else "❌Введите правильные данные.❌"
            text2 = "📅 Tug'ilgan kuningizni kiriting (masalan, dd.mm.yyyy):" if language == "uzb" else "📅 Укажите дату своего рождения (пример, дд.мм.гггг):"
            markup = back_or_main_default_keyboard_uzb if language == "uzb" else back_or_main_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
    if language == 'uzb':
        text = "🏠 Yashash manzil (shahar, tuman, ko'cha/blok)"
        markup = back_or_main_default_keyboard_uzb
    else:
        text = "🏠 Адрес проживания (город, район, улица/квартал)"
        markup = back_or_main_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.location.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.email)
@dp.message_handler(state=ResumeState.location)
async def get_location(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    location = message.text
    if location not in ["⬅️ Ortga", "⬅️ Назад"]:
        await state.update_data(location=location)
    if language == 'uzb':
        text = "📱 Telefon raqamingizni kiriting (masalan: +998XXXXXXXXX):"
        markup = back_or_main_default_keyboard_uzb
    else:
        text = "📱 Укажите Ваш номер телефона (пример: +998XXXXXXXXX):"
        markup = back_or_main_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.phone.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.username)
@dp.message_handler(state=ResumeState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    phone = message.text
    if phone not in ["⬅️ Ortga", "⬅️ Назад"]:
        if await validate_phone_number(phone):
            await state.update_data(phone=phone)
        else:
            text1 = "❌To'g'ri ma'lumotlarni kiriting.❌" if language == "uzb" else "❌Введите правильные данные.❌"
            text2 = "📱 Telefon raqamingizni kiriting (masalan: +998XXXXXXXXX):" if language == "uzb" else "📱 Укажите Ваш номер телефона (пример: +998XXXXXXXXX):"
            markup = back_or_main_default_keyboard_uzb if language == "uzb" else back_or_main_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
    if language == 'uzb':
        text = "📥 Elektron pochta manzilingizni kiriting (google@gmail.com)"
        markup = back_or_main_default_keyboard_uzb
    else:
        text = "📥 Введите электронную почту (google@gmail.com)"
        markup = back_or_main_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.email.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.marital_status)
@dp.message_handler(state=ResumeState.email)
async def get_email(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    email = message.text
    if email not in ["⬅️ Ortga", "⬅️ Назад"]:
        if await validate_email(email):
            await state.update_data(email=email)
        else:
            text1 = "❌To'g'ri ma'lumotlarni kiriting.❌" if language == "uzb" else "❌Введите правильные данные.❌"
            text2 = "📥 Elektron pochta manzilingizni kiriting (google@gmail.com)" if language == "uzb" else "📥 Введите электронную почту (google@gmail.com)"
            markup = back_or_main_default_keyboard_uzb if language == "uzb" else back_or_main_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
    if language == 'uzb':
        text = "✏️ Telegramda username kiriting (@username)"
        markup = back_or_main_default_keyboard_uzb
    else:
        text = "✏️ Введите username в телеграме (@username)"
        markup = back_or_main_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.username.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.is_student)
@dp.message_handler(state=ResumeState.username)
async def get_username(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    username = message.text
    if username not in ["⬅️ Ortga", "⬅️ Назад"]:
        await state.update_data(username=username)
    if language == 'uzb':
        text = "💍 Oilaviy ahvolingiz:"
        markup = marital_status_default_keyboard_uzb
    else:
        text = "💍 Ваше семейное положение:"
        markup = marital_status_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.marital_status.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.education_form)
@dp.message_handler(state=ResumeState.marital_status)
async def get_marital_status(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    marital_status = message.text
    if marital_status not in ["⬅️ Ortga", "⬅️ Назад"]:
        if marital_status in ["Uylangan/erga tekkan", "Женат/замужем", "Uylanmagan/erga tegmagan",
                              "Не женат/не замужем", "Ajrashgan", "Разведен/Разведена", "Beva",
                              "Вдовец/Вдова"]:
            marital_status = marital_status
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "‍💍 Oilaviy ahvolingiz:" if language == 'uzb' else "💍 Ваше семейное положение:"
            markup = marital_status_default_keyboard_uzb if language == 'uzb' else marital_status_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(marital_status=marital_status)
    if language == 'uzb':
        text = "👨‍🎓 Siz hozir talabasizmi?"
        markup = yes_no_default_keyboard_uzb
    else:
        text = "👨‍🎓 Являетесь ли вы учеником , студентом в настоящее время?"
        markup = yes_no_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.is_student.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.education_level)
@dp.message_handler(state=ResumeState.is_student)
async def get_marital_is_student(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    is_student = message.text
    if is_student not in ["⬅️ Ortga", "⬅️ Назад"]:
        if is_student in ["Ha", "Да", "Yo'q", "Нет"]:
            is_student = is_student

        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "👨‍🎓 Siz hozir talabasizmi?" if language == 'uzb' else "👨‍🎓 Являетесь ли вы учеником , студентом в настоящее время?"
            markup = yes_no_default_keyboard_uzb if language == 'uzb' else yes_no_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(is_student=is_student)
        next_state = True
    else:
        is_student = data.get('is_student')
        next_state = False
    if is_student in ["Ha", "Да"]:
        if language == 'uzb':
            text = "📚 Ta'lim shaklini tanlang"
            markup = education_form_default_keyboard_uzb
        else:
            text = "📚 Выберите форму обучения"
            markup = education_form_default_keyboard_rus
        await message.answer(text=text, reply_markup=markup)
        await ResumeState.education_form.set()
    else:
        if next_state:
            if language == 'uzb':
                text = "🌐 Ta'lim darajangiz qanday?"
                markup = education_level_default_keyboard_uzb
            else:
                text = "🌐 Какой у вас уровень образования?"
                markup = education_level_default_keyboard_rus
            await message.answer(text=text, reply_markup=markup)
            await ResumeState.education_level.set()
        else:
            if language == 'uzb':
                text = "👨‍🎓 Siz hozir talabasizmi?"
                markup = yes_no_default_keyboard_uzb
            else:
                text = "👨‍🎓 Являетесь ли вы учеником , студентом в настоящее время?"
                markup = yes_no_default_keyboard_rus
            await message.answer(text=text, reply_markup=markup)
            await ResumeState.is_student.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.uzb_language_level)
@dp.message_handler(state=ResumeState.education_form)
async def get_education_form(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    education_form = message.text
    if education_form not in ["⬅️ Ortga", "⬅️ Назад"]:
        if education_form in ["Kunduzgi", "Очное", "Sirtqi", "Заочное", "Kechki",
                              "Вечернее", "Masofaviy", "Дистанционное"]:
            education_form = education_form
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "‍📚 Ta'lim shaklini tanlang" if language == 'uzb' else "📚 Выберите форму обучения"
            markup = education_form_default_keyboard_uzb if language == 'uzb' else education_form_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(education_form=education_form)
    if language == 'uzb':
        text = "🌐 Ta'lim darajangiz qanday?"
        markup = education_level_default_keyboard_uzb
    else:
        text = "🌐 Какой у вас уровень образования?"
        markup = education_level_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.education_level.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.rus_language_level)
@dp.message_handler(state=ResumeState.education_level)
async def get_education_level(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    education_level = message.text
    if education_level not in ["⬅️ Ortga", "⬅️ Назад"]:
        if education_level in ["O'rta", "Среднее", "O'rta maxsus", "Среднее-специальное", "Oliy",
                               "Высшее"]:
            education_level = education_level
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "‍🌐 Ta'lim darajangiz qanday?" if language == 'uzb' else "🌐 Какой у вас уровень образования?"
            markup = education_level_default_keyboard_uzb if language == 'uzb' else education_level_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(education_level=education_level)
    if language == 'uzb':
        text = "🇺🇿 O'zbek tilini bilish darajangiz qanday?"
        markup = language_level_default_keyboard_uzb
    else:
        text = "🇺🇿 Какой у Вас уровень узбекского языка?"
        markup = language_level_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.uzb_language_level.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.computer_level)
@dp.message_handler(state=ResumeState.uzb_language_level)
async def get_uzb_language_level(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    uzb_language_level = message.text
    if uzb_language_level not in ["⬅️ Ortga", "⬅️ Назад"]:
        if uzb_language_level in ["Past(tushunmayman va gapirmayman)",
                                  "Низкий (не понимаю и не говорю)",
                                  "O'rta(tushunaman, lekin yomon gapiraman)",
                                  "Средний (понимаю, но плохо говорю)",
                                  "Ilg'or(men ravon gapiraman va tushunaman)",
                                  "Продвинутый (свободно говорю и понимаю)",
                                  ]:
            uzb_language_level = uzb_language_level
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "‍🇺🇿 O'zbek tilini bilish darajangiz qanday?" if language == 'uzb' else "🇺🇿 Какой у Вас уровень узбекского языка?"
            markup = language_level_default_keyboard_uzb if language == 'uzb' else language_level_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(uzb_language_level=uzb_language_level)
    if language == 'uzb':
        text = "🇷🇺 Rus tilini bilish darajangiz qanday?"
        markup = language_level_default_keyboard_uzb
    else:
        text = "🇷🇺 Какой у Вас уровень русского языка?"
        markup = language_level_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.rus_language_level.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.expected_salary)
@dp.message_handler(state=ResumeState.rus_language_level)
async def get_rus_language_level(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    rus_language_level = message.text
    if rus_language_level not in ["⬅️ Ortga", "⬅️ Назад"]:
        if rus_language_level in ["Past(tushunmayman va gapirmayman)",
                                  "Низкий (не понимаю и не говорю)",
                                  "O'rta(tushunaman, lekin yomon gapiraman)",
                                  "Средний (понимаю, но плохо говорю)",
                                  "Ilg'or(men ravon gapiraman va tushunaman)",
                                  "Продвинутый (свободно говорю и понимаю)",
                                  ]:
            rus_language_level = rus_language_level
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "‍🇷🇺 Rus tilini bilish darajangiz qanday?" if language == 'uzb' else "🇷🇺 Какой у Вас уровень русского языка?"
            markup = language_level_default_keyboard_uzb if language == 'uzb' else language_level_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(rus_language_level=rus_language_level)
    if language == 'uzb':
        text = "🖥 Kompyuterni qanday darajada bilasiz?"
        markup = computer_level_default_keyboard_uzb
    else:
        text = "🖥 Какой у Вас уровень владения компьютером?"
        markup = computer_level_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.computer_level.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.photo)
@dp.message_handler(state=ResumeState.computer_level)
async def get_computer_level(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    computer_level = message.text
    if computer_level not in ["⬅️ Ortga", "⬅️ Назад"]:
        if computer_level in ["Bilmayman",
                              "Не владею", "O'rtacha daraja",
                              "Средний уровень", "Foydalanuvchi",
                              "Пользователь", "Mutaxasis",
                              "Эксперт"]:
            computer_level = computer_level
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "🖥 Kompyuterni qanday darajada bilasiz?" if language == 'uzb' else "🖥 Какой у Вас уровень владения компьютером?"
            markup = language_level_default_keyboard_uzb if language == 'uzb' else language_level_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(computer_level=computer_level)
    if language == 'uzb':
        text = "💵 Kutilayotgan ish haqi darajasini ko'rsating (so'm)"
        markup = expected_salary_default_keyboard_uzb
    else:
        text = "💵 Укажите ожидаемый уровень заработной платы (сум)"
        markup = expected_salary_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.expected_salary.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.source_about_vacancy)
@dp.message_handler(state=ResumeState.expected_salary)
async def get_expected_salary(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    expected_salary = message.text
    if expected_salary not in ["⬅️ Ortga", "⬅️ Назад"]:
        if expected_salary in ["1 mln dan 2.5 mln gacha",
                               "От 1 мл до 2.5 мл", "2.5 mln dan 4 mln gacha",
                               "От 2.5 млн до 4 млн", "4 mln dan 5.5 mln gacha",
                               "От 4 млн до 5.5 млн", "5.5 mln va undan ko'p",
                               "5.5 млн и больше"]:
            expected_salary = expected_salary
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "💵 Kutilayotgan ish haqi darajasini ko'rsating (so'm)" if language == 'uzb' else "💵 Укажите ожидаемый уровень заработной платы (сум)"
            markup = expected_salary_default_keyboard_uzb if language == 'uzb' else expected_salary_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(expected_salary=expected_salary)
    if language == 'uzb':
        text = "🤵 Suratingizni yuboring (telefoningizdan selfi olishingiz mumkin)"
        markup = back_or_main_default_keyboard_uzb
    else:
        text = "🤵 Отправьте Ваше фото (можно селфи с телефона)"
        markup = back_or_main_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.photo.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.agreement)
@dp.message_handler(state=ResumeState.photo, content_types=types.ContentType.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')

    photo = message.text
    if photo not in ["⬅️ Ortga", "⬅️ Назад"]:
        photo = message.photo[-1]
        file_id = photo.file_id
        await state.update_data(photo=file_id)
    if language == 'uzb':
        text = "❓ Vakansiya haqida qayerdan bildingiz?"
        markup = source_about_vacancy_default_keyboard_uzb
    else:
        text = "❓ Как Вы узнали о вакансии?"
        markup = source_about_vacancy_default_keyboard_rus
    await message.answer(text=text, reply_markup=markup)
    await ResumeState.source_about_vacancy.set()


@dp.message_handler(state=ResumeState.photo)
async def get_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
    text2 = "🤵 Suratingizni yuboring (telefoningizdan selfi olishingiz mumkin)" if language == 'uzb' else "🤵 Отправьте Ваше фото (можно селфи с телефона)"
    markup = back_or_main_default_keyboard_uzb if language == 'uzb' else back_or_main_default_keyboard_rus
    await message.answer(text=text1)
    await message.answer(text=text2, reply_markup=markup)


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.user)
@dp.message_handler(state=ResumeState.source_about_vacancy)
async def get_source_about_vacancy(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    source_about_vacancy = message.text
    if source_about_vacancy not in ["⬅️ Ortga", "⬅️ Назад"]:
        if source_about_vacancy in ["Instagram", "OLX", "hh.uz", "Telegram kanal",
                                    "Телеграм канал", "Do'stlar va tanishlar",
                                    "Друзья-знакомые", "ISHBORUZ_Elon", "Mahalla fuqarolar yig'ini",
                                    "Собрание граждан махалли", "Xokimiyat",
                                    "Buyurtmalar berish shaxobchasidagi elon",
                                    "Пункт выдачи заказов",
                                    "Биржа труда (Bandlik markazi)"]:
            source_about_vacancy = source_about_vacancy
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "❓ Vakansiya haqida qayerdan bildingiz?" if language == 'uzb' else "❓ Как Вы узнали о вакансии?"
            markup = source_about_vacancy_default_keyboard_uzb if language == 'uzb' else source_about_vacancy_default_keyboard_rus
            await message.answer(text=text1)
            await message.answer(text=text2, reply_markup=markup)
            return
        await state.update_data(source_about_vacancy=source_about_vacancy)
    if language == 'uzb':
        text = "Ommaviy ofera bilan tanishib chiqing"

        markup = agreement_default_keyboard_uzb
    else:
        text = "Ознакомиться с офертой"

        markup = agreement_default_keyboard_rus
    offer_url = "https://telegra.ph/Ishga-joylashishga-komaklashish-boyicha-xizmatlar-korsatish-uchun-oferta-01-14"
    await message.answer(
        f'<a href="{offer_url}" style="color:blue;"><b>{text}</b></a>',
        parse_mode=types.ParseMode.HTML, disable_web_page_preview=True, reply_markup=markup)
    await ResumeState.agreement.set()


@dp.message_handler(text=["⬅️ Ortga", "⬅️ Назад"], state=ResumeState.created_at)
@dp.message_handler(state=ResumeState.agreement)
async def get_agreement(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    agreement = message.text
    if agreement not in ["⬅️ Ortga", "⬅️ Назад"]:
        if agreement in ["✅ Oferta shartlariga roziman", "✅ Согласен с офертой"]:
            agreement = agreement
        else:
            text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
            text2 = "Ommaviy ofera bilan tanishib chiqing" if language == 'uzb' else "Ознакомиться с офертой"
            markup = agreement_default_keyboard_uzb if language == 'uzb' else agreement_default_keyboard_rus
            await message.answer(text=text1)
            offer_url = "https://telegra.ph/Ishga-joylashishga-komaklashish-boyicha-xizmatlar-korsatish-uchun-oferta-01-14"
            await message.answer(
                f'<a href="{offer_url}" style="color:blue;"><b>{text2}</b></a>',
                parse_mode=types.ParseMode.HTML, disable_web_page_preview=True, reply_markup=markup)
            return
        await state.update_data(agreement=agreement)
    region_id = data.get('region')
    regions = await db.select_region(id=region_id)
    region = regions[0]
    category_id = data.get('category')
    categories = await db.select_category(id=category_id)
    category = categories[0]
    branch_id = data.get('branch')
    branches = await db.select_branch(id=branch_id)
    branch = branches[0]
    vacancy_id = data.get('vacancy')
    vacancies = await db.select_vacancy(id=vacancy_id)
    vacancy = vacancies[0]
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    fathers_name = data.get('fathers_name')
    gender = data.get('gender')
    date_of_birth = data.get('date_of_birth')
    location = data.get('location')
    phone = data.get('phone')
    email = data.get('email')
    username = data.get('username')
    marital_status = data.get('marital_status')
    is_student = data.get('is_student')
    education_form = data.get('education_form')
    education_level = data.get('education_level')
    uzb_language_level = data.get('uzb_language_level')
    rus_language_level = data.get('rus_language_level')
    computer_level = data.get('computer_level')
    expected_salary = data.get('expected_salary')
    photo_id = data.get('photo')
    file_info = await bot.get_file(photo_id)
    source_about_vacancy = data.get('source_about_vacancy')

    text_uzb = (f"Viloyat: {region['name_uzb']}\n"
                f"Ish yo'nalishi: {category['title_uzb']}\n"
                f"📍Filial: {branch['title_uzb']}\n"
                f"Vakansiya: {vacancy['title_uzb']}\n"
                f"Ism: {first_name}\n"
                f"Familiya: {last_name}\n"
                f"Otangiz ismi: {fathers_name}\n"
                f"💢Jins: {gender}\n"
                f"Tug'ilgan kun: {date_of_birth}\n"
                f"Turar joy manzili: {location}\n"
                f"Telefon: {phone}\n"
                f"📥Elektron pochta: {email}\n"
                f"✏️Telegramdagi username: {username}\n"
                f"💍Oilaviy ahvolingiz: {marital_status}\n"
                f"👨‍🎓Talaba: {is_student}\n"
                f"📚Ta'lim shakli: {education_form}\n"
                f"🌐Ta'lim darajasi: {education_level}\n"
                f"O'zbek tili darajasi: {uzb_language_level}\n"
                f"Rus tili darajasi: {rus_language_level}\n"
                f"🖥 Kompyuterni qanday darajada bilasiz: {computer_level}\n"
                f"💵 Kutilayotgan ish haqi: {expected_salary}\n"
                f"🤵 Surat: {file_info.file_unique_id}.jpg\n"
                f"❓ Vakansiya haqida qanday eshitdingiz?: {source_about_vacancy}\n"
                f"Ommaviy oferta bilan tanishib chiqing: {agreement}")

    text_rus = (f"Регион: {region['name_rus']}\n"
                f"Выберите направление: {category['title_rus']}\n"
                f"📍Филиал: {branch['title_rus']}\n"
                f"Вакансия: {vacancy['title_rus']}\n"
                f"Имя: {first_name}\n"
                f"Фамилия: {last_name}\n"
                f"Очество: {fathers_name}\n"
                f"💢Пол: {gender}\n"
                f"Дата рождения: {date_of_birth}\n"
                f"Адрес проживание: {location}\n"
                f"Телефон: {phone}\n"
                f"📥Электронная почта: {email}\n"
                f"✏️Username в телеграме: {username}\n"
                f"💍Ваше семейное положение: {marital_status}\n"
                f"👨‍🎓Cтудент: {is_student}\n"
                f"📚Форма обучения: {education_form}\n"
                f"🌐Уровень образования: {education_level}\n"
                f"🇺🇿Уровень узбекского языка: {uzb_language_level}\n"
                f"🇷🇺Уровень русского языка: {rus_language_level}\n"
                f"🖥 Владения компьютером: {computer_level}\n"
                f"💵 Ожидаемый оклад: {expected_salary}\n"
                f"🤵 Фото: {file_info.file_unique_id}.jpg\n"
                f"❓ Откуда вы узнали о вакансии?: {source_about_vacancy}\n"
                f"Ознакомиться с офертой: {agreement}")
    text1 = text_uzb if language == 'uzb' else text_rus
    text2 = "Barcha ma'lumotlar to'g'ri to'ldirilganligini tasdiqlaysizmi?" if language == 'uzb' else "Подтверждаете ли Вы, что все данные были правильно заполнены?"
    markup = send_default_keyboard_uzb if language == 'uzb' else send_default_keyboard_rus

    await message.answer(text=text1)
    await message.answer(text=text2, reply_markup=markup)
    await ResumeState.user.set()


@dp.message_handler(state=ResumeState.user)
async def send_resume(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    send = message.text
    if send in ["⬅️ Ortga", "⬅️ Назад"]:
        if language == 'uzb':
            text = "Ommaviy ofera bilan tanishib chiqing"
            markup = agreement_default_keyboard_uzb
        else:
            text = "Ознакомиться с офертой"
            markup = agreement_default_keyboard_rus
        offer_url = "https://telegra.ph/Ishga-joylashishga-komaklashish-boyicha-xizmatlar-korsatish-uchun-oferta-01-14"
        await message.answer(
            f'<a href="{offer_url}" style="color:blue;"><b>{text}</b></a>',
            parse_mode=types.ParseMode.HTML, disable_web_page_preview=True, reply_markup=markup)
        await ResumeState.agreement.set()
        return
    elif send in ["⬆️ Yuborish", "⬆️Отправить"]:
        region_id = data.get('region')
        category_id = data.get('category')
        branch_id = data.get('branch')
        vacancy_id = data.get('vacancy')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        fathers_name = data.get('fathers_name')
        gender = data.get('gender')
        if gender in ["👩 Ayol", "👩 Женщина"]:
            gender = 'female'
        elif gender in ["👨 Erkak", "👨 Мужчина"]:
            gender = 'male'
        date_of_birth = data.get('date_of_birth')
        date_of_birth = datetime.strptime(date_of_birth, '%d.%m.%Y')
        location = data.get('location')
        phone = data.get('phone')
        email = data.get('email')
        username = data.get('username')
        marital_status = data.get('marital_status')
        if marital_status in ["Uylangan/erga tekkan", "Женат/замужем"]:
            marital_status = 'Uylangan/erga tekkan'
        elif marital_status in ["Uylanmagan/erga tegmagan", "Не женат/не замужем"]:
            marital_status = 'Uylanmagan/erga tegmagan'
        elif marital_status in ["Ajrashgan", "Разведен/Разведена"]:
            marital_status = 'Ajrashgan'
        elif marital_status in ["Beva", "Вдовец/Вдова"]:
            marital_status = 'Beva'
        is_student = data.get('is_student')
        if is_student in ["Ha", "Да"]:
            is_student = True
        elif is_student in ["Yo'q", "Нет"]:
            is_student = False
        education_form = data.get('education_form')
        if education_form in ["Kunduzgi", "Очное"]:
            education_form = 'Kunduzgi'
        elif education_form in ["Sirtqi", "Заочное"]:
            education_form = 'Sirtqi'
        elif education_form in ["Kechki", "Вечернее"]:
            education_form = 'Kechki'
        elif education_form in ["Masofaviy", "Дистанционное"]:
            education_form = 'Masofaviy'
        education_level = data.get('education_level')
        if education_level in ["O'rta", "Среднее"]:
            education_level = "O'rta"
        elif education_level in ["O'rta maxsus", "Среднее-специальное"]:
            education_level = "O'rta maxsus"
        elif education_level in ["Oliy", "Высшее"]:
            education_level = "Oliy"
        uzb_language_level = data.get('uzb_language_level')
        if uzb_language_level in ["Past(tushunmayman va gapirmayman)",
                                  "Низкий (не понимаю и не говорю)"]:
            uzb_language_level = "Past(tushunmayman va gapirmayman)"
        elif uzb_language_level in ["O'rta(tushunaman, lekin yomon gapiraman)",
                                    "Средний (понимаю, но плохо говорю)"]:
            uzb_language_level = "O'rta(tushunaman, lekin yomon gapiraman)"
        elif uzb_language_level in ["Ilg'or(men ravon gapiraman va tushunaman)",
                                    "Продвинутый (свободно говорю и понимаю)"]:
            uzb_language_level = "Ilg‘or(men ravon gapiraman va tushunaman)"
        rus_language_level = data.get('rus_language_level')
        if rus_language_level in ["Past(tushunmayman va gapirmayman)",
                                  "Низкий (не понимаю и не говорю)"]:
            rus_language_level = "Past(tushunmayman va gapirmayman)"
        elif rus_language_level in ["O'rta(tushunaman, lekin yomon gapiraman)",
                                    "Средний (понимаю, но плохо говорю)"]:
            rus_language_level = "O'rta(tushunaman, lekin yomon gapiraman)"
        elif rus_language_level in ["Ilg'or(men ravon gapiraman va tushunaman)",
                                    "Продвинутый (свободно говорю и понимаю)"]:
            rus_language_level = "Ilg'or(men ravon gapiraman va tushunaman)"
        computer_level = data.get('computer_level')
        if computer_level in ["Bilmayman",
                              "Не владею"]:
            computer_level = "Bilmayman"
        elif computer_level in ["O'rtacha daraja",
                                "Средний уровень"]:
            computer_level = "O'rtacha daraja"
        elif computer_level in ["Foydalanuvchi",
                                "Пользователь"]:
            computer_level = "Foydalanuvchi"
        elif computer_level in ["Mutaxasis",
                                "Эксперт"]:
            computer_level = "Mutaxasis"
        expected_salary = data.get('expected_salary')
        if expected_salary in ["1 mln dan 2.5 mln gacha",
                               "От 1 мл до 2.5 мл"]:
            expected_salary = "1 mln dan 2.5 mln gacha"
        elif expected_salary in ["2.5 mln dan 4 mln gacha",
                                 "От 2.5 млн до 4 млн"]:
            expected_salary = "2.5 mln dan 4 mln gacha"
        elif expected_salary in ["4 mln dan 5.5 mln gacha",
                                 "От 4 млн до 5.5 млн"]:
            expected_salary = "4 mln dan 5.5 mln gacha"
        elif expected_salary in ["5.5 mln va undan ko'p",
                                 "5.5 млн и больше"]:
            expected_salary = "5.5 mln va undan ko'p"

        photo_id = data.get('photo')

        file_info = await bot.get_file(photo_id)
        file_path = file_info.file_path
        file_name = os.path.join(PHOTO_DIR, f"{file_info.file_unique_id}.jpg")
        await bot.download_file(file_path, file_name)

        file_path = f'/photos/{file_info.file_unique_id}.jpg'
        source_about_vacancy = data.get('source_about_vacancy')
        if source_about_vacancy in ["Instagram"]:
            source_about_vacancy = "Instagram"
        elif source_about_vacancy in ["OLX"]:
            source_about_vacancy = "OLX"
        elif source_about_vacancy in ["hh.uz"]:
            source_about_vacancy = "hh.uz"
        elif source_about_vacancy in ["Telegram kanal",
                                      "Телеграм канал"]:
            source_about_vacancy = "Telegram kanal"
        elif source_about_vacancy in ["Do'stlar va tanishlar",
                                      "Друзья-знакомые"]:
            source_about_vacancy = "Do'stlar va tanishlar"
        elif source_about_vacancy in ["ISHBORUZ_Elon"]:
            source_about_vacancy = "ISHBORUZ_Elon"
        elif source_about_vacancy in ["Mahalla fuqarolar yig'ini",
                                      "Собрание граждан махалли"]:
            source_about_vacancy = "Mahalla fuqarolar yig'ini"
        elif source_about_vacancy in ["Xokimiyat"]:
            source_about_vacancy = "Xokimiyat"
        elif source_about_vacancy in ["Buyurtmalar berish shaxobchasidagi elon",
                                      "Пункт выдачи заказов"]:
            source_about_vacancy = "Buyurtmalar berish shaxobchasidagi elon"
        elif source_about_vacancy in ["Биржа труда (Bandlik markazi)"]:
            source_about_vacancy = "Биржа труда (Bandlik markazi)"
        agreement = data.get('agreement')
        if agreement in ["✅ Oferta shartlariga roziman", "✅ Согласен с офертой"]:
            agreement = "✅ Oferta shartlariga roziman"
        user_id = data.get('user_id')

        await db.create_resume(
            region_id=region_id,
            category_id=category_id,
            branch_id=branch_id,
            vacancy_id=vacancy_id,
            first_name=first_name,
            last_name=last_name,
            fathers_name=fathers_name,
            gender=gender,
            date_of_birth=date_of_birth,
            location=location,
            phone=phone,
            email=email,
            username=username,
            marital_status=marital_status,
            is_student=is_student,
            education_form=education_form,
            education_level=education_level,
            uzb_language_level=uzb_language_level,
            rus_language_level=rus_language_level,
            computer_level=computer_level,
            expected_salary=expected_salary,
            photo=file_path,
            source_about_vacancy=source_about_vacancy,
            user_id=user_id,
            agreement=agreement
        )
        text_uzb = ("Anketamizni to'ldirganingiz uchun tashakkur.\n"
                    "Biz sizning jamoamizga qo'shilish imkoniyatiga bo'lgan vaqtingiz va qiziqishingizni yuqori baholaymiz.\n"
                    "Sizning so'rovnomangiz muvaffaqiyatli qabul qilindi, siz ko'rib chiqish uchun nomzodlar ro'yxatiga kiritilgansiz.")
        text_rus = (
            "Благодарим вас за заполнение нашей анкеты. Мы высоко ценим ваше время и интерес к возможности присоединиться к нашей команде.\n"
            "Ваша анкета успешно получена, вы включены в список кандидатов на рассмотрение.")
        text = text_uzb if language == 'uzb' else text_rus
        markup = main_menu_default_keyboard_uzb if language == 'uzb' else main_menu_default_keyboard_rus
        await message.answer(text=text, reply_markup=markup)
        await state.finish()

    else:
        text1 = "Noto'g'ri ma'lumot kiritildi" if language == 'uzb' else "Введена неверная информация"
        text2 = "Barcha ma'lumotlar to'g'ri to'ldirilganligini tasdiqlaysizmi?" if language == 'uzb' else "Подтверждаете ли Вы, что все данные были правильно заполнены?"
        markup = send_default_keyboard_uzb if language == 'uzb' else send_default_keyboard_rus
        await message.answer(text=text1)
        await message.answer(text=text2, reply_markup=markup)
        return
