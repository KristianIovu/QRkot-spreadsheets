"""Модель целевого проекта."""

from sqlalchemy import Column, String, Text, Integer, CheckConstraint

from app.models.base import BaseModel
from app.core.constants import MAX_NAME_LENGTH


class CharityProject(BaseModel):
    """Модель целевого проекта фонда."""

    __tablename__ = "charityproject"

    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_amount_not_exceed_full_amount'
        ),
        CheckConstraint(
            'invested_amount >= 0',
            name='check_invested_amount_non_negative'
        ),
    )
