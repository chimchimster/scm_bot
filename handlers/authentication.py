from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import *
from database import *
from keyboards import *
from .navigation import nav_menu_handler


router = Router()


@router.message(Command(commands=['run']))
async def start_cmd_handler(
        message: Message,
        state: FSMContext,
        **kwargs,
):

    user_name = message.from_user.username

    state_level = kwargs.get('auth_state')

    if state_level == AuthenticationState.waiting_for_registration:

        await message.answer(f'Продолжить регистрацию как {user_name}?', reply_markup=register_markup())

        await state.set_state(AuthenticationState.register_new_user)

    elif state_level == AuthenticationState.waiting_for_authentication:

        await message.answer(f'Авторизоваться как {user_name}?', reply_markup=authenticate_markup())

        await state.set_state(AuthenticationState.authenticate_user)

    elif state_level == AuthenticationState.available_for_purchases:

        await state.set_state(NavigationState.main_menu_state)

        await nav_menu_handler(message)


@router.callback_query(
    AuthenticationState.register_new_user,
    lambda callback_name: callback_name.data == 'register_user_handler',
)
async def register_user_handler(query: CallbackQuery, state: FSMContext):

    user_id = query.from_user.id
    username = query.from_user.username

    await create_user(user_id, username)

    await state.set_state(NavigationState.main_menu_state)

    await nav_menu_handler(query.message)


@router.callback_query(
    AuthenticationState.authenticate_user,
    lambda callback_name: callback_name.data == 'auth_user_handler',
)
async def auth_user_handler(query: CallbackQuery, state: FSMContext):

    user_id = query.from_user.id

    await authenticate_user(user_id)

    await state.set_state(NavigationState.main_menu_state)

    await nav_menu_handler(query.message)


@router.callback_query(lambda callback_name: callback_name.data == 'exit')
async def reset_state_handler(query: CallbackQuery, state: FSMContext):

    user_id = query.from_user.id

    await logout(user_id)

    await state.clear()
