from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboards


available_food_names = ["Суши", "Спагетти", "Хачапури"]
available_food_sizes = ["Маленькую", "Среднюю", "Большую"]
available_drink_names = ["Кола", "Пепси", "Sprite"]


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()

class OrderDrink(StatesGroup):
    choosing_drink_name = State()
    choosing_drink_size = State()



router = Router()


@router.message(Command('food'))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(text='Выберите блюдо', reply_markup=make_row_keyboards(available_food_names))

    await state.set_state(OrderFood.choosing_food_name)


@router.message(
    OrderFood.choosing_food_name,
    F.text.in_(available_food_names)
)
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer('Спасибо теперь выберите размер порции:', reply_markup=make_row_keyboards(available_food_sizes))

    await state.set_state(OrderFood.choosing_food_size)

@router.message(
    OrderFood.choosing_food_name,
)
async def incorrect_food_chosen(message: Message):

    await message.answer('Выберите блюдо из списка ниже', reply_markup=make_row_keyboards(available_food_names))


@router.message(
    OrderFood.choosing_food_size,
    F.text.in_(available_food_sizes),
)
async def size_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_size=message.text.lower())
    user_data = await state.get_data()

    await message.answer(f'Вы выбрали {user_data["chosen_food"]} с размером порации {user_data["chosen_size"]} Попробуйте теперь заказать напитки: /drinks',
                          reply_markup=ReplyKeyboardRemove())

    await state.clear()


@router.message(
    OrderFood.choosing_food_size
)
async def incorrect_size_chosen(message: Message):
    await message.answer('Выберите размер из списка', reply_markup=make_row_keyboards(available_food_sizes))





@router.message(Command('drinks'))
async def cmd_drinks(message: Message, state: FSMContext):

    await message.answer('Выберите напитки', reply_markup=make_row_keyboards(available_drink_names))
    await state.set_state(OrderDrink.choosing_drink_name)

@router.message(OrderDrink.choosing_drink_name, F.text.in_(available_drink_names))
async def chosen_drinks(message: Message, state: FSMContext):

    await state.update_data(chosen_drink=message.text.lower())

    await message.answer('Выберите размер напитка: ', reply_markup=make_row_keyboards(available_food_sizes))

    await state.set_state(OrderDrink.choosing_drink_size)

@router.message(OrderDrink.choosing_drink_name)
async def incorrect_chosen_drinks(message: Message):

    await message.answer('Выберите напиток из списка ниже!')


@router.message(OrderDrink.choosing_drink_size, F.text.in_(available_food_sizes))
async def chosen_drink_size(message: Message, state: FSMContext):

    await state.update_data(chosen_size=message.text.lower())
    user_data = await state.get_data()

    await message.answer(f'Вы выбрали напиток {user_data["chosen_drink"]} размером {user_data["chosen_size"]}', reply_markup=ReplyKeyboardRemove())

    await state.clear()


@router.message(OrderDrink.choosing_drink_size)
async def incorrect_chosen_sizes(message: Message):

    await message.answer('Выберите размер из списка ниже!')
