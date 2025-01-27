from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.application.context import IContext
from app.presentation.dependency.context import get_context
from app.application.dto.user_dto import UserDTO, CreateUserDTO, UserListDTO, UpdateUserDTO
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
    ctx: Annotated[IContext, Depends(get_context())],
    keyword: str | None = Query(None),
    email: str | None = Query(None),
    limit: int = Query(10),
    offset: int = Query(0),
) -> UserListDTO:
    return search_user_use_case.execute(
        ctx,
        keyword=keyword,
        email=email,
        limit=limit,
        offset=offset,
    )


@user_router.get('/{user_id}/')
def get_user(
    ctx: Annotated[IContext, Depends(get_context())],
    user_id: int,
) -> UserDTO:
    return get_user_use_case.execute(ctx, user_id)


@user_router.post('/', status_code=HTTPStatus.CREATED)
def create_user(
    ctx: Annotated[IContext, Depends(get_context())],
    dto: CreateUserDTO,
) -> UserDTO:
    return create_user_use_case.execute(ctx, dto)


@user_router.patch('/{user_id}/')
def update_user(
    ctx: Annotated[IContext, Depends(get_context())],
    user_id: int,
    dto: UpdateUserDTO,
) -> UserDTO:
    return update_user_use_case.execute(ctx, user_id, dto)


@user_router.delete('/{user_id}/', status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    ctx: Annotated[IContext, Depends(get_context())],
    user_id: int,
) -> None:
    return delete_user_use_case.execute(ctx, user_id)
