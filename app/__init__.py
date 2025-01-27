from app.infrastructure.config.setting import Setting
from app.infrastructure.config.logging import config_logging
from app.infrastructure.config.celery import config_celery
from app.infrastructure.db.connection_pool import ConnectionPool

setting = Setting()
config_logging(setting)
celery_app = config_celery(setting)
connection_pool = ConnectionPool(setting.DB_URL)

__all__ = [
    'setting',
    'celery_app',
    'connection_pool',
    'translation',
]
