"""Главный модуль приложения QRKot."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import engine, Base
from app.api.routers import main_router
from app.api.routes.google import router as google_router
from app.api.routes.google import router as google_router
from app.core.fastapi_users_setup import fastapi_users
from app.core.auth import auth_backend
from app.schemas.user import UserRead, UserCreate, UserUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Благотворительный фонд поддержки котиков QRKot",
    description="Сервис для поддержки котиков",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры пользователей
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes
    if route.name != "delete_user"
]
app.include_router(users_router, prefix="/users", tags=["users"])

app.include_router(main_router)
app.include_router(google_router)


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {"message": "Добро пожаловать в QRKot!"}
