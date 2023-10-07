from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import *
from callback_data import *


def main_menu_markup() -> InlineKeyboardMarkup:

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