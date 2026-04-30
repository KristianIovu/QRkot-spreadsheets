"""Инициализация модуля маршрутов."""

from app.api.routes.charity_project import router as charity_project_router
from app.api.routes.donation import router as donation_router

__all__ = ["charity_project_router", "donation_router"]
