import os
from typing import Dict

import aiofiles
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config_reader import bot_config
from states import *
from keyboards import *
from database import *


router = Router()


@router.message(Command(commands=['admin']))
async def admin_panel_handler(message: Message, state: FSMContext):

    user = message.from_user.username
    admin = bot_config.admin.get_secret_value()

    if user == admin:
        await state.set_state(AdminState.valid_admin_state)
        await message.answer(text='Добро пожаловать, admin!', reply_markup=add_item_markup())

    else:
        await message.answer(text='Доступ запрещен!')


@router.callback_query(AdminState.valid_admin_state, lambda callback_name: callback_name.data == 'add_item')
async def validated_admin_handler(query: CallbackQuery, state: FSMContext):

    await state.set_state(AddItemState.add_title_state)

    await query.message.answer(text='Введите название продукта')


@router.message(AddItemState.add_title_state)
async def add_title_handler(message: Message, state: FSMContext):

    title = message.text

    await state.update_data(title=title)

    await state.set_state(AddItemState.add_description_state)

    await message.answer(text='Введите описание продукта')


@router.message(AddItemState.add_description_state)
async def add_description_handler(message: Message, state: FSMContext):

    description = message.text

    await state.update_data(description=description)

    await state.set_state(AddItemState.add_price_state)

    await message.answer(text='Введите цену продукта')


@router.message(AddItemState.add_price_state)
async def add_price_handler(message: Message, state: FSMContext):

    price = message.text

    try:
        price = float(price)
    except TypeError:
        await message.answer(
            text='Цена продукта должна быть в числовом формате. Допускаются значения с плавающей точкой.'
        )
        return
    else:
        await state.update_data(price=price)

        await state.set_state(AddItemState.add_quantity_state)

        await message.answer('Введите количество продукта')


@router.message(AddItemState.add_quantity_state)
async def add_quantity_handler(message: Message, state: FSMContext):

    quantity = message.text
    try:
        quantity = int(quantity)
    except TypeError:
        await message.answer(
            text='Количество продукта должна быть в числовом формате. Значения с плавающей точкой не допускаются.'
        )
        return

    else:
        await state.update_data(quantity=quantity)

        await state.set_state(AddItemState.add_image_state)

        await message.answer('Загрузите изображение товара')


@router.message(AddItemState.add_image_state, F.photo)
async def add_image_handler(message: Message, state: FSMContext, bot: Bot):

    image = message.photo[-1]

    await bot.download(
        image,
        destination=f'temp_images/{image.file_id}.jpg'
    )

    async with aiofiles.open(f'temp_images/{image.file_id}.jpg', 'rb') as file:

        image_bytes = file.read()

        await state.update_data(image_bytes=image_bytes)

        await state.set_state(AddItemState.choose_city_state)

        await message.answer('Выберите город')

    os.remove(f'temp_images/{image.file_id}.jpg')


@router.message(AddItemState.choose_city_state)
async def choose_city_handler(message: Message, state: FSMContext):

    city = message.text.capitalize()

    city_id = await add_city(city)

    await state.update_data(city_id=city_id)

    await state.set_state(AddItemState.choose_location_state)

    await message.answer('Выберите локацию')


@router.message(AddItemState.choose_location_state)
async def choose_location_handler(message: Message, state: FSMContext):

    location = message.text.capitalize()

    location_id = await add_location(location)

    await state.update_data(location_id=location_id)

    await state.set_state(AddItemState.confirm_state)

    await message.answer(text='Загрузить товар', reply_markup=confirm_uploading_item())


@router.callback_query(AddItemState.confirm_state)
async def confirm_uploading_item_handler(query: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    print(data)

