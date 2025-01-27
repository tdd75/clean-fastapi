import pytest
from fastapi.testclient import TestClient
from typing import Generator

from app import connection_pool
from app.presentation.dto.user_dto import UserCreateDTO, UserDTO
from app.main import app
from app.application.service import auth_service
from app.application.use_case.user import create_user_use_case


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app=app, base_url='http://localhost:8000/api/v1')


@pytest.fixture
def normal_user() -> UserDTO:
    with connection_pool.open_session() as session:
        dto = UserCreateDTO(
            email='normal_user@example.com',
            password='normal_user',
            first_name='Normal',
            last_name='User',
            phone=None,
        )
        return create_user_use_case.execute(session, dto)


@pytest.fixture
def normal_user_client(client, normal_user) -> Generator[TestClient, None, None]:
    access, _ = auth_service.generate_token_pair(normal_user.id)
    client.headers['Authorization'] = f'Bearer {access}'
    yield client


@pytest.fixture
def admin_user() -> UserDTO:
    with connection_pool.open_session() as session:
        dto = UserCreateDTO(
            email='admin_user@example.com',
            password='password',
            first_name='Admin',
            last_name='User',
            phone=None,
        )
        return create_user_use_case.execute(session, dto)


@pytest.fixture
def admin_user_client(client, admin_user) -> Generator[TestClient, None, None]:
    access, _ = auth_service.generate_token_pair(admin_user.id)
    client.headers['Authorization'] = f'Bearer {access}'
    yield client
