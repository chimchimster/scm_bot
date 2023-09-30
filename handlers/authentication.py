from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from states import Authentication as auth_state
from database import *

router = Router()


@router.message(Command(commands=['start']))
async def start_cmd(
        message: Message,
        state: FSMContext,
):
    user_name = message.from_user.username

    state_data = await state.get_data()
    state_level = state_data.get('state')

    if state_level == 'waiting_for_registration':
        print(state_level)
        register_button = InlineKeyboardButton(text=f'Зарегистрироваться как {user_name}?', callback_data='register')
        return_button = InlineKeyboardButton(text='Выйти')
        keyboard_markup = InlineKeyboardMarkup(
            inline_keyboard=[[register_button, return_button]]
        )

        await message.answer(f'Вы успешно зарегистрировались как {user_name}', reply_markup=keyboard_markup)

    elif state_level == 'waiting_for_authentication':

        authenticate_button = InlineKeyboardButton(text=f'Продолжить как {user_name}?', callback_data='authenticate')
        return_button = InlineKeyboardButton(text='Выйти')
        keyboard_markup = InlineKeyboardMarkup(
            inline_keyboard=[[authenticate_button, return_button]]
        )

        await message.answer(f'Вы авторизовались как {user_name}', reply_markup=keyboard_markup)

    elif state_level == 'available_for_purchases':

        await message.answer('Можете приступать к покупкам!')


