"""Модель пожертвования."""

from sqlalchemy import Column, Text, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Donation(BaseModel):
    """Модель пожертвования пользователя."""

    __tablename__ = "donation"

    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="donations")

    __table_args__ = (
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_amount_not_exceed_full_amount'
        ),
    )
