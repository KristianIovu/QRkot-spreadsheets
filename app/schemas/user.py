"""Схемы для пользователей."""

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для чтения информации о пользователе."""


class UserCreate(schemas.BaseUserCreate):
    """Схема для регистрации пользователя."""


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя."""
