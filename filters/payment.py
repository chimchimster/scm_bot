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

        has_unpaid_orders = await check_if_user_has_unpaid_orders(user_id)

        if has_unpaid_orders:

            await query.message.answer('У вас есть неоплаченный заказ. Оплатите либо откажитесь от оплаты')

        else:

            last_order = await get_last_order(user_id, item_id)

            order_has_been_expired = await check_if_order_expired(last_order)

            if order_has_been_expired:

                await set_order_expired(last_order)
                await state.set_state(PaymentState.order_expired_state)
                await query.message.answer('Заказ просрочен!')

            order_has_been_payed = await check_if_order_has_been_paid(last_order)

            if not order_has_been_payed:

                minutes_left = await order_minutes_left(last_order)

                await query.message.answer(f'Для оплаты заказа у вас осталось {minutes_left} минут. В противном случае, заказ будет отменен.')

            else:

                await state.set_state(PaymentState.order_paid_state)
                await query.message.answer('Заказ оплачен!', reply_markup=None)
