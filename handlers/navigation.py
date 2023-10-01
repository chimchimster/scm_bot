from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import *
from database import *
from utils import render_template

router = Router()

async def get_personal_account(telegram_id: int) -> str:


