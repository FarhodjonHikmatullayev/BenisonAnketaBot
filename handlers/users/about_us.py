from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db


@dp.message_handler(text=['🏢Biz haqimizda', '🏢 О нас'], state="*")
async def about_us_function(message: types.Message, state: FSMContext):
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
        caption = (
            "Uzum - O‘zbekistondagi o‘ziga xos kompaniya bo‘lib, mamlakatdagi birinchi texnologik xizmatlar ekotizimini tashkil etadi. Biz mamlakatimiz millionlab aholisiga cheksiz mahsulot turlarini tez yetkazib berish imkoniyatini ta’minlash, shuningdek, kundalik muammolarni hal qilish va biznesni rivojlantirishga ko‘maklashadigan moliyaviy xizmatlardan foydalanish uchun bir vaqtning o‘zida bir nechta yuqori texnologiyali mahsulotlarni rivojlantirmoqdamiz. Biz o‘zimizning IT-platformamizni qurmoqdamiz, yuz minglab tadbirkorlarni hamkorlikka jalb etgan holda logistika tizimini rivojlantirmoqdamiz.\n"
            "\n"
            "Uzum bilan innovatsiyalarga qo'shiling!")
    else:
        caption = (
            f"Uzum —  это уникальная компания в Узбекистане, первая технологичная экосистема сервисов в стране. Мы развиваем сразу несколько высокотехнологичных продуктов, чтобы у миллионов жителей страны был доступ к безграничному ассортименту товаров с быстрой доставкой, а также финансовые сервисы, помогающие в решении бытовых задачи и развитии бизнеса. Мы строим собственную IT-платформу, развиваем систему логистики, привлекая к сотрудничеству сотни тысяч предпринимателей.\n"
            f"\n"
            f"Подключайтесь к инновациям с Uzum!")

    file_id = "AgACAgIAAxkBAAMYZ4JYbh-C6ajEErFrWtTpGG6smrcAAk_xMRtgPBFIdNquZwjbpEkBAAMCAAN5AAM2BA"
    await message.answer_photo(caption=caption, photo=file_id)
