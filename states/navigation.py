from aiogram.fsm.state import StatesGroup, State


class NavigationState(StatesGroup):
    main_menu_state = State()
    choose_city_state = State()
    choose_location_state = State()
    choose_item_state = State()
    choose_item_category_state = State()


class PurchaseState(StatesGroup):
    waiting_for_payment_state = State()
    order_has_been_payed_state = State()
