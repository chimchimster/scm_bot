from aiogram.fsm.state import StatesGroup, State


class AuthenticationState(StatesGroup):
    waiting_for_registration = State()
    waiting_for_authentication = State()
    available_for_purchases = State()
    register_new_user = State()
    authenticate_user = State()