from typing import Optional
from models import User

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .exceptions import UserIsNotExist


async def get_user_by_tg_id(
        session: AsyncSession,
        tg_id: int
) -> Optional[User]:
    stmt = select(User).where(User.telegram_id == tg_id)

    result = await session.execute(stmt)

    return result.fetchone()


async def get_user_by_id(
        session: AsyncSession,
        user_id: int,
) -> Optional[User]:

    stmt = select(User).where(User.id == user_id)

    result = await session.execute(stmt)

    return result.fetchone()


async def create_user(
        session: AsyncSession,
        tg_id: int,
        full_name: str,
        token: Optional[str] = None,
) -> Optional[User]:

    existed_user = await get_user_by_tg_id(session, tg_id)

    if existed_user is not None:
        raise UserIsNotExist(f'User {tg_id} is not exists!')

    is_authorized = token is not None

    user = User(
        telegram_id=tg_id,
        full_name=full_name,
        token=token,
        is_authorized=is_authorized,
    )

    session.add(user)
    await session.flush()
    await session.refresh(user)

    return user


async def update_user_token(
        session: AsyncSession,
        tg_id: int,
        token: Optional[str] = None
) -> Optional[User]:

    user = await get_user_by_tg_id(session, tg_id)

    if not user:
        raise UserIsNotExist(f'User {tg_id} is not exists!')

    is_authorized = token is not None

    stmt = update(User).values(is_authorized=is_authorized, token=token).where(User.telegram_id == tg_id)

    await session.execute(stmt)

    return await get_user_by_tg_id(session, user.telegram_id)


async def update_user(
        session: AsyncSession,
        user_id: int,
        tg_id: int,
        full_name: str
) -> Optional[User]:

    user = await get_user_by_id(session, user_id)

    if not user:
        raise UserIsNotExist(f'User {user_id} is not exists!')

    stmt = update(User).values(
        full_name=full_name,
    ).where(User.telegram_id == tg_id)

    await session.execute(stmt)

    return await get_user_by_id(session, user_id)


async def delete_user(
        session: AsyncSession,
        user_id: int
):
    user = await get_user_by_id(session, user_id)

    if not user:
        raise UserIsNotExist(f'User {user_id} is not exists!')

    stmt = delete(User).where(User.id == user_id)

    await session.execute(stmt)

    return
