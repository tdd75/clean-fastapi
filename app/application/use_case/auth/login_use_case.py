from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.application.service import auth_service
from app.application.service.password_service import verify_password
from app.presentation.dto.auth_dto import LoginDTO, TokenPairDTO
from app.domain.repository import user_repository


def execute(session: Session, dto: LoginDTO) -> TokenPairDTO:
    user = user_repository.find_by_email(session, dto.email)
    if not user:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'Invalid credentials')

    matched = verify_password(dto.password, user.password)
    if not matched:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'Invalid credentials')

    access, refresh = auth_service.generate_token_pair(user.id)
    return TokenPairDTO(access=access, refresh=refresh)
