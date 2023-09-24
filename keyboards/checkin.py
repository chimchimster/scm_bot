from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_kb_markup() -> InlineKeyboardMarkup:

    kb = InlineKeyboardBuilder()
    kb.button(text='Подтвердить', callback_data='confirm')

    return kb.as_markup()