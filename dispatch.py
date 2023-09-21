import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


load_dotenv()
token = os.environ.get('TOKEN')
bot = Bot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
