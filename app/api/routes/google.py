"""Роутер для работы с Google Sheets."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.dependencies import current_superuser
from app.services.google_api import (
    get_google_services,
    create_spreadsheet,
    rename_sheet,
    set_user_permissions,
    update_spreadsheet_value,
)
from app.services.investment import get_projects_by_completion_rate
from app.core.config import settings

# Константа для формирования ссылки на Google таблицу
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/"

router = APIRouter(prefix="/google", tags=["Google"])


@router.post("/report/", dependencies=[Depends(current_superuser)])
async def get_report(
    session: AsyncSession = Depends(get_async_session),
):
    """Формирование отчёта о скорости закрытия проектов в Google Sheets."""
    aiogoogle, sheets, drive = await get_google_services()
    projects = await get_projects_by_completion_rate(session)

    spreadsheet_id = await create_spreadsheet(
        aiogoogle, drive, "Отчёт по скорости сбора средств"
    )
    await rename_sheet(aiogoogle, sheets, spreadsheet_id, "Закрытые проекты")
    await set_user_permissions(aiogoogle, drive, spreadsheet_id,
                               settings.email)

    table_values = [["Название проекта", "Время сбора (в днях)", "Описание"]]
    for project in projects:
        table_values.append([
            project.name,
            project.completion_days,
            project.description,
        ])

    await update_spreadsheet_value(
        aiogoogle, sheets, spreadsheet_id, "A:C", table_values
    )

    return {
        "message": "Отчёт создан",
        "spreadsheet_id": spreadsheet_id,
        "url": f"{GOOGLE_SHEETS_URL}{spreadsheet_id}",
    }
