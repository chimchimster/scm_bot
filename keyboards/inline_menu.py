from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import *
from callback_data import *


async def main_menu_markup() -> InlineKeyboardMarkup:

    show_account_info_button = InlineKeyboardButton(text='К аккаунту', callback_data='to_account_handler')
    to_purchases_button = InlineKeyboardButton(text='К покупкам', callback_data='to_purchases_handler')
    exit_button = InlineKeyboardButton(text='Выйти', callback_data='exit')

    return InlineKeyboardMarkup(inline_keyboard=[[show_account_info_button, to_purchases_button, exit_button]])


async def choose_city_markup() -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    cities = await get_available_cities()

    for item in cities:
        builder.button(text=item[1], callback_data=CityCallback(id=item[0], title=item[1]))

    builder.adjust(2, 3, repeat=True)

    return builder.as_markup()


async def choose_location_markup(city_id: int) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    locations = await get_available_locations(city_id)

    for item in locations:
        builder.button(text=item[1], callback_data=LocationCallback(id=item[0], title=item[1]))

    return_to_previous_callback_button = InlineKeyboardButton(text='Назад', callback_data='return_to_previous_callback')
    builder.add(return_to_previous_callback_button)

    builder.adjust(2, 3, repeat=True)
    return builder.as_markup()


async def choose_item_markup(location_id: int) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    items = await get_available_items(location_id)

    for item in items:
        builder.button(text=item[1], callback_data=ItemCallback(id=item[0], title=item[1]))

    return_to_previous_callback_button = InlineKeyboardButton(text='Назад', callback_data='return_to_previous_callback')
    builder.add(return_to_previous_callback_button)

    builder.adjust(2, 3, repeat=True)
    return builder.as_markup()


async def choose_category_markup(item_id: int) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    categories = await get_available_categories(item_id)

    for item in categories:
        builder.button(text=item[1], callback_data=CategoryCallback(id=item[0], title=item[1]))

    return_to_previous_callback_button = InlineKeyboardButton(text='Назад', callback_data='return_to_previous_callback')
    builder.add(return_to_previous_callback_button)

    builder.adjust(2, 3, repeat=True)
    return builder.as_markup()


async def confirm_choice_markup() -> InlineKeyboardMarkup:

    confirm_choice_button = InlineKeyboardButton(text='Да', callback_data='confirm_choice')
    refuse_choice_button = InlineKeyboardButton(text='Назад', callback_data='return_to_previous_callback')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[confirm_choice_button, refuse_choice_button]]
    )

    return keyboard


async def confirm_payment_markup() -> InlineKeyboardMarkup:

    confirm_payment_button = InlineKeyboardButton(text='Я оплатил', callback_data='confirm_payment')
    refuse_payment_button = InlineKeyboardButton(text='Отказаться', callback_data='refuse_payment')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[confirm_payment_button, refuse_payment_button]]
    )

    return keyboard
