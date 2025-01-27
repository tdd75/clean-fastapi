from sqlalchemy.orm import Session

from app.application.service import user_service
from app.presentation.dto.user_dto import UserDTO


def execute(session: Session, user_id: int) -> UserDTO:
    user = user_service.read(session, user_id)
    return UserDTO.model_validate(user)
