"""Базовый CRUD класс."""

from typing import Any, TypeVar, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase:
    """Базовый класс для CRUD операций."""

    def __init__(self, model: Type[ModelType]):
        """Инициализация CRUD с указанием модели."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> ModelType | None:
        """Получить объект по ID."""
        return await session.get(self.model, obj_id)

    async def get_all(
        self,
        session: AsyncSession
    ) -> list[ModelType]:
        """Получить все объекты."""
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(
        self,
        obj_in: dict[str, Any],
        session: AsyncSession
    ) -> ModelType:
        """Создать новый объект."""
        obj = self.model(**obj_in)
        session.add(obj)
        await session.flush()
        return obj

    async def update(
        self,
        obj: ModelType,
        obj_in: dict[str, Any],
        session: AsyncSession
    ) -> ModelType:
        """Обновить объект."""
        for field, value in obj_in.items():
            if value is not None:
                setattr(obj, field, value)
        session.add(obj)
        await session.flush()
        return obj

    async def remove(
        self,
        obj: ModelType,
        session: AsyncSession
    ) -> ModelType:
        """Удалить объект."""
        await session.delete(obj)
        await session.commit()
        return obj
