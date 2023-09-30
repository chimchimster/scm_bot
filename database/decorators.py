import sys
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .engine import engine_sqlite3

AsyncSessionLocal = sessionmaker(
    engine_sqlite3.engine, class_=AsyncSession, expire_on_commit=False
)


def execute_transaction(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        print(1)
        await engine_sqlite3.create_bd_if_not_exists()

        async with AsyncSessionLocal() as session:
            async with session.begin() as transaction:
                try:
                    await coro(*args, **kwargs, db_session=session)
                    await transaction.commit()
                except Exception as e:
                    await transaction.rollback()
                    sys.stderr.write(f'Транзакция завершилась неудачно: {e}')

    return wrapper
