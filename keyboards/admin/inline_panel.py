from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def add_item_markup() -> InlineKeyboardMarkup:

    add_item_button = InlineKeyboardButton(text='Добавить товар', callback_data='add_item')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[add_item_button]]
    )

    return keyboard


def confirm_uploading_item() -> InlineKeyboardMarkup:

    confirm_uploading_item_button = InlineKeyboardButton(text='Подтвердить', callback_data='confirm_uploading_item')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[confirm_uploading_item_button]]
    )

    return keyboard