from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import *
from database import *
from keyboards import *
from utils import render_template

from .navigation import get_personal_account


router = Router()


async def get_auth_state(message: Message) -> AuthenticationState:
    telegram_id = message.from_user.id

    has_user = await user_exists(telegram_id)

    if has_user == Signal.USER_EXISTS:

        is_authenticated = await user_is_authenticated(telegram_id)

        if is_authenticated == Signal.USER_AUTHORIZED:
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

        await message.answer(f'Продолжить регистрацию как {user_name}?', reply_markup=register_markup())

        await state.set_state(AuthenticationState.register_new_user)

        st = await state.get_state()
        print(st)

    elif state_level == AuthenticationState.waiting_for_authentication:

        await message.answer(f'Авторизоваться как {user_name}?', reply_markup=authenticate_markup())

        await state.set_state(AuthenticationState.authenticate_user)

    elif state_level == AuthenticationState.available_for_purchases:

        text = await render_template('user_detail.html', user=user_name)

        await message.answer(text=text)

        await state.set_state(NavigationState.main_menu_state)


@router.message(AuthenticationState.available_for_purchases)
async def menu_nav_handler(
        message: Message,
        state: FSMContext,
        **kwargs,
):
    text = await render_template('user_detail.html')

    await message.answer(text=text)

    await message.answer(text='Главное меню')

    print("Хэндлер вызван и сообщения отправлены")


@router.callback_query(
    AuthenticationState.register_new_user,
    lambda callback_name: callback_name.data == 'register_user_handler',
)
async def register_user_handler(query: CallbackQuery, state: FSMContext):

    user_id = query.from_user.id
    username = query.from_user.username

    await create_user(user_id, username)

    await state.set_state(AuthenticationState.available_for_purchases)

    await query.message.answer()


@router.callback_query(
    AuthenticationState.authenticate_user,
    lambda callback_name: callback_name.data == 'auth_user_handler',
)
async def auth_user_handler(query: CallbackQuery, state: FSMContext):

    user_id = query.from_user.id

    await authenticate_user(user_id)

    await state.set_state(AuthenticationState.available_for_purchases)


@router.callback_query(lambda callback_name: callback_name.data == 'exit')
async def reset_state_handler(query: CallbackQuery, state: FSMContext):

    user_id = query.from_user.id

    await logout(user_id)

    await state.clear()