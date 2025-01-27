import logging
from typing import Annotated, Generator

from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app import connection_pool
from app.application.use_case.auth import authenticate_use_case

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    with connection_pool.open_session() as session:
        yield session


def get_authenticated_db(
    token: Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer(auto_error=True))],
    session: Annotated[Session, Depends(get_db)],
) -> Generator[Session, None, None]:
    yield authenticate_use_case.execute(session, token.credentials)
