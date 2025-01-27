from dataclasses import dataclass

from decouple import config
from sqlalchemy import URL, make_url


@dataclass
class Setting:
    LOG_LEVEL: str = config('LOG_LEVEL', default='INFO')

    JWT_SECRET: str = config('JWT_SECRET')
    JWT_ACCESS_TOKEN_EXPIRES: int = config('JWT_ACCESS_TOKEN_EXPIRES', default=3600)
    JWT_REFRESH_TOKEN_EXPIRES: int = config('JWT_REFRESH_TOKEN_EXPIRES', default=86400 * 7)

    DB_URL: str = config('DB_URL')
    REDIS_URL: str = config('REDIS_URL', default='redis://localhost:6379/0')
    CELERY_BROKER_URL: str = config('CELERY_BROKER_URL', default='redis://localhost:6379/1')
    CELERY_RESULT_BACKEND: str = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/2')

    SMTP_HOST: str = config('SMTP_HOST', default='smtp.gmail.com')
    SMTP_PORT: int = config('SMTP_PORT', default=587, cast=int)
    SMTP_TLS: bool = config('SMTP_TLS', default=True, cast=bool)
    SMTP_USER: str | None = config('SMTP_USER', default=None)
    SMTP_PASSWORD: str | None = config('SMTP_PASSWORD', default=None)

    @property
    def db_url(self) -> URL:
        return make_url(self.DB_URL)
