from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    valid_admin_state = State()


class AddItemState(StatesGroup):
    add_title_state = State()
    add_description_state = State()
    add_price_state = State()
    add_quantity_state = State()
    add_image_state = State()
    choose_city_state = State()
    choose_location_state = State()
    confirm_state = State()
