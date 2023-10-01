from typing import Union

from sqlalchemy import select, update, insert, delete, join, func

from models import *
from .signals import Signal
from .decorators import execute_transaction


@execute_transaction
async def create_item(
        item_title: str,
        description: str,
        image: bytes,
        price: float,
        quantity: int,
        category_title: str,
        **kwargs,
) -> Union[Item, Signal]:
    db_session = kwargs.pop('db_session')

    item = await db_session.execute(select(Item).filter_by(title=item_title))

    if item.scalar() is not None:
        return Signal.ITEM_EXISTS

    category = await db_session.execute(select(Category).filter_by(title=category_title))

    if category.scalar() is None:
        category = await db_session.execute(insert(Category(title=category_title)))

    new_item = Item(title=item_title, description=description, image=image, price=price, quantity=quantity)
    new_item.category = category

    await db_session.add(new_item)
    return new_item.scalar()


@execute_transaction
async def update_item(
        item_title: str,
        description: str = None,
        image: bytes = None,
        price: float = None,
        quantity: int = None,
        category_title: str = None,
        **kwargs
) -> Union[Item, Signal]:
    db_session = kwargs.pop('db_session')

    item = await db_session.execute(select(Item).filter_by(title=item_title))

    if item.scalar() is None:
        return Signal.USER_DOES_NOT_EXIST

    updated_values = {}

    if description is not None:
        updated_values['description'] = description
    if image is not None:
        updated_values['image'] = image
    if price is not None:
        updated_values['price'] = price
    if quantity is not None:
        updated_values['quantity'] = quantity

    updated_item = update(Item).filter_by(title=item_title).values(**updated_values).returning(Item)
    new_item = await db_session.execute(updated_item)

    if category_title:
        new_item.category = category_title

    return new_item.scalar()


@execute_transaction
async def delete_item(
        item_title: str,
        **kwargs,
) -> Union[Item, Signal]:
    db_session = kwargs.pop('db_session')

    item = await db_session.execute(select(Item).filter_by(title=item_title))

    if item.scalar() is not None:
        return Signal.USER_DOES_NOT_EXIST

    await db_session.execute(delete(Item).filter_by(title=item_title))

    return item.scalar()


@execute_transaction
async def show_all_items(**kwargs) -> Item:
    db_session = kwargs.pop('db_session')

    items = await db_session.execute(select(Item))

    result = items.fetchall()

    return result


@execute_transaction
async def show_items_count(**kwargs) -> int:
    db_session = kwargs.pop('db_session')

    items_count = await db_session.execute(select([func.count()]).select_from(Item))

    result = items_count.scalar()

    return result


@execute_transaction
async def show_sum_of_orders(paid=True, **kwargs) -> float:
    db_session = kwargs.pop('db_session')

    stmt = select(func.sum(Item.price)).select_from(
        join(Item, Order, Order.item_id == Item.id)
    ).where(Order.paid == paid)

    total_amount = await db_session.execute(stmt)

    return total_amount.scalar()
