from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import *
from database import *
from keyboards import *
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
        state: FSMContext,
):
    username = query.from_user.username
    user_id = query.from_user.id

    await get_personal_account_info(username, user_id)

    personal_account_info = await get_personal_account_info(username, user_id)

    await query.message.answer(text=personal_account_info)