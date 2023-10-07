import asyncio
import time
import secrets
import hashlib

from typing import Final, Union, List

from sqlalchemy import select, update, func, join, and_, Row, Sequence
from sqlalchemy.orm import joinedload

from models import *
from .signals import Signal
from .decorators import execute_transaction

AUTH_TIME: Final[int] = 1800


@execute_transaction
async def get_user(
        telegram_id: int,
        **kwargs
) -> User:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(select(User).filter_by(telegram_id=telegram_id))

    return user.scalar()


@execute_transaction
async def get_user_purchases_count(
        telegram_id: int,
        **kwargs,
) -> int:
    db_session = kwargs.pop('db_session')

    items_count = await db_session.execute(
        select(func.count()).where(
            and_(Order.user_id == telegram_id, Order.paid.is_(True))
        )
    )

    total = items_count.scalar()

    return total or 0


@execute_transaction
async def get_total_cost_of_purchased_items(
        telegram_id: int,
        **kwargs,
) -> float:

    db_session = kwargs.pop('db_session')

    items_price_count = await db_session.execute(
        select(func.sum(Item.price)).select_from(
            join(Order, Item, Order.item_id == Item.id).join(User, User.id == Order.user_id)
        ).where(and_(User.id == telegram_id, Order.paid.is_(True)))
    )

    total = items_price_count.scalar()

    return total or 0.0


@execute_transaction
async def user_exists(
        telegram_id: int,
        **kwargs
) -> Signal:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(select(User).filter_by(telegram_id=telegram_id))

    if user.scalar() is not None:
        return Signal.USER_EXISTS
    return Signal.USER_DOES_NOT_EXIST


@execute_transaction
async def create_user(
        telegram_id: int,
        username: str,
        **kwargs,
) -> User:
    db_session = kwargs.pop('db_session')

    new_user = User(username=username, telegram_id=telegram_id)

    session_key = secrets.token_hex(32)
    auth_hash = hashlib.sha256(session_key.encode()).hexdigest()

    auth_session = Session(auth_hash=auth_hash, created_at_unix=int(time.time()))

    new_user.session = auth_session

    db_session.add(new_user)

    return new_user


@execute_transaction
async def user_is_authenticated(
        telegram_id: int,
        **kwargs,
) -> Signal:
    db_session = kwargs.pop('db_session')

    result = await db_session.execute(
        select(User).filter_by(telegram_id=telegram_id).options(joinedload(User.session))
    )
    user = result.fetchone()
    now = int(time.time())

    session_unix_time = user[-1].session.created_at_unix
    is_expired = user[-1].session.expired

    if now - session_unix_time > AUTH_TIME or is_expired:
        return Signal.USER_DOES_NOT_AUTHORIZED

    return Signal.USER_AUTHORIZED


@execute_transaction
async def authenticate_user(
        telegram_id: int,
        **kwargs,
) -> User:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(select(User).filter_by(telegram_id=telegram_id))
    user = user.scalar()

    session_key = secrets.token_hex(32)
    auth_hash = hashlib.sha256(session_key.encode()).hexdigest()

    await db_session.execute(
        update(Session)
        .where(Session.user_id == user.id)
        .values(auth_hash=auth_hash, created_at_unix=int(time.time()), expired=False)
    )

    return user


@execute_transaction
async def logout(
        telegram_id: int,
        **kwargs,
) -> User:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(select(User).filter_by(telegram_id=telegram_id))
    user = user.scalar()

    await db_session.execute(update(Session).where(Session.user_id == user.id).values(expired=True))

    return user


@execute_transaction
async def restrict_user(
        telegram_id: int,
        **kwargs,
) -> User:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(update(User).filter_by(telegram_id=telegram_id).values(is_restricted=True))

    return user


@execute_transaction
async def user_is_restricted(
        telegram_id: int,
        **kwargs,
) -> Signal:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(select(User).filter_by(telegram_id=telegram_id))
    user = user.scalar()

    if user.is_restricted:
        return Signal.USER_IS_RESTRICTED
    return Signal.USER_IS_NOT_RESTRICTED


@execute_transaction
async def ban_user(
        telegram_id: int,
        **kwargs,
) -> User:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(update(User).filter_by(telegram_id=telegram_id).values(is_banned=True))

    return user


@execute_transaction
async def user_is_banned(
        telegram_id: int,
        **kwargs,
) -> Signal:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(select(User).filter_by(telegram_id=telegram_id))
    user = user.scalar()

    if user.is_blocked:
        return Signal.USER_IS_BANNED
    return Signal.USER_IS_NOT_BANNED


@execute_transaction
async def get_available_cities(**kwargs) -> Union[Sequence[Row[int, str]], List]:

    db_session = kwargs.pop('db_session')

    cities = await db_session.execute(select(City.id, City.title))
    cities = cities.fetchall()

    if cities:
        return cities
    return []


@execute_transaction
async def get_available_locations(city_id: int, **kwargs) -> Union[Sequence[Row[int, str]], List]:

    db_session = kwargs.pop('db_session')

    locations = await db_session.execute(
        select(Location.id, Location.title).select_from(
            join(City, Location, City.id == Location.city_id)
        ).where(City.id == city_id)
    )
    locations = locations.fetchall()

    if locations:
        return locations
    return []


@execute_transaction
async def get_available_items(location_id: int, **kwargs) -> Union[Sequence[Row[Item]], List]:

    db_session = kwargs.pop('db_session')

    items = await db_session.execute(
        select(Item).select_from(
            join(Item, City, Item.city_id == City.id).join(Location, City, Location.city_id == City.id)
        ).where(Location.id == location_id)
    ).all()

    items = items.fetchall()

    if items:
        return items
    return []
