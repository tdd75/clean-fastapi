from sqlalchemy.orm import Session

from app.domain.repository import user_repository
from app.application.service import user_service


def execute(session: Session, user_id: int) -> None:
    user = user_service.read(session, user_id)
    return user_repository.delete(session, user)
