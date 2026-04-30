"""Инициализация пакета models."""

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.base import BaseModel
from app.models.user import User

__all__ = ["CharityProject", "Donation", "BaseModel", "User"]
