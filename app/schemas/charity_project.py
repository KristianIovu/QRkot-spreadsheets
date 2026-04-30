"""Pydantic схемы для целевых проектов."""

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.core.constants import (
    MAX_NAME_LENGTH,
    MIN_NAME_LENGTH,
    MIN_DESCRIPTION_LENGTH,
    MIN_FULL_AMOUNT
)


class CharityProjectCreate(BaseModel):
    """Схема для создания проекта."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=MIN_NAME_LENGTH,
                      max_length=MAX_NAME_LENGTH)
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: int = Field(..., gt=MIN_FULL_AMOUNT - 1)


class CharityProjectUpdate(BaseModel):
    """Схема для обновления проекта."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(None, min_length=MIN_NAME_LENGTH,
                             max_length=MAX_NAME_LENGTH)
    description: str | None = Field(None, min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: int | None = Field(None, gt=MIN_FULL_AMOUNT - 1)


class CharityProjectDB(CharityProjectCreate):
    """Схема проекта из базы данных."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None

    model_config = ConfigDict(from_attributes=True)
