from typing import List

from aiogram import Router, F
from aiogram.types import Message

from filters.find_usernames import HasUsernamesFilter

router = Router()

@router.message(F.text, HasUsernamesFilter())
async def message_with_username(message: Message, usernames: List):
    await message.reply('Спасибо подпишусь на ' + ', '.join(usernames))
