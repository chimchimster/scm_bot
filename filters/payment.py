from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import *
from states import *
from keyboards import *


class PaymentSucceedFilter(BaseFilter):

    async def __call__(self, query: CallbackQuery, state: FSMContext):

        data = await state.get_data()

        user_id = data.get('user_id')

        last_order = await get_last_order(user_id)

        if last_order:

            order_has_been_expired = await check_if_order_expired(last_order)
            has_unpaid_order = await check_if_user_has_unpaid_order(user_id)

            if order_has_been_expired:

                await set_order_expired(last_order.id)

                await state.set_state(PaymentState.order_expired_state)

            elif has_unpaid_order:

                await state.set_state(PaymentState.last_order_has_not_been_paid)

            else:

                await state.set_state(PaymentState.order_paid_state)

        current_state = await state.get_state()

        return current_state


class BlockUnpaidOrderFilter(BaseFilter):
    async def __call__(self, query: CallbackQuery, state: FSMContext):

        data = await state.get_data()

        user_id = data.get('user_id')

        last_order = await get_last_order(user_id)

        if last_order:

            has_unpaid_order = await check_if_user_has_unpaid_order(user_id)

            if has_unpaid_order:

                minutes_left = await order_minutes_left(last_order)

                last_order_item = await get_item_by_order_id(last_order.id)

                await query.message.answer(f'У вас есть неоплаченный заказ {last_order_item.title}.\n\n'
                                           f'На сумму {round(last_order_item.price, 2)}₽\n\n'
                                           f'Для оплаты заказа у вас осталось {minutes_left} минут.\n\n'
                                           f'Оплатите заказ либо откажитесь от оплаты.',
                                           parse_mode='HTML',
                                           reply_markup=await confirm_payment_markup(),
                                           )

                await state.set_state(PaymentState.last_order_has_not_been_paid)

        current_state = await state.get_state()

        return current_state


class ClearLastOrderFilter(BaseFilter):

    async def __call__(self, query: CallbackQuery, state: FSMContext):

        data = await state.get_data()

        user_id = data.get('user_id')

        last_order = await get_last_order(user_id)

        if last_order:

            await set_order_expired(last_order.id)

        current_state = await state.get_state()

        return current_state