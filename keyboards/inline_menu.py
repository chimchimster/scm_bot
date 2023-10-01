from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_markup() -> InlineKeyboardMarkup:

    show_menu_button = InlineKeyboardButton(text='Показать меню', callback_data='show_menu')
    exit_button = InlineKeyboardButton(text='Выйти', callback_data='exit')

    return InlineKeyboardMarkup(inline_keyboard=[[show_menu_button, exit_button]])
