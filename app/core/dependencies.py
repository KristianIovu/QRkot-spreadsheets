"""Зависимости для проверки прав доступа."""

from app.core.fastapi_users_setup import current_user, current_superuser

__all__ = ["current_user", "current_superuser"]
