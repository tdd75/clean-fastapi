from http import HTTPStatus

from fastapi import HTTPException

from app.application.context import IContext
from app.infrastructure.helper.jwt_helper import generate_token_pair
from app.infrastructure.helper.password_helper import verify_password
from app.application.dto.auth_dto import LoginDTO, TokenPairDTO
from app.domain.repository import user_repository


def execute(ctx: IContext, dto: LoginDTO) -> TokenPairDTO:
    user = user_repository.find_by_email(ctx.session, dto.email)
    if not user:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, ctx.t('Invalid credentials'))

    matched = verify_password(dto.password, user.password)
    if not matched:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, ctx.t('Invalid credentials'))

    access, refresh = generate_token_pair(user.id)
    return TokenPairDTO(access=access, refresh=refresh)
