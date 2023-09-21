from aiogram.filters import CommandStart
from aiogram.methods import SendMessage
from aiogram.types import Message, CallbackQuery
from scm_bot.keyboards import DefaultMarkups, MyCallback
from aiogram import Router, F

menu_router = Router()
markups = DefaultMarkups()


@menu_router.message(CommandStart())
async def show_menu_handler(message: Message) -> None:
    await message.answer(text='Добро пожаловать!', reply_markup=markups.choose_city())


@menu_router.callback_query(lambda x: x.data == 'city')
async def show_cities(callback: CallbackQuery):
    print(1)
    await SendMessage(chat_id=callback.from_user.id, text='Вы выбрали город!', reply_markup=markups.show_cities())
