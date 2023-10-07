from aiogram.fsm.state import StatesGroup, State


class PaymentState(StatesGroup):
    begin_order_state = State()
    create_order_state = State()
