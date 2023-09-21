import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()
token = os.environ.get('TOKEN')
dp = Dispatcher()

builder = InlineKeyboardBuilder()

for index in range(1, 11):
    builder.button(text=f"Set {index}", callback_data=f"set:{index}")

builder.adjust(3, 2)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer('hello from bot!', reply_markup=builder.as_markup())


async def main():
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())