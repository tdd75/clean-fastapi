from unittest.mock import patch
from faker import Faker
import jwt

from app import connection_pool, setting
from app.presentation.dto.auth_dto import RegisterDTO
from app.application.use_case.auth import register_use_case

fake = Faker()


class TestRegister:
    def test_register_success(self, client):
        # Arrange
        body = {
            'email': fake.email(),
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }

        # Act
        with patch('app.infrastructure.task.mail_task.send_mail_task.delay'):
            response = client.post('/auth/register/', json=body)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert 'access' in data
        assert 'refresh' in data

    def test_register_missing_fields(self, client):
        # Arrange
        body = {
            'email': fake.email(),
            'password': fake.password(),
        }

        # Act
        response = client.post('/auth/register/', json=body)

        # Assert
        assert response.status_code == 422

    def test_register_duplicate_email(self, client):
        # Arrange
        email = fake.email()
        body = {
            'email': email,
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }

        # Act
        with patch('app.infrastructure.task.mail_task.send_mail_task.delay'):
            res1 = client.post('/auth/register/', json=body)
            res2 = client.post('/auth/register/', json=body)

        # Assert
        assert res1.status_code == 200
        assert res2.status_code in (400, 422)
        assert 'email' in res2.text.lower()


class TestLogin:
    def test_login_success(self, client):
        # Arrange
        password = fake.password()
        user_data = RegisterDTO(
            email=fake.email(),
            password=password,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        with connection_pool.open_session() as session:
            with patch('app.infrastructure.task.mail_task.send_mail_task.delay'):
                register_use_case.execute(session, user_data)

        body = {
            'email': user_data.email,
            'password': password,
        }

        # Act
        response = client.post('/auth/login/', json=body)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert 'access' in data
        assert 'refresh' in data

    def test_login_wrong_password(self, client):
        # Arrange
        correct_password = fake.password()
        wrong_password = fake.password()
        user_data = RegisterDTO(
            email=fake.email(),
            password=correct_password,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        with connection_pool.open_session() as session:
            with patch('app.infrastructure.task.mail_task.send_mail_task.delay'):
                register_use_case.execute(session, user_data)

        body = {
            'email': user_data.email,
            'password': wrong_password,
        }

        # Act
        response = client.post('/auth/login/', json=body)

        # Assert
        assert response.status_code == 401
        assert response.json()['detail'].lower() == 'invalid credentials'

    def test_login_nonexistent_email(self, client):
        # Arrange
        body = {
            'email': fake.email(),
            'password': fake.password(),
        }

        # Act
        response = client.post('/auth/login/', json=body)

        # Assert
        assert response.status_code == 401
        assert response.json()['detail'].lower() == 'invalid credentials'

    def test_login_missing_fields(self, client):
        # Arrange
        body = {'email': fake.email()}

        # Act
        response = client.post('/auth/login/', json=body)

        # Assert
        assert response.status_code == 422

    def test_token_jwt_structure(self, client):
        # Arrange
        body = {
            'email': fake.email(),
            'password': fake.password(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        }

        # Act
        with patch('app.infrastructure.task.mail_task.send_mail_task.delay'):
            response = client.post('/auth/register/', json=body)

        # Assert
        assert response.status_code == 200
        tokens = response.json()

        decoded = jwt.decode(tokens['access'], setting.JWT_SECRET, algorithms=['HS256'])

        assert 'sub' in decoded
        assert 'iat' in decoded
        assert 'exp' in decoded
