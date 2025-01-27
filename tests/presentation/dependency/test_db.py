from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.presentation.dependency.db import get_authenticated_db


class TestGetAuthenticatedDb:
    def test_get_authenticated_db_valid_token_returns_session_with_uid(self):
        # Arrange
        token = Mock()
        token.credentials = 'valid_token'
        session = Mock()

        # Act
        with patch(
            'app.application.use_case.auth.authenticate_use_case.execute', return_value=session
        ) as mock_exec:
            gen = get_authenticated_db(token, session)
            result = next(gen)

        # Assert
        mock_exec.assert_called_once_with(session, 'valid_token')
        assert result == session

    def test_get_authenticated_db_token_expired_raises_401(self):
        # Arrange
        token = Mock()
        token.credentials = 'expired_token'
        session = Mock()

        # Act & Assert
        with patch('app.application.use_case.auth.authenticate_use_case.execute') as mock_exec:
            mock_exec.side_effect = HTTPException(HTTPStatus.UNAUTHORIZED, 'Token has expired')
            with pytest.raises(HTTPException) as exc_info:
                next(get_authenticated_db(token, session))

        # Assert
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.detail == 'Token has expired'

    def test_get_authenticated_db_invalid_token_raises_401(self):
        # Arrange
        token = Mock()
        token.credentials = 'bad_token'
        session = Mock()

        # Act & Assert
        with patch('app.application.use_case.auth.authenticate_use_case.execute') as mock_exec:
            mock_exec.side_effect = HTTPException(HTTPStatus.UNAUTHORIZED, 'Invalid token')
            with pytest.raises(HTTPException) as exc_info:
                next(get_authenticated_db(token, session))

        # Assert
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.detail == 'Invalid token'

    def test_get_authenticated_db_user_not_found_raises_401(self):
        # Arrange
        token = Mock()
        token.credentials = 'valid_token'
        session = Mock()

        # Act & Assert
        with patch('app.application.use_case.auth.authenticate_use_case.execute') as mock_exec:
            mock_exec.side_effect = HTTPException(HTTPStatus.UNAUTHORIZED, 'User not found')
            with pytest.raises(HTTPException) as exc_info:
                next(get_authenticated_db(token, session))

        # Assert
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.detail == 'User not found'
