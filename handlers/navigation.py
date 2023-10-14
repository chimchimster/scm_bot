from aiogram import Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, Update

from states import *
from keyboards import *
from database import *
from .common import *
from filters import *
from callback_data import *


router = Router()


async def nav_menu_handler(
        message: Message,
):
    await message.answer(text='Сразу к покупкам?', reply_markup= await main_menu_markup())


@router.callback_query(
    NavigationState.main_menu_state,
    lambda callback_name: callback_name.data == 'to_account_handler'
)
async def to_account_handler(
        query: CallbackQuery,
        state: FSMContext,
):
    username = query.from_user.username
    user_id = query.from_user.id

    await get_personal_account_info(username, user_id)

    personal_account_info = await get_personal_account_info(username, user_id)

    await query.message.answer(text=personal_account_info)

    await state.update_data(callbacks_stack=[])


@router.callback_query(
    NavigationState.main_menu_state,
    lambda callback_name: callback_name.data == 'to_purchases_handler'
)
async def to_purchase_handler(query: CallbackQuery, state: FSMContext):

    await state.set_state(NavigationState.choose_city_state)

    await choose_city_handler(query, state)


@router.callback_query(
    lambda callback_name: callback_name.data == 'return_to_previous_callback'
)
async def return_to_previous_callback_handler(query: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    prev_callback = data.get('prev_callback')

    match prev_callback.split(':')[0]:
        case 'city':
            await state.set_state(NavigationState.main_menu_state)
            await choose_city_handler(query, state, prev_callback=prev_callback)
        case 'location':
            await state.set_state(NavigationState.choose_location_state)
            await choose_location_handler(query, state, prev_callback=prev_callback)
        case 'item':
            await state.set_state(NavigationState.choose_item_state)
            await choose_item_handler(query, state, prev_callback=prev_callback)
        case 'category':
            await state.set_state(NavigationState.choose_item_category_state)
            await choose_category_handler(query, state, prev_callback=prev_callback)


@router.callback_query(
    NavigationState.choose_city_state,
)
async def choose_city_handler(query: CallbackQuery, state: FSMContext, **kwargs):

    user_telegram_id = query.from_user.id

    user = await get_user(user_telegram_id)
    user_id = user.id

    await query.message.answer('Выберите город', reply_markup=await choose_city_markup())

    await state.update_data(user_id=user_id)
    await state.set_state(NavigationState.choose_location_state)


@router.callback_query(
    NavigationState.choose_location_state,
)
async def choose_location_handler(query: CallbackQuery, state: FSMContext, **kwargs):

    prev_callback = kwargs.get('prev_callback')

    if not prev_callback:
        callback_data = CityCallback.unpack(query.data)
        prev_callback = query.data
    else:
        callback_data = LocationCallback.unpack(prev_callback)

    city_id = callback_data.id
    city_title = callback_data.title

    await query.message.answer('Выберите локацию', reply_markup=await choose_location_markup(city_id))

    await state.update_data(city_id=city_id, city_title=city_title, prev_callback=prev_callback)
    await state.set_state(NavigationState.choose_item_state)


@router.callback_query(
    NavigationState.choose_item_state,
)
async def choose_item_handler(query: CallbackQuery, state: FSMContext, **kwargs):

    prev_callback = kwargs.get('prev_callback')

    if not prev_callback:
        callback_data = LocationCallback.unpack(query.data)
        prev_callback = query.data
    else:
        callback_data = ItemCallback.unpack(prev_callback)

    location_id = callback_data.id
    location_title = callback_data.title

    await query.message.answer('Выберите товар', reply_markup=await choose_item_markup(location_id))

    await state.update_data(location_id=location_id, location_title=location_title, prev_callback=prev_callback)
    await state.set_state(NavigationState.choose_item_category_state)


@router.callback_query(
    NavigationState.choose_item_category_state,
)
async def choose_category_handler(query: CallbackQuery, state: FSMContext, **kwargs):

    prev_callback = kwargs.get('prev_callback')

    if not prev_callback:
        callback_data = ItemCallback.unpack(query.data)
        prev_callback = query.data
    else:
        callback_data = CategoryCallback.unpack(prev_callback)

    item_id = callback_data.id
    item_title = callback_data.title

    await query.message.answer('Выберите категорию', reply_markup=await choose_category_markup(item_id))

    await state.update_data(item_id=item_id, item_title=item_title, prev_callback=prev_callback)
    await state.set_state(PaymentState.begin_order_state)


@router.callback_query(
    PaymentState.begin_order_state,
    BlockUnpaidOrderFilter(),
)
async def payment_start_handler(query: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    prev_callback = data.get('prev_callback')

    await state.update_data(prev_callback=prev_callback)

    current_state = await state.get_state()

    if current_state != PaymentState.last_order_has_not_been_paid:
        await state.set_state(PaymentState.create_order_state)
        await query.message.answer(text='Подтвердить выбор?', reply_markup=await confirm_choice_markup())


@router.callback_query(
    PaymentState.create_order_state,
    lambda callback_name: callback_name.data == 'confirm_choice',
)
async def create_order_handler(query: CallbackQuery, state: FSMContext):

    order_data = await state.get_data()
    user_telegram_id = query.from_user.id

    user_id = order_data.get('user_id')
    item_id = order_data.get('item_id')
    item_title = order_data.get('item_title')
    city_title = order_data.get('city_title')
    location_title = order_data.get('location_title')

    order_id = await create_order(user_id, item_id)

    order_info = await get_order_info(item_id, order_id, user_telegram_id)

    await state.update_data(
        order_id=order_id,
        user_id=user_id,
        item_title=item_title,
        city_title=city_title,
        location_title=location_title,
    )
    await state.set_state(PaymentState.order_created_state)
    await query.message.answer(text=order_info, reply_markup=await confirm_payment_markup())


@router.callback_query(
    PaymentSucceedFilter(),
    or_f(PaymentState.order_created_state, PaymentState.last_order_has_not_been_paid),
    lambda callback_name: callback_name.data == 'confirm_payment',
)
async def process_payment_handler(query: CallbackQuery, state: FSMContext):

    current_state = await state.get_state()

    if current_state == PaymentState.order_expired_state:
        await query.message.answer('Заказ просрочен!')
    elif current_state == PaymentState.order_paid_state:
        await query.message.answer('Заказ оплачен!')
    elif current_state == PaymentState.last_order_has_not_been_paid:

        data = await state.get_data()

        user_id = data.get('user_id')

        last_order = await get_last_order(user_id)

        minutes_left = await order_minutes_left(last_order)

        last_order_item = await get_item_by_order_id(last_order.id)

        await query.message.answer(f'У вас есть неоплаченный заказ {last_order_item.title}.\n\n'
                                   f'На сумму {round(last_order_item.price, 2)}₽\n\n'
                                   f'Для оплаты заказа у вас осталось {minutes_left} минут.\n\n'
                                   f'Оплатите заказ либо откажитесь от оплаты.',
                                   parse_mode='HTML',
                                   reply_markup=await confirm_payment_markup(),
                                   )


@router.callback_query(
    ClearLastOrderFilter(),
    lambda callback_name: callback_name.data == 'refuse_payment',
)
async def refuse_payment_handler(query: CallbackQuery, state: FSMContext):

    await state.set_state(NavigationState.main_menu_state)
    await query.message.answer('Вы отказались от заказа!')
    await nav_menu_handler(query.message)


