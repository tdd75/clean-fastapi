import pytest
from fastapi.testclient import TestClient
from typing import Generator

from app import connection_pool
from app.application.dto.user_dto import CreateUserDTO, UserDTO
from app.infrastructure.helper.jwt_helper import generate_token_pair
from app.main import app
from app.application.use_case.user import create_user_use_case
from app.presentation.dependency.context import AppContext


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app=app, base_url='http://localhost:8000/api/v1')


@pytest.fixture
def normal_user() -> UserDTO:
    with connection_pool.open_session() as session:
        ctx = AppContext(session)
        dto = CreateUserDTO(
            email='user@example.com',
            password='user_password',
            first_name='Normal',
            last_name='User',
            phone=None,
        )
        return create_user_use_case.execute(ctx, dto)


@pytest.fixture
def normal_user_client(client, normal_user) -> Generator[TestClient, None, None]:
    access, _ = generate_token_pair(normal_user.id)
    client.headers['Authorization'] = f'Bearer {access}'
    yield client


@pytest.fixture
def admin_user() -> UserDTO:
    with connection_pool.open_session() as session:
        ctx = AppContext(session)
        dto = CreateUserDTO(
            email='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            phone=None,
        )
        return create_user_use_case.execute(ctx, dto)


@pytest.fixture
def admin_user_client(client, admin_user) -> Generator[TestClient, None, None]:
    access, _ = generate_token_pair(admin_user.id)
    client.headers['Authorization'] = f'Bearer {access}'
    yield client
