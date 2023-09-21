import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

token = os.environ.get('TOKEN')
bot = Bot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
