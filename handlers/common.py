from typing import Union

from decimal import Decimal, getcontext

from database import *
from utils import render_template
from exchange_rates import get_latest_exchange_rate_on_pair_btc_rub


async def get_personal_account_info(
        username: str,
        telegram_id: int,
) -> str:

    bought_count = await get_user_purchases_count(telegram_id)
    total_cost_of_bought_count = await get_total_cost_of_purchased_items(telegram_id)

    text = await render_template(
        'user_detail.html',
        user=username,
        bought_count=bought_count,
        total_cost=total_cost_of_bought_count,
    )

    return text


async def get_order_info(
        item_id: int,
        order_id: int,
        telegram_id: int,
) -> Union[str, None]:

    item = await get_item(item_id)

    if not item:
        return

    user = await get_user(telegram_id)

    if not user:
        return

    category = await get_item_category(item_id)

    if not category:
        return

    exchange_rate_btc_rub = await get_latest_exchange_rate_on_pair_btc_rub()

    getcontext().prec = 10

    text = await render_template(
        'order_detail.html',
        id=order_id,
        username=user.username,
        title=item.title,
        category=category.title,
        total_cost=item.price,
        btc_price=Decimal(str(item.price)) / Decimal(str(exchange_rate_btc_rub))
    )

    return text


__all__ = [
    'get_personal_account_info',
    'get_order_info',
]
