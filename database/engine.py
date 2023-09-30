from sqlalchemy.ext.asyncio import create_async_engine

from models import Base


class EngineSQLite3:
    db_url = "sqlite+aiosqlite:///bot.db"
    engine = create_async_engine(db_url)

    async def create_bd_if_not_exists(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


engine_sqlite3 = EngineSQLite3()
