from aiogram.fsm.state import StatesGroup, State


class NavigationState(StatesGroup):
    main_menu_state = State()