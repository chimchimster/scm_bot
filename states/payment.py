from aiogram.fsm.state import StatesGroup, State


class PaymentState(StatesGroup):
    begin_order_state = State()
    create_order_state = State()
    order_created_state = State()
    order_expired_state = State()
    last_order_has_not_been_paid = State()
    order_paid_state = State()
