from http import HTTPStatus


import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.helper.jwt_helper import decode_token
from app.domain.repository import user_repository


def execute(session: Session, token: str) -> Session:
    try:
        claims = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'Token has expired')
    except (jwt.InvalidTokenError, jwt.DecodeError):
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'Invalid token')

    user = user_repository.find_by_id(session, int(claims.sub))
    if not user:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, 'User not found')

    session.info['uid'] = user.id
    return session
