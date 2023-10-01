from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_markup() -> InlineKeyboardMarkup:

    show_account_info_button = InlineKeyboardButton(text='К аккаунту', callback_data='to_account_handler')
    to_purchases_button = InlineKeyboardButton(text='К покупкам', callback_data='to_purchases_handler')
    exit_button = InlineKeyboardButton(text='Выйти', callback_data='exit')

    return InlineKeyboardMarkup(inline_keyboard=[[show_account_info_button, to_purchases_button, exit_button]])
