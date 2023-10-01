from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def register_markup() -> InlineKeyboardMarkup:

    register_button = InlineKeyboardButton(text=f'Да', callback_data='register_user_handler')
    exit_button = InlineKeyboardButton(text='Выйти', callback_data='exit')

    return InlineKeyboardMarkup(inline_keyboard=[[register_button, exit_button]])


def authenticate_markup() -> InlineKeyboardMarkup:

    authentication_button = InlineKeyboardButton(text='Да', callback_data='auth_user_handler')
    exit_button = InlineKeyboardButton(text='Выйти', callback_data='exit')

    return InlineKeyboardMarkup(inline_keyboard=[[authentication_button, exit_button]])

