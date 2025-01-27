from uuid import uuid4

import pytest
from typing import Generator

from sqlalchemy import create_engine, StaticPool, Engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

from app.infrastructure.db.base import Base
from app import connection_pool, setting


@pytest.fixture(scope='session')
def _engine() -> Generator[Engine, None, None]:
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True)
def setup_test(_engine) -> Generator[None, None, None]:
    connection_pool.engine = _engine
    connection_pool.session_factory = scoped_session(
        sessionmaker(bind=connection_pool.engine, autocommit=False, autoflush=False, expire_on_commit=False)
    )
    Base.metadata.create_all(bind=connection_pool.engine)
    yield
    Base.metadata.drop_all(bind=connection_pool.engine)


@pytest.fixture(scope='session')
def _engine_pg() -> Generator[Engine, None, None]:
    default_engine = create_engine(setting.db_url.set(database='postgres'))
    db_test_name = f'db_test_{uuid4().hex}'
    with default_engine.connect() as connection:
        connection.execution_options(isolation_level='AUTOCOMMIT')
        connection.execute(text(f'CREATE DATABASE {db_test_name}'))
    engine = create_engine(setting.db_url.set(database=db_test_name))
    yield engine
    engine.dispose()
    with default_engine.connect() as connection:
        connection.execution_options(isolation_level='AUTOCOMMIT')
        connection.execute(text(f'DROP DATABASE {db_test_name} WITH (FORCE)'))
    default_engine.dispose()


@pytest.fixture
def setup_test_pg(_engine_pg) -> Generator[None, None, None]:
    """
    Fixture for tests that require PostgreSQL-specific behavior.

    Use this for test cases that cannot be accurately validated with SQLite,
    such as those involving:
    - Complex constraints or index behavior
    - JSONB, ARRAY, or other PostgreSQL-specific data types
    - Transactional behavior or isolation levels
    - Case-sensitive or collation-specific queries

    Ensures tests run against a real PostgreSQL instance for correctness.
    """

    connection_pool.engine = _engine_pg
    connection_pool.session_factory = scoped_session(
        sessionmaker(bind=connection_pool.engine, autocommit=False, autoflush=False, expire_on_commit=False)
    )
    Base.metadata.create_all(connection_pool.engine)
    yield
    Base.metadata.drop_all(connection_pool.engine)
