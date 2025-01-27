import pytest
from faker import Faker

from app import connection_pool
from app.domain.repository import user_repository
from app.application.dto.user_dto import UserDTO, CreateUserDTO
from app.application.use_case.user import create_user_use_case
from app.presentation.dependency.context import AppContext

fake = Faker()


@pytest.fixture
def user_1() -> UserDTO:
    # Arrange
    body = CreateUserDTO(
        email=fake.unique.email(),
        password=fake.password(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone=fake.phone_number(),
    )
    with connection_pool.open_session() as session:
        ctx = AppContext(session)
        return create_user_use_case.execute(ctx, body)


class TestSearchUsers:
    def test_search_by_keyword_returns_match(self, normal_user_client, user_1):
        # Arrange
        keyword = user_1.first_name

        # Act
        response = normal_user_client.get('/user/', params={'keyword': keyword})

        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['count'] >= 1
        assert any(u['id'] == user_1.id for u in data['results'])


class TestGetUser:
    def test_get_user_by_id(self, normal_user_client, user_1):
        # Act
        response = normal_user_client.get(f'/user/{user_1.id}/')

        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['id'] == user_1.id
        assert data['email'] == user_1.email
        assert 'password' not in data
        assert data['first_name'] == user_1.first_name
        assert data['last_name'] == user_1.last_name

    def test_get_user_returns_404_for_nonexistent(self, normal_user_client):
        # Arrange
        fake_id = fake.random_int(min=99999, max=999999)

        # Act
        response = normal_user_client.get(f'/user/{fake_id}/')

        # Assert
        assert response.status_code == 404, response.text


class TestCreateUser:
    def test_create_user_successfully(self, normal_user_client, normal_user):
        # Arrange
        body = {
            'email': fake.unique.email(),
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'phone': fake.phone_number(),
        }

        # Act
        response = normal_user_client.post('/user/', json=body)

        # Assert
        assert response.status_code == 201, response.text
        data = response.json()
        assert data['email'] == body['email']
        assert data['first_name'] == body['first_name']
        assert data['last_name'] == body['last_name']
        assert data['phone'] == body['phone']
        assert 'password' not in data
        assert data['full_name'] == f'{body["first_name"]} {body["last_name"]}'
        assert data['created_user']['id'] == normal_user.id
        assert data['updated_user']['id'] == normal_user.id

    def test_create_user_returns_422_for_duplicate_email(self, normal_user_client, normal_user):
        # Arrange
        body = {
            'email': normal_user.email,
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'phone': fake.phone_number(),
        }

        # Act
        response = normal_user_client.post('/user/', json=body)

        # Assert
        assert response.status_code == 422, response.text


class TestUpdateUser:
    def test_update_user_first_name(self, normal_user_client, user_1):
        # Arrange
        new_first_name = fake.first_name()

        # Act
        response = normal_user_client.patch(f'/user/{user_1.id}/', json={'first_name': new_first_name})

        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['first_name'] == new_first_name


class TestDeleteUser:
    def test_delete_user_by_id(self, normal_user_client, user_1):
        # Act
        response = normal_user_client.delete(f'/user/{user_1.id}/')

        # Assert
        assert response.status_code == 204, response.text

        # Verify from DB
        with connection_pool.open_session() as session:
            user = user_repository.find_by_id(session, user_1.id)
            assert user is None, f'Expected user {user_1.id} to be deleted'
