"""Модуль для работы с базой данных."""

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base

from app.core.config import settings


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_async_session() -> AsyncSession:
    """Генератор асинхронных сессий базы данных."""
    async with AsyncSessionLocal() as session:
        yield session
