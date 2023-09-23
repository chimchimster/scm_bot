import asyncio
import logging
from datetime import datetime
from random import randint
from typing import Optional
from aiogram import Bot, Dispatcher, types, html, F
from aiogram.filters.command import Command, CommandObject
from aiogram.types import BufferedInputFile, FSInputFile, URLInputFile, ReplyKeyboardMarkup
from aiogram.utils.markdown import hide_link
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from config_reader import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher()

user_data = {}

class NumberCallbackFactory(CallbackData, prefix='fabnum'):
    action: str
    value: Optional[int] = None


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='-2', callback_data=NumberCallbackFactory(action='change', value=-2)
    )
    builder.button(
        text='-1', callback_data=NumberCallbackFactory(action='change', value=-1)
    )

    builder.button(
            text='+1', callback_data=NumberCallbackFactory(action='change', value=+1)
        )
    builder.button(
            text='+2', callback_data=NumberCallbackFactory(action='change', value=+2)
        )

    builder.button(
        text='Подтвердить', callback_data=NumberCallbackFactory(action='finish')
    )
    builder.adjust(4)
    return builder.as_markup()



def get_keyboard():

    buttons = [
        [
            types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
            types.InlineKeyboardButton(text='-1', callback_data="num_decr")
        ],
        [types.InlineKeyboardButton(text="Конец", callback_data='num_finish')]
    ]

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=buttons,

    )

    return keyboard


@dp.message(Command('game'))
async def game_hdl(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer(text="Укажите число 0", reply_markup=get_keyboard_fab())


async def update_num_text(message: types.Message, num: int):

    await message.edit_text(f'Укажите число {num}', reply_markup=get_keyboard_fab())


@dp.callback_query(NumberCallbackFactory.filter(F.action == 'change'))
async def game_callback_change(callback: types.CallbackQuery, callback_data: NumberCallbackFactory):

    user_value = user_data.get(callback.from_user.id, 0)

    user_data[callback.from_user.id] = user_value + callback_data.value
    await update_num_text(callback.message, user_value + callback_data.value)
    await callback.answer()

@dp.callback_query(NumberCallbackFactory.filter(F.action == 'finish'))
async def game_callback_finish(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)

    await callback.message.edit_text(f'Ваше число: {user_value}')
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())