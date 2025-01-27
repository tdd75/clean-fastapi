from http import HTTPStatus

from fastapi import HTTPException

from app.application.context import IContext
from app.domain.entity.user import User
from app.domain.repository import user_repository


def read(ctx: IContext, user_id: int) -> User:
    user = user_repository.find_by_id(ctx.session, user_id)
    if not user:
        raise HTTPException(HTTPStatus.NOT_FOUND, ctx.t('User ({user_id}) not found').format(user_id=user_id))
    return user


def validate_unique_email(ctx: IContext, email: str, exclude_id: int | None = None) -> None:
    user = user_repository.find_by_email(ctx.session, email)
    if user and user.id != exclude_id:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY, ctx.t('Email already exists'))
