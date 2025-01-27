from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url


class Setting(BaseSettings):
    model_config = SettingsConfigDict()

    LOG_LEVEL: str = Field('INFO')

    JWT_SECRET: str
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(1800)
    JWT_REFRESH_TOKEN_EXPIRES: int = Field(86400)

    DB_URL: str
    REDIS_URL: str = Field('redis://localhost:6379')
    CELERY_BROKER_URL: str = Field('redis://localhost:6379')
    CELERY_RESULT_BACKEND: str = Field('redis://localhost:6379')

    SMTP_HOST: str = Field('smtp.gmail.com')
    SMTP_PORT: int = Field(587)
    SMTP_TLS: bool = Field(True)
    SMTP_USER: str | None = Field(None)
    SMTP_PASSWORD: str | None = Field(None)

    @property
    def db_url(self) -> URL:
        return make_url(self.DB_URL)
