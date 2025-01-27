import dotenv

from app.infrastructure.config.setting import Setting
from app.infrastructure.db.connection_pool import ConnectionPool
from app.infrastructure.config.logging import config_logging

dotenv.load_dotenv()
setting = Setting()
config_logging(setting)
connection_pool = ConnectionPool(setting.DB_URL)

__all__ = [
    'setting',
    'connection_pool',
]
