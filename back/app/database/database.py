from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import DATABASE_URL as database_url
from config import SYNC_DATABASE_URL as sync_database_url

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    database_url,
    echo = False,
)

AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    expire_on_commit = False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

sync_engine = create_engine(sync_database_url)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)