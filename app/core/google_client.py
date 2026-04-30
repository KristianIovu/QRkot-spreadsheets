"""Клиент для работы с Google API."""

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

# Ожидаемые переменные для тестов
INFO = {
    "type": settings.type,
    "project_id": settings.project_id,
    "private_key_id": settings.private_key_id,
    "private_key": settings.private_key,
    "client_email": settings.client_email,
    "client_id": settings.client_id,
    "auth_uri": settings.auth_uri,
    "token_uri": settings.token_uri,
    "auth_provider_x509_cert_url": settings.auth_provider_x509_cert_url,
    "client_x509_cert_url": settings.client_x509_cert_url,
}

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_service_account_creds() -> ServiceAccountCreds:
    """Формирование учётных данных сервисного аккаунта."""
    private_key = settings.private_key
    if isinstance(private_key, str):
        private_key = private_key.replace('\\n', '\n')
    return ServiceAccountCreds(
        scopes=SCOPES,
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


async def get_service():
    """Асинхронный генератор, возвращающий клиенты Google API."""
    creds = get_service_account_creds()
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        sheets = await aiogoogle.discover("sheets", "v4")
        drive = await aiogoogle.discover("drive", "v3")
        yield sheets, drive


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


async def set_user_permissions(aiogoogle, drive, file_id: str,
                               email: str) -> None:
    """Предоставление прав на редактирование таблицы."""
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": email,
    }
    await aiogoogle.as_service_account(
        drive.permissions.create(fileId=file_id, json=permissions_body,
                                 fields="id")
    )


async def update_spreadsheet_value(
    aiogoogle, sheets, spreadsheet_id: str, range_: str, values: list
) -> None:
    """Запись данных в Google таблицу."""
    body = {
        "majorDimension": "ROWS",
        "values": values,
    }
    await aiogoogle.as_service_account(
        sheets.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=range_,
            json=body,
            valueInputOption="USER_ENTERED",
        )
    )
