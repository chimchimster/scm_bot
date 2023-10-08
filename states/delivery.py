from aiogram.fsm.state import StatesGroup, State


class DeliveryItemState(StatesGroup):
    available_for_delivery = State()
