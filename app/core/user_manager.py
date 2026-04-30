"""Менеджер для управления пользователями."""

from typing import Optional
from fastapi import Request, HTTPException

from fastapi_users import BaseUserManager, IntegerIDMixin

from app.models.user import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Класс для управления пользователями."""

    async def validate_password(self, password: str, user: User) -> None:
        """Проверка длины пароля."""
        if len(password) < 3:
            raise HTTPException(status_code=400, detail="Password too short")
        return await super().validate_password(password, user)

    async def on_after_register(self, user: User,
                                request: Optional[Request] = None):
        """Действия после регистрации пользователя."""
        print(f"Пользователь {user.email} зарегистрирован.")

    async def on_after_login(self, user: User,
                             request: Optional[Request] = None):
        """Действия после входа пользователя."""
        print(f"Пользователь {user.email} вошёл в систему.")
