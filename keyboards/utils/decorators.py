from functools import wraps
from typing import Callable

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def add_menu_markups(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> ReplyKeyboardMarkup:

        buttons: tuple[KeyboardButton] = func(*args, **kwargs)

        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    *buttons,
                ]
            ],
            resize_keyboard=True,
            selective=True,
        )

        return markup

    return wrapper
