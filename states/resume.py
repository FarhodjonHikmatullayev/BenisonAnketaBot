from aiogram.dispatcher.filters.state import StatesGroup, State


class ResumeState(StatesGroup):
    region = State()
    category = State()
    branch = State()
    vacancy = State()
    first_name = State()
    last_name = State()
    fathers_name = State()
    gender = State()
    date_of_birth = State()
    location = State()
    phone = State()
    email = State()
    username = State()
    marital_status = State()
    is_student = State()
    education_form = State()
    education_level = State()
    uzb_language_level = State()
    rus_language_level = State()
    computer_level = State()
    expected_salary = State()
    photo = State()
    source_about_vacancy = State()
    agreement = State()
    user = State()
    created_at = State()
