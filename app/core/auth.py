"""Настройки аутентификации."""

from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from app.core.config import settings


cookie_transport = CookieTransport(cookie_name="qrkot", cookie_max_age=3600)

SECRET = settings.secret


def get_jwt_strategy() -> JWTStrategy:
    """Создание JWT стратегии."""
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
