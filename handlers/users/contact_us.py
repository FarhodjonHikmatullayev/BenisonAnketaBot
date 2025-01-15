from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from keyboards.inline.reply_keyboard import reply_inline_keyboard, reply_callback_data
from loader import dp, db, bot
from states.contact_us_states import ContactUsStates


@dp.message_handler(text=["💭 Biz bilan bog'laning", "💭 Обратная связь"], state="*")
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
        text = "Bu yerda bizga yozing, biz albatta javob beramiz."
    else:
        text = "Напишите нам сюда, мы обязательно ответим."

    await ContactUsStates.message.set()
    await message.answer(text=text)


@dp.message_handler(state=ContactUsStates.message)
async def get_message_from_user(message: types.Message, state: FSMContext):
    admin_users = await db.select_users(role='admin')
    for admin in admin_users:
        markup = await reply_inline_keyboard(message_id=message.message_id, chat_id=message.chat.id)
        await bot.send_message(chat_id=admin['telegram_id'], text=message.text,
                               reply_markup=markup)
    await state.finish()


# @dp.message_handler(lambda message: message.chat.id == int(ADMINS) and message.reply_to_message)
@dp.callback_query_handler(reply_callback_data.filter(), state="*")
async def answer_to_user(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    message_id = callback_data.get('message_id')
    chat_id = callback_data.get('chat_id')
    user_telegram_id = call.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)

    if not users:
        full_name = call.from_user.full_name
        username = call.from_user.username
        user = await db.create_user(
            username=username,
            full_name=full_name,
            telegram_id=user_telegram_id
        )
        role = user['role']
    else:
        role = users[0]['role']
    if role == "user":
        return
    else:
        await ContactUsStates.reply.set()
        await state.update_data(chat_id=chat_id, message_id=message_id)
        await call.message.answer(text="Xabar jo'nating:")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.message_handler(state=ContactUsStates.reply)
async def reply_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chat_id = data.get('chat_id')
    message_id = data.get('message_id')
    await bot.send_message(
        chat_id=chat_id,
        text=message.text,
        reply_to_message_id=message_id
    )
    await message.reply(text="Yuborildi")
    await state.finish()
