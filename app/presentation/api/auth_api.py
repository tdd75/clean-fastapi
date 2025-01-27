from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session

from app.application.dto.auth_dto import LoginDTO, TokenPairDTO, RegisterDTO
from app.presentation.dependency.db import get_db
from app.application.use_case.auth import register_use_case, login_use_case

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/login/')
def login(
    session: Annotated[Session, Depends(get_db)],
    dto: Annotated[
        LoginDTO,
        Body(
            examples=[
                {
                    'email': 'user@example.com',
                    'password': 'password',
                }
            ]
        ),
    ],
) -> TokenPairDTO:
    return login_use_case.execute(session, dto)


@auth_router.post('/register/')
def register(
    session: Annotated[Session, Depends(get_db)],
    dto: Annotated[
        RegisterDTO,
        Body(
            examples=[
                {
                    'email': 'user@example.com',
                    'password': 'password',
                    'first_name': 'John',
                    'last_name': 'Doe',
                }
            ]
        ),
    ],
) -> TokenPairDTO:
    return register_use_case.execute(session, dto)
