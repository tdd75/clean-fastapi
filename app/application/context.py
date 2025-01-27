import logging
from typing import Protocol

from sqlalchemy.orm import Session

from app.domain.entity.user import User

logger = logging.getLogger(__name__)


class ITranslator(Protocol):
    def set_lang(self, lang: str) -> None: ...
    def translate(self, msg: str) -> str: ...


class IContext(Protocol):
    session: Session
    user: 'User | None'

    def authenticate(self, user: User) -> None: ...
    def set_lang(self, lang: str) -> None: ...
    def t(self, msg: str) -> str: ...
