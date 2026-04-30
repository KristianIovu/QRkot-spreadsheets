"""Модуль конфигурации приложения."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    # Название приложения.
    app_title: str = "Благотворительный фонд поддержки котиков QRKot"
    # URL для подключения к базе данных SQLite.
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    # Секретный ключ для JWT-токенов.
    secret: str = "SECRET_KEY_FOR_QRKOT"

    # Тип учётной записи (service_account).
    type: str = ""
    # ID проекта в Google Cloud.
    project_id: str = ""
    # Идентификатор приватного ключа.
    private_key_id: str = ""
    # Приватный ключ сервисного аккаунта.
    private_key: str = ""
    # Email сервисного аккаунта.
    client_email: str = ""
    # ID клиента сервисного аккаунта.
    client_id: str = ""
    # URI для авторизации Google.
    auth_uri: str = ""
    # URI для получения токена.
    token_uri: str = ""
    # URL сертификата x509 провайдера авторизации.
    auth_provider_x509_cert_url: str = ""
    # URL сертификата x509 клиента.
    client_x509_cert_url: str = ""
    # Личный email пользователя для доступа к таблице.
    email: str = ""

    class Config:
        """Настройки загрузки переменных из .env файла."""

        # Путь к файлу с переменными окружения.
        env_file = ".env"
        # Кодировка файла .env.
        env_file_encoding = "utf-8"
        # Разрешить игнорировать лишние поля в .env.
        extra = "ignore"


# Создаём глобальный объект настроек для импорта в другие модули
settings = Settings()
