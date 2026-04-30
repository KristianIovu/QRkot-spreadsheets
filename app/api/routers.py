"""Общий роутер для API."""

from fastapi import APIRouter

from app.api.routes import charity_project, donation

main_router = APIRouter()

main_router.include_router(
    charity_project.router,
    prefix="/charity_project",
    tags=["charity_projects"]
)
main_router.include_router(
    donation.router,
    prefix="/donation",
    tags=["donations"]
)
