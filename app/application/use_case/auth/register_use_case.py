from sqlalchemy.orm import Session

from app.presentation.dto.auth_dto import RegisterDTO, TokenPairDTO
from app.application.service.password_service import hash_password
from app.domain.entity.user import User
from app.domain.repository import user_repository
from app.application.service import user_service, auth_service


def execute(session: Session, dto: RegisterDTO) -> TokenPairDTO:
    user_service.validate_unique_email(session, dto.email)

    data = dto.model_dump(exclude_unset=True)
    user = User(**data)
    user.password = hash_password(dto.password)
    new_user = user_repository.create(session, user)
    auth_service.send_welcome_mail(new_user.email, new_user.first_name)
    access, refresh = auth_service.generate_token_pair(user.id)
    return TokenPairDTO(access=access, refresh=refresh)
