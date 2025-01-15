from aiogram.dispatcher.filters.state import StatesGroup, State


class ContactUsStates(StatesGroup):
    message = State()
    reply = State()
