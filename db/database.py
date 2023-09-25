from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config_reader import database_config


engine = create_async_engine(
    url=database_config.db_url.get_secret_value(),
)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)