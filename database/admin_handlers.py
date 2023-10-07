from typing import Union, Dict

from sqlalchemy import select, update, insert, delete, join, func
from sqlalchemy.ext.asyncio import AsyncSession

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


@execute_transaction
async def add_category(title: str, **kwargs) -> int:

    db_session = kwargs.pop('db_session')

    category_exists = await check_if_category_exists(title, db_session)

    if category_exists:
        return category_exists

    stmt = insert(Category).values(title=title)
    stmt = stmt.returning(Category.id)

    result = await db_session.execute(stmt)

    category_id = result.scalar()
    return category_id


async def check_if_category_exists(title: str, session: AsyncSession) -> Union[int, None]:

    stmt = select(Category.id).filter_by(title=title)
    result = await session.execute(stmt)

    category_id = result.scalar()
    return category_id


@execute_transaction
async def add_city(title: str, **kwargs) -> int:

    db_session = kwargs.pop('db_session')

    city_exists = await check_if_city_exists(title, db_session)

    if city_exists:
        return city_exists

    stmt = insert(City).values(title=title)
    stmt = stmt.returning(City.id)

    result = await db_session.execute(stmt)
    city_id = result.scalar()

    return city_id


async def check_if_city_exists(title: str, session: AsyncSession) -> Union[int, None]:

    stmt = select(City.id).filter_by(title=title)

    city = await session.execute(stmt)
    city = city.scalar()

    return city


@execute_transaction
async def add_location(title: str, **kwargs) -> int:

    db_session = kwargs.pop('db_session')

    location_exists = await check_if_location_exists(title, db_session)

    if location_exists:
        return location_exists

    stmt = insert(Location).values(title=title)
    stmt = stmt.returning(Location.id)

    result = await db_session.execute(stmt)
    location_id = result.scalar()

    return location_id


async def check_if_location_exists(title: str, session: AsyncSession) -> Union[int, bool]:

    stmt = select(Location.id).filter_by(title=title)

    location = await session.execute(stmt)
    location = location.scalar()

    if location:
        return location
    return False


@execute_transaction
async def add_item(data: Dict, **kwargs):

    db_session = kwargs.pop('db_session')

    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    quantity = data.get('quantity')
    image = bytes(data.get('image_bytes', b''))
    category_id = data.get('category_id')
    city_id = data.get('city_id')
    location_id = data.get('location_id')

    stmt = insert(Item).values(
        title=title,
        description=description,
        price=price,
        image=image,
        quantity=quantity,
    )
    stmt = stmt.returning(Item.id)

    result = await db_session.execute(stmt)
    item_id = result.scalar()

    item_category = ItemCategoryAssociation(item_id=item_id, category_id=category_id)
    item_city = ItemCityAssociation(city_id=city_id, item_id=item_id)
    city_location = CityLocationAssociation(city_id=city_id, location_id=location_id)

    db_session.add_all([item_city, city_location, item_category])