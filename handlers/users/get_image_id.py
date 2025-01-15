from aiogram import types

from loader import dp


@dp.message_handler(content_types=['photo'])
async def send_image_id(message: types.Message):
    photo = message.photo[-1]
    image_id = photo.file_id
    await message.reply(text=f"{image_id}")
