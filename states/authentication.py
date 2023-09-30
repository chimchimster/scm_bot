from aiogram.fsm.state import StatesGroup, State


class Authentication(StatesGroup):
    waiting_for_registration = State()
    waiting_for_authentication = State()
    available_for_purchases = State()