from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import *
from states import *


class PaymentSucceedFilter(BaseFilter):

    async def __call__(self, query: CallbackQuery, state: FSMContext):

        data = await state.get_data()

        item_id = data.get('item_id')
        user_id = data.get('user_id')

        last_order = await get_last_order(user_id, item_id)

        order_has_been_expired = await check_if_order_expired(last_order)

        if order_has_been_expired:

            await set_order_expired(last_order)

            await state.set_state(PaymentState.order_expired_state)

        else:

            await state.set_state(PaymentState.order_paid_state)

        current_state = await state.get_state()

        return current_state


class BlockUnpaidOrderFilter(BaseFilter):
    async def __call__(self, query: CallbackQuery, state: FSMContext):

        data = await state.get_data()

        item_id = data.get('item_id')
        user_id = data.get('user_id')

        last_order = await get_last_order(user_id, item_id)

        has_unpaid_orders = await check_if_user_has_unpaid_orders(user_id)

        if has_unpaid_orders:

            order_has_been_payed = await check_if_order_has_been_paid(last_order)

            if not order_has_been_payed:

                minutes_left = await order_minutes_left(last_order)

                last_order_item = await get_item_by_order_id(last_order.id)

                await query.message.answer(f'У вас есть неоплаченный заказ {last_order_item.title}.\n\n'
                                           f'На сумму {last_order_item.price}\n\n'
                                           f'Для оплаты заказа у вас осталось {minutes_left} минут.\n\n'
                                           f'Оплатите заказ либо откажитесь от оплаты.', parse_mode='HTML')

            await state.set_state(PaymentState.last_order_has_not_been_paid)

        current_state = await state.get_state()

        return current_state
