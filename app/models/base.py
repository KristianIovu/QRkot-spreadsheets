"""Базовые модели для всех таблиц."""

from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.core.db import Base


class BaseModel(Base):
    """Абстрактная базовая модель."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

    __table_args__ = (
        CheckConstraint(
            'invested_amount >= 0',
            name='check_invested_amount_non_negative'
        ),
    )
