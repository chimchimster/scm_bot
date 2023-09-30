from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states import AuthenticationState
from database import *

router = Router()


async def get_auth_state(message: Message) -> AuthenticationState:
    telegram_id = message.from_user.id

    user = await get_user(telegram_id)

    if user == Signal.USER_EXISTS:
        is_authenticated = await user_is_authenticated(telegram_id)

        if is_authenticated:
            return AuthenticationState.available_for_purchases
        else:
            return AuthenticationState.waiting_for_authentication

    else:
        return AuthenticationState.waiting_for_registration


@router.message(CommandStart())
async def start_cmd(
        message: Message,
        state: FSMContext,
):
    user_name = message.from_user.username

    state_level = await get_auth_state(message)

    if state_level == AuthenticationState.waiting_for_registration:

        register_button = InlineKeyboardButton(text=f'Зарегистрироваться', callback_data='user_register')
        exit_button = InlineKeyboardButton(text='Выйти', callback_data='exit')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[register_button, exit_button]])

        await message.answer(f'Продолжить регистрацию как {user_name}?', reply_markup=keyboard)

        await state.set_state(AuthenticationState.register_new_user)


@router.callback_query(AuthenticationState.register_new_user, lambda callback_name: callback_name.data == 'user_register')
async def user_register(query: CallbackQuery, state: FSMContext):

    user_id = query.from_user.id
    username = query.from_user.username

    await create_user(user_id, username)

    await state.set_state(AuthenticationState.available_for_purchases)
