"""Валидаторы для API запросов."""

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.charity_project import CharityProject


async def check_name_unique(
    name: str,
    session: AsyncSession,
    exclude_id: int | None = None
) -> None:
    """Проверить уникальность имени проекта."""
    query = select(CharityProject).where(CharityProject.name == name)
    if exclude_id is not None:
        query = query.where(CharityProject.id != exclude_id)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!"
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверить существование проекта и вернуть его."""
    project = await session.get(CharityProject, project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Проект не найден"
        )
    return project


def check_project_not_closed(project: CharityProject) -> None:
    """Проверить, что проект не закрыт."""
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="Закрытый проект нельзя редактировать!"
        )


def check_project_not_invested(project: CharityProject) -> None:
    """Проверить, что в проект не были внесены средства."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!"
        )


def check_full_amount_valid(
    project: CharityProject,
    new_full_amount: int | None
) -> None:
    """Проверить корректность новой суммы."""
    if new_full_amount is not None:
        if new_full_amount < project.invested_amount:
            raise HTTPException(
                status_code=400,
                detail="Нельзя установить значение full_amount "
                "меньше уже вложенной суммы."
            )
