from scm_bot.dispatch import dp
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from scm_bot.keyboards import DefaultMarkups


@dp.message(CommandStart())
async def show_menu(message: Message) -> None:

    await message.answer(text='None', reply_markup=DefaultMarkups.message_choose_city())

