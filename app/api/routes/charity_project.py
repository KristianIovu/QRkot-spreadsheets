"""Маршруты для работы с целевыми проектами."""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.dependencies import current_superuser
from app.crud import charity_project_crud
from app.models.donation import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB
)
from app.services.investment import distribute_funds
from app.api.validators import (
    check_name_unique,
    check_project_exists,
    check_project_not_closed,
    check_project_not_invested,
    check_full_amount_valid
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary="Получить все проекты",
    description="Показать список всех целевых проектов. "
    "Доступно всем пользователям."
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
) -> list[CharityProjectDB]:
    """Получить список всех целевых проектов."""
    return await charity_project_crud.get_all(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary="Создать проект",
    description="Создать целевой проект (только для суперпользователя).",
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Создать новый целевой проект."""
    await check_name_unique(project.name, session)

    new_project = await charity_project_crud.create(
        project.model_dump(),
        session
    )

    # Получаем неинвестированные пожертвования
    result = await session.execute(
        select(Donation).where(
            Donation.invested_amount < Donation.full_amount
        ).order_by(Donation.create_date)
    )
    donations = result.scalars().all()

    if donations:
        changed_donations = distribute_funds(new_project, donations)
        if changed_donations:
            session.add_all(changed_donations)

    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary="Обновить проект",
    description="Редактировать целевой проект (только для суперпользователя).",
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    project_update: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Обновить данные целевого проекта."""
    project = await check_project_exists(project_id, session)
    check_project_not_closed(project)

    if project_update.name is not None:
        await check_name_unique(project_update.name, session, project_id)

    if project_update.full_amount is not None:
        check_full_amount_valid(project, project_update.full_amount)
        project.full_amount = project_update.full_amount
        if project.full_amount == project.invested_amount:
            project.fully_invested = True
            project.close_date = datetime.now()

    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(project, field, value)

    await session.commit()
    await session.refresh(project)

    return project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    summary="Удалить проект",
    description="Удалить целевой проект (только для суперпользователя).",
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Удалить целевой проект."""
    project = await check_project_exists(project_id, session)
    check_project_not_invested(project)

    return await charity_project_crud.remove(project, session)
