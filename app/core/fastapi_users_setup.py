"""Настройка FastAPI Users."""

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.db import get_async_session
from app.core.user_manager import UserManager
from app.core.auth import auth_backend
from app.models.user import User


async def get_user_db(session=Depends(get_async_session)):
    """Получение базы данных пользователей."""
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    """Получение менеджера пользователей."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Зависимости для прав доступа
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
