from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

reply_callback_data = CallbackData('reply', 'chat_id', 'message_id')


async def reply_inline_keyboard(message_id, chat_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Reply',
                    callback_data=reply_callback_data.new(
                        chat_id=chat_id,
                        message_id=message_id
                    )
                )
            ]
        ]
    )
    return markup
