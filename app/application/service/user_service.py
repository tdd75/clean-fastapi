from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.domain.entity.user import User
from app.domain.repository import user_repository


def read(session: Session, user_id: int) -> User:
    user = user_repository.find_by_id(session, user_id)
    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, f'User ({user_id}) not found')
    return user


def validate_unique_email(session: Session, email: str, exclude_id: int | None = None) -> None:
    user = user_repository.find_by_email(session, email)
    if user and user.id != exclude_id:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY, 'Email already exists')
