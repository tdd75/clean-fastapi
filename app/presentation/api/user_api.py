from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.presentation.dependency.db import get_authenticated_db
from app.presentation.dto.user_dto import UserDTO, UserCreateDTO, UserListDTO, UserUpdateDTO
from app.application.use_case.user import (
    search_user_use_case,
    update_user_use_case,
    create_user_use_case,
    delete_user_use_case,
    get_user_use_case,
)

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.get('/')
def search_users(
    session: Annotated[Session, Depends(get_authenticated_db)],
    keyword: str | None = Query(None),
    email: str | None = Query(None),
    limit: int = Query(10),
    offset: int = Query(0),
) -> UserListDTO:
    return search_user_use_case.execute(
        session,
        keyword=keyword,
        email=email,
        limit=limit,
        offset=offset,
    )


@user_router.get('/{user_id}/')
def get_user(
    session: Annotated[Session, Depends(get_authenticated_db)],
    user_id: int,
) -> UserDTO:
    return get_user_use_case.execute(session, user_id)


@user_router.post('/', status_code=HTTPStatus.CREATED)
def create_user(
    session: Annotated[Session, Depends(get_authenticated_db)],
    dto: UserCreateDTO,
) -> UserDTO:
    return create_user_use_case.execute(session, dto)


@user_router.patch('/{user_id}/')
def update_user(
    session: Annotated[Session, Depends(get_authenticated_db)],
    user_id: int,
    dto: UserUpdateDTO,
) -> UserDTO:
    return update_user_use_case.execute(session, user_id, dto)


@user_router.delete('/{user_id}/', status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    session: Annotated[Session, Depends(get_authenticated_db)],
    user_id: int,
) -> None:
    return delete_user_use_case.execute(session, user_id)
