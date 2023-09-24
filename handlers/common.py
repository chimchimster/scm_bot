from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram import F
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Приветствую в боте! Чтобы заказать еду выполните /food,"
        " чтобы заказать напитки выполните /drinks",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command('cancel'))
@router.message(F.text.lower() == 'отмена')
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы отменили действие!',  reply_markup=ReplyKeyboardRemove())
