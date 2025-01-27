import pytest
from unittest.mock import MagicMock, patch

from app.domain.entity.user import User
from app.infrastructure.cmd.seed import create_user_if_not_exist, init_data


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def user_data():
    return User(
        email='test@example.com', password='plain_password', first_name='Test', last_name='User'
    )


class TestCreateUserIfNotExist:
    @patch('app.domain.repository.user_repository.find_by_email', return_value=None)
    @patch('app.domain.repository.user_repository.create')
    @patch('app.infrastructure.cmd.seed.hash_password', return_value='hashed_pw')
    def test_create_user_if_not_exist_user_does_not_exist(
        self, mock_hash, mock_create, mock_find, mock_session, user_data
    ):
        create_user_if_not_exist(mock_session, user_data)

        mock_find.assert_called_once_with(mock_session, user_data.email)
        mock_hash.assert_called_once_with('plain_password')
        mock_create.assert_called_once_with(mock_session, user_data)
        assert user_data.password == 'hashed_pw'

    @patch('app.domain.repository.user_repository.find_by_email', return_value=user_data)
    @patch('app.domain.repository.user_repository.create')
    @patch('app.infrastructure.cmd.seed.hash_password', return_value='hashed_pw')
    def test_create_user_if_not_exist_user_exists(
        self, mock_hash, mock_create, mock_find, mock_session, user_data
    ):
        create_user_if_not_exist(mock_session, user_data)

        mock_find.assert_called_once_with(mock_session, user_data.email)
        mock_hash.assert_not_called()
        mock_create.assert_not_called()


class TestInitData:
    @patch('app.infrastructure.cmd.seed.connection_pool.open_session')
    @patch('app.infrastructure.cmd.seed.create_user_if_not_exist')
    def test_init_data_create_users(self, mock_create_user, mock_open_session, mock_session):
        mock_open_session.return_value.__enter__.return_value = mock_session

        # run
        init_data()

        # check
        assert mock_create_user.call_count == 2

        args_list = mock_create_user.call_args_list
        assert args_list[0][0][0] == mock_session  # session
        assert args_list[0][0][1].email == 'tranducduy7520@gmail.com'
        assert args_list[1][0][1].email == 'admin@example.com'
