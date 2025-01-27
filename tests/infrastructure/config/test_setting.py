from sqlalchemy.engine import URL
from app.infrastructure.config.setting import Setting


class TestSetting:
    def test_db_url_property(self):
        db_url_str = 'postgresql+psycopg://user:pass@localhost:5432/mydatabase'
        setting = Setting(DB_URL=db_url_str, JWT_SECRET='abc123')

        db_url = setting.db_url

        assert isinstance(db_url, URL)
        assert db_url.render_as_string(hide_password=False) == db_url_str

        # Optional: kiểm tra từng phần
        assert db_url.drivername == 'postgresql+psycopg'
        assert db_url.username == 'user'
        assert db_url.password == 'pass'
        assert db_url.host == 'localhost'
        assert db_url.port == 5432
        assert db_url.database == 'mydatabase'
