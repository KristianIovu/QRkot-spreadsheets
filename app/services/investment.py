"""Сервис для распределения пожертвований по проектам."""

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


def distribute_funds(target, sources):
    """Распределяет средства между целевым объектом и источниками."""
    changed_objects = []

    for source in sources:
        target_free = target.full_amount - target.invested_amount
        source_free = source.full_amount - source.invested_amount
        invest_amount = min(target_free, source_free)

        if invest_amount <= 0:
            break

        for obj in (target, source):
            obj.invested_amount += invest_amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()

        changed_objects.append(source)

        if target.fully_invested:
            break

    return changed_objects


async def get_projects_by_completion_rate(session: AsyncSession):
    """Возвращает закрытые проекты, отсорт. по скорости сбора средств."""
    result = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(True),
            CharityProject.close_date.is_not(None)
        )
    )
    projects = result.scalars().all()

    for project in projects:
        delta = project.close_date - project.create_date
        project.completion_days = delta.days

    projects.sort(key=lambda x: x.completion_days)
    return projects
