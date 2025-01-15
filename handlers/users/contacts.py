from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db


@dp.message_handler(text=['📞Kontaktlar', '📞 Контакты'], state="*")
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
        caption = ("📲 Bizning kontaktlarimiz\n"
                   "+ 998 78 150 11 15")
    else:
        caption = ("📲Наши контакты\n"
                   "+ 998 78 150 11 15")

    file_id = "AgACAgIAAxkBAAMjZ4JaQfjRj-I1PSIJ5NbP1ELucz0AAmLxMRtgPBFI8HlCHqD5cvgBAAMCAAN4AAM2BA"
    await message.answer_photo(caption=caption, photo=file_id)
