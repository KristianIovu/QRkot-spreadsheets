"""Pydantic схемы для пожертвований."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.core.constants import MIN_FULL_AMOUNT


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""

    full_amount: int = Field(..., gt=MIN_FULL_AMOUNT - 1)
    comment: str | None = None


class DonationCreate(DonationBase):
    """Схема для создания пожертвования."""

    model_config = ConfigDict(extra="forbid")


class DonationDB(DonationBase):
    """Схема пожертвования из базы данных (для пользователя)."""

    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    """Полная схема пожертвования для суперпользователя."""

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)