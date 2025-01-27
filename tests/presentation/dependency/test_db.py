from http import HTTPStatus

import pytest
from fastapi import HTTPException

from app.presentation.dependency.db import get_authenticated_db


class TestGetAuthenticatedDb:
    def test_get_authenticated_db_valid_token_returns_session_with_uid(self, mocker):
        # Arrange
        token = mocker.Mock()
        token.credentials = 'valid_token'
        session = mocker.Mock()

        # Act
        mock_exec = mocker.patch('app.application.use_case.auth.authenticate_use_case.execute', return_value=session)
        gen = get_authenticated_db(token, session)
        result = next(gen)

        # Assert
        mock_exec.assert_called_once_with(session, 'valid_token')
        assert result == session

    def test_get_authenticated_db_token_expired_raises_401(self, mocker):
        # Arrange
        token = mocker.Mock()
        token.credentials = 'expired_token'
        session = mocker.Mock()

        # Act & Assert
        mocker.patch(
            'app.application.use_case.auth.authenticate_use_case.execute',
            side_effect=HTTPException(HTTPStatus.UNAUTHORIZED, 'Token has expired'),
        )
        with pytest.raises(HTTPException) as exc_info:
            next(get_authenticated_db(token, session))

        # Assert
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.detail == 'Token has expired'

    def test_get_authenticated_db_invalid_token_raises_401(self, mocker):
        # Arrange
        token = mocker.Mock()
        token.credentials = 'bad_token'
        session = mocker.Mock()

        # Act & Assert
        mocker.patch(
            'app.application.use_case.auth.authenticate_use_case.execute',
            side_effect=HTTPException(HTTPStatus.UNAUTHORIZED, 'Invalid token'),
        )
        with pytest.raises(HTTPException) as exc_info:
            next(get_authenticated_db(token, session))

        # Assert
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.detail == 'Invalid token'

    def test_get_authenticated_db_user_not_found_raises_401(self, mocker):
        # Arrange
        token = mocker.Mock()
        token.credentials = 'valid_token'
        session = mocker.Mock()

        # Act & Assert
        mocker.patch(
            'app.application.use_case.auth.authenticate_use_case.execute',
            side_effect=HTTPException(HTTPStatus.UNAUTHORIZED, 'User not found'),
        )
        with pytest.raises(HTTPException) as exc_info:
            next(get_authenticated_db(token, session))

        # Assert
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.detail == 'User not found'
