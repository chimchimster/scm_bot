from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def text_msg(message: Message):
    await message.answer('Это текстовое сообщение')

@router.message(F.text)
async def text_msg(message: Message):
    await message.answer('Это текстовое сообщение')

@router.message(F.sticker)
async def sticker_msg(message: Message):
    await message.answer('Это сообщение со стикером')

@router.message(F.gif)
async def text_msg(message: Message):
    await message.answer('Это gif сообщение')