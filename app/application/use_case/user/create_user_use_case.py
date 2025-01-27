from sqlalchemy.orm import Session

from app.presentation.dto.user_dto import UserCreateDTO, UserDTO
from app.application.service.password_service import hash_password
from app.domain.entity.user import User
from app.domain.repository import user_repository
from app.application.service import user_service


def execute(session: Session, dto: UserCreateDTO) -> UserDTO:
    user_service.validate_unique_email(session, dto.email)

    create_data = dto.model_dump(exclude_unset=True)
    user = User(**create_data)
    user.password = hash_password(dto.password)
    new_user = user_repository.create(session, user)
    return UserDTO.model_validate(new_user)
