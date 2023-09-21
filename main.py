import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


load_dotenv()
token = os.environ.get('TOKEN')
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer('Макс привет!')


async def main():
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())