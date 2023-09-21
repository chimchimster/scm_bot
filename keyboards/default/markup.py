from aiogram.types import KeyboardButton
from ..utils import add_menu_markups


class DefaultMarkups:
    message_return_back = 'Назад'
    message_confirm_order = 'Подтвердить заказ'
    message_cancel_order = 'Отменить заказ'
    message_choose_city = 'Выберите город'

    @classmethod
    @add_menu_markups
    def confirm_order(cls) -> tuple[KeyboardButton, KeyboardButton]:
        return_back_button = KeyboardButton(text=cls.message_return_back, callback_data='return')
        confirm_order_button = KeyboardButton(text=cls.message_confirm_order, callback_data='confirm')

        return return_back_button, confirm_order_button

    @classmethod
    @add_menu_markups
    def cancel_order(cls) -> tuple[KeyboardButton, KeyboardButton]:
        return_back_button = KeyboardButton(text=cls.message_return_back, callback_data='return')
        cancel_order_button = KeyboardButton(text=cls.message_cancel_order, callback_data='cancel')
        return return_back_button, cancel_order_button

    @classmethod
    @add_menu_markups
    def choose_city(cls) -> tuple[KeyboardButton, ...]:
        choose_city_button = KeyboardButton(text=cls.message_choose_city, callback_data='city')
        return (choose_city_button,)
