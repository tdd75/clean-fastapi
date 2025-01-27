from dataclasses import dataclass, field

from decouple import config
from sqlalchemy import URL, make_url


@dataclass
class Setting:
    LOG_LEVEL: str = field(default=config('LOG_LEVEL', default='INFO'))

    JWT_SECRET: str = field(default=config('JWT_SECRET'))
    JWT_ACCESS_TOKEN_EXPIRES: int = field(default=config('JWT_ACCESS_TOKEN_EXPIRES', default=3600))
    JWT_REFRESH_TOKEN_EXPIRES: int = field(default=config('JWT_REFRESH_TOKEN_EXPIRES', default=86400 * 7))

    DB_URL: str = field(default=config('DB_URL'))
    REDIS_URL: str = field(default=config('REDIS_URL', default='redis://localhost:6379/0'))
    CELERY_BROKER_URL: str = field(default=config('CELERY_BROKER_URL', default='redis://localhost:6379/1'))
    CELERY_RESULT_BACKEND: str = field(default=config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/2'))

    SMTP_HOST: str = field(default=config('SMTP_HOST', default='smtp.gmail.com'))
    SMTP_PORT: int = field(default=config('SMTP_PORT', default=587, cast=int))
    SMTP_TLS: bool = field(default=config('SMTP_TLS', default=True, cast=bool))
    SMTP_USER: str | None = field(default=config('SMTP_USER', default=None))
    SMTP_PASSWORD: str | None = field(default=config('SMTP_PASSWORD', default=None))

    SUPPORTED_LOCALES: list[str] = field(
        default_factory=lambda: config('SUPPORTED_LOCALES', default='en,vi').split(','),
    )
    DEFAULT_LOCALE: str = field(default=config('DEFAULT_LOCALE', default='en'))

    @property
    def db_url(self) -> URL:
        return make_url(self.DB_URL)
