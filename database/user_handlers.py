import time
import secrets
import hashlib

from typing import Final, Union

from sqlalchemy import select, update

from models import *
from .signals import Signal
from .decorators import execute_transaction


AUTH_TIME: Final[int] = 7200


@execute_transaction
async def get_user(
        telegram_id: int,
        **kwargs
) -> Union[User, None]:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(select(User).filter_by(telegram_id=telegram_id))

    if user.scalar() is not None:
        return user.scalar()
    return None


@execute_transaction
async def create_user(
        telegram_id: int,
        username: str,
        **kwargs,
) -> Union[User, Signal]:
    db_session = kwargs.pop('db_session')

    user = await get_user(telegram_id)

    if user is not None:
        return Signal.USER_EXISTS

    new_user = User(username=username, telegram_id=telegram_id)

    session_key = secrets.token_hex(32)
    auth_hash = hashlib.sha256(session_key.encode()).hexdigest()

    auth_session = Session(auth_hash=auth_hash, created_at_unix=int(time.time()))

    new_user.session = auth_session

    await db_session.add(new_user)
    await db_session.add(auth_session)

    return new_user.scalar()


@execute_transaction
async def user_is_authenticated(
        telegram_id: int,
        **kwargs,
) -> Union[bool, Signal]:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(select(User).filter_by(telegram_id=telegram_id))

    if user.scalar() is None:
        return Signal.USER_DOES_NOT_EXIST

    now = int(time.time())

    if now - user.session.created_at_unix > AUTH_TIME:
        return Signal.USER_DOES_NOT_AUTHORIZED

    return True


async def authenticate_user(
        telegram_id: int,
        **kwargs,
) -> Union[User, Signal]:
    db_session = kwargs.pop('db_session')

    user = await db_session.execute(select(User).filter_by(telegram_id=telegram_id))

    if user.scalar() is None:
        return Signal.USER_DOES_NOT_EXIST
    session_key = secrets.token_hex(32)
    auth_hash = hashlib.sha256(session_key.encode()).hexdigest()

    auth_session = Session(auth_hash=auth_hash, created_at_unix=int(time.time()))

    await db_session.execute(update(User).values(session=auth_session))

    return user.scalar()


