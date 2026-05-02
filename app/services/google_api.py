"""Сервис для работы с Google API."""

import copy
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

# Константы-заготовки для JSON-тел запросов
RENAME_SHEET_BODY_TEMPLATE = {
    "requests": [
        {
            "updateSheetProperties": {
                "properties": {"sheetId": 0, "title": None},
                "fields": "title",
            }
        }
    ]
}

PERMISSIONS_BODY_TEMPLATE = {
    "type": "user",
    "role": "writer",
    "emailAddress": None,
}

UPDATE_VALUES_BODY_TEMPLATE = {
    "majorDimension": "ROWS",
    "values": None,
}


def get_service_account_creds() -> ServiceAccountCreds:
    """Формирование учётных данных сервисного аккаунта."""
    private_key = settings.private_key
    if isinstance(private_key, str):
        private_key = private_key.replace('\\n', '\n')
    return ServiceAccountCreds(
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
        project_id=settings.project_id,
        private_key=private_key,
        client_email=settings.client_email,
        token_uri=settings.token_uri or "https://oauth2.googleapis.com/token",
    )


async def get_google_services():
    """Возвращает клиенты Aiogoogle, Google Sheets и Google Drive."""
    creds = get_service_account_creds()
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        sheets = await aiogoogle.discover("sheets", "v4")
        drive = await aiogoogle.discover("drive", "v3")
        return aiogoogle, sheets, drive


async def create_spreadsheet(aiogoogle, drive, title: str) -> str:
    """Создание Google таблицы через Drive API."""
    file_metadata = {
        "name": title,
        "mimeType": "application/vnd.google-apps.spreadsheet",
    }
    file = await aiogoogle.as_service_account(
        drive.files.create(json=file_metadata, fields="id")
    )
    return file["id"]


async def rename_sheet(aiogoogle, sheets, spreadsheet_id: str,
                       new_title: str) -> None:
    """Переименование первого листа таблицы."""
    # Глубокое копирование заготовки, чтобы не изменять оригинал
    body = copy.deepcopy(RENAME_SHEET_BODY_TEMPLATE)
    properties = body["requests"][0]["updateSheetProperties"]["properties"]
    properties["title"] = new_title

    await aiogoogle.as_service_account(
        sheets.spreadsheets.batchUpdate(spreadsheetId=spreadsheet_id,
                                        json=body)
    )


async def set_user_permissions(aiogoogle, drive, file_id: str,
                               email: str) -> None:
    """Предоставление прав на ред. таблицы указанному пользователю."""
    # Глубокое копирование заготовки, чтобы не изменять оригинал
    permissions_body = copy.deepcopy(PERMISSIONS_BODY_TEMPLATE)
    permissions_body["emailAddress"] = email

    await aiogoogle.as_service_account(
        drive.permissions.create(fileId=file_id, json=permissions_body,
                                 fields="id")
    )


async def update_spreadsheet_value(
    aiogoogle, sheets, spreadsheet_id: str, range_: str, values: list
) -> None:
    """Запись данных в Google таблицу."""
    # Глубокое копирование заготовки, чтобы не изменять оригинал
    body = copy.deepcopy(UPDATE_VALUES_BODY_TEMPLATE)
    body["values"] = values

    await aiogoogle.as_service_account(
        sheets.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=range_,
            json=body,
            valueInputOption="USER_ENTERED",
        )
    )
