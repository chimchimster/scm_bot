from database import *
from utils import render_template


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
