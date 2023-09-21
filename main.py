import os
import asyncio

from aiogram.handlers import callback_query
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import DefaultMarkups


load_dotenv()
token = os.environ.get('TOKEN')
dp = Dispatcher()

builder = InlineKeyboardBuilder()
dp.callback_query.middleware(CallbackAnswerMiddleware())

bot = Bot(token=token, parse_mode=ParseMode.HTML)
builder.button(text=f"Выберите ваш город", callback_data=f"cities")

builder.adjust(3, 2)


# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#
#     await message.answer('hello from bot!', reply_markup=builder.as_markup())


@dp.message(Command('menu'))
async def menu_handler(message: Message) -> None:

    await message.answer('Добро пожаловать в главное меню!', reply_markup=DefaultMarkups.cancel_order())


@dp.callback_query(lambda call: call.data == 'cities')
async def cities(callback_query: CallbackQuery) -> None:
    buttons = [
        InlineKeyboardButton(text="Moscow", callback_data="district"),
        InlineKeyboardButton(text="New York", callback_data="new_york"),
        InlineKeyboardButton(text="Paris", callback_data="paris"),
        InlineKeyboardButton(text="London", callback_data="london")
    ]

    keyboard = InlineKeyboardBuilder()
    keyboard.add(*buttons)

    await bot.send_message(callback_query.from_user.id, "Выберите город:", reply_markup=keyboard.as_markup())


@dp.callback_query(lambda call: call.data == 'district')
async def district(callback_query: CallbackQuery) -> None:
    buttons = [
        InlineKeyboardButton(text='Пушкино', callback_data='items')
    ]

    keyboard = InlineKeyboardBuilder()
    keyboard.add(*buttons)

    await bot.send_message(callback_query.from_user.id, "Выберите район:", reply_markup=keyboard.as_markup())


async def main():

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())