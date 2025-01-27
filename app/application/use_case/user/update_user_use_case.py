from sqlalchemy.orm import Session

from app.domain.repository import user_repository
from app.application.service import user_service
from app.presentation.dto.user_dto import UserUpdateDTO, UserDTO


def execute(session: Session, user_id: int, dto: UserUpdateDTO) -> UserDTO:
    user = user_service.read(session, user_id)
    update_data = dto.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    updated_user = user_repository.update(session, user)
    return UserDTO.model_validate(updated_user)
