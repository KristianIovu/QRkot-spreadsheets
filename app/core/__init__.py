"""Инициализация пакета core."""

from app.core.config import settings
from app.core.db import Base, engine, get_async_session
from app.core.user_manager import UserManager
from app.core.auth import auth_backend
from app.core.google_client import (
    get_google_services,
    create_spreadsheet,
    set_user_permissions,
    update_spreadsheet_value,
)

__all__ = [
    "settings",
    "Base",
    "engine",
    "get_async_session",
    "UserManager",
    "auth_backend",
    "get_google_services",
    "create_spreadsheet",
    "set_user_permissions",
    "update_spreadsheet_value",
]
