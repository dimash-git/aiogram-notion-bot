from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    size = State()
    trade = State()
    leverage = State()
