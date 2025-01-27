import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker, Session

logger = logging.getLogger(__name__)


class ConnectionPool:
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url, echo=False)
        self.session_factory = scoped_session(
            sessionmaker(bind=self.engine, autocommit=False, autoflush=False, expire_on_commit=False)
        )

    @contextmanager
    def open_session(self) -> Generator[Session, None, None]:
        session = self.session_factory()
        session.info.clear()
        try:
            yield session
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            logger.exception(exc)
            raise exc
        finally:
            session.close()
