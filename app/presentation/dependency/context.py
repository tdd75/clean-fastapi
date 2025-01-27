from dataclasses import dataclass, field
import logging
from typing import Callable

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.context import IContext, ITranslator
from app.domain.entity.user import User
from app.presentation.dependency.db import get_db, get_authenticated_db
from app.presentation.dependency.translator import Translator

logger = logging.getLogger(__name__)


@dataclass
class AppContext:
    session: Session
    user: 'User | None' = field(default=None)
    translator: ITranslator | None = field(default=None)

    def authenticate(self, user: User) -> None:
        self.user = user
        self.session.info['uid'] = user.id

    def set_lang(self, lang: str) -> None:
        if self.translator:
            self.translator.set_lang(lang)

    def t(self, msg: str) -> str:
        if not self.translator:
            return msg
        return self.translator.translate(msg)


def get_context(is_authenticated: bool = True) -> Callable[[Session, Translator], IContext]:
    def _get_context(
        session: Session = Depends(get_db if not is_authenticated else get_authenticated_db),
        translator: Translator = Depends(Translator),
    ) -> IContext:
        return AppContext(session=session, translator=translator)

    return _get_context
