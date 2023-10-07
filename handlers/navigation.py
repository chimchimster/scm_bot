from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import *
from database import *
from keyboards import *
from callback_data import *
from utils import render_template

from .common import get_personal_account_info

router = Router()


async def nav_menu_handler(
        message: Message,
):
    await message.answer(text='Сразу к покупкам?', reply_markup=main_menu_markup())


@router.callback_query(
    NavigationState.main_menu_state,
    lambda callback_name: callback_name.data == 'to_account_handler'
)
async def to_account_handler(
        query: CallbackQuery,
):
    username = query.from_user.username
    user_id = query.from_user.id

    await get_personal_account_info(username, user_id)

    personal_account_info = await get_personal_account_info(username, user_id)

    await query.message.answer(text=personal_account_info)


@router.callback_query(
    NavigationState.main_menu_state,
    lambda callback_name: callback_name.data == 'to_purchases_handler'
)
async def to_purchase_handler(query: CallbackQuery, state: FSMContext):

    await state.set_state(NavigationState.choose_city_state)

    await choose_city_handler(query, state)


@router.callback_query(
    NavigationState.choose_city_state,
)
async def choose_city_handler(query: CallbackQuery, state: FSMContext):

    await query.message.answer('Выберите город', reply_markup=await choose_city_markup())

    await state.update_data(prev_callback_data=query.data)
    await state.set_state(NavigationState.choose_location_state)


@router.callback_query(
    NavigationState.choose_location_state,
)
async def choose_location_handler(query: CallbackQuery, state: FSMContext):

    callback_data = CityCallback.unpack(query.data)
    city_id = callback_data.id

    await query.message.answer('Выберите локацию', reply_markup=await choose_location_markup(city_id))

    await state.update_data(prev_callback_data=callback_data)
    await state.set_state(NavigationState.choose_item_state)


@router.callback_query(
    lambda callback_name: callback_name.data == 'return_to_previous_callback'
)
async def return_to_previous_callback_handler(query: CallbackQuery, state: FSMContext):

    prev_callback_data = await state.get_data()

    prev_callback_data = prev_callback_data.get('prev_callback_data')

    if prev_callback_data.callback_name == 'city':
        await state.set_state(NavigationState.choose_city_state)
        await choose_city_handler(query, state)


