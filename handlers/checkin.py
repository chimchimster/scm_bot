from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.checkin import get_kb_markup
from middlewares.weekend import WeekendMessageMiddleware

router = Router()
router.message.filter(F.chat.type == 'private')
router.message.middleware(WeekendMessageMiddleware())

@router.message(Command('checkin'))
async def cmd_checkin(message: Message):
    await message.answer('Пожалуйста нажмите на кнопку ниже', reply_markup=get_kb_markup())


@router.callback_query(F.data == 'confirm')
async def confirm(callback: CallbackQuery):
    await callback.answer('Подтверждено', show_alert=True)