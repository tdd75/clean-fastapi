from typing import Any

import pytest
from app.domain.entity.user import User
from app.infrastructure.cmd.seed import create_user_if_not_exist, init_data


@pytest.fixture
def mock_session(mocker) -> Any:
    return mocker.Mock()


@pytest.fixture
def user_data() -> User:
    return User(email='test@example.com', password='plain_password', first_name='Test', last_name='User')


class TestCreateUserIfNotExist:
    def test_create_user_if_not_exist_user_does_not_exist(self, mocker, mock_session, user_data):
        # Arrange
        mock_find = mocker.patch('app.domain.repository.user_repository.find_by_email', return_value=None)
        mock_create = mocker.patch('app.domain.repository.user_repository.create')
        mock_hash = mocker.patch('app.infrastructure.cmd.seed.hash_password', return_value='hashed_pw')

        # Act
        create_user_if_not_exist(mock_session, user_data)

        # Assert
        mock_find.assert_called_once_with(mock_session, user_data.email)
        mock_hash.assert_called_once_with('plain_password')
        mock_create.assert_called_once_with(mock_session, user_data)
        assert user_data.password == 'hashed_pw'

    def test_create_user_if_not_exist_user_exists(self, mocker, mock_session, user_data):
        # Arrange
        mock_find = mocker.patch('app.domain.repository.user_repository.find_by_email', return_value=user_data)
        mock_create = mocker.patch('app.domain.repository.user_repository.create')
        mock_hash = mocker.patch('app.infrastructure.cmd.seed.hash_password', return_value='hashed_pw')

        # Act
        create_user_if_not_exist(mock_session, user_data)

        # Assert
        mock_find.assert_called_once_with(mock_session, user_data.email)
        mock_hash.assert_not_called()
        mock_create.assert_not_called()


class TestInitData:
    def test_init_data_create_users(self, mocker, mock_session):
        # Arrange
        mock_open_session = mocker.patch('app.infrastructure.cmd.seed.connection_pool.open_session')
        mock_open_session.return_value.__enter__.return_value = mock_session
        mock_create_user = mocker.patch('app.infrastructure.cmd.seed.create_user_if_not_exist')

        # Act
        init_data()

        # Assert
        assert mock_create_user.call_count == 2
        args_list = mock_create_user.call_args_list
        assert args_list[0][0][0] == mock_session  # session
        assert args_list[0][0][1].email == 'user@example.com'
        assert args_list[1][0][1].email == 'admin@example.com'
