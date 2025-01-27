from http import HTTPStatus

import jwt
import pytest
from fastapi import HTTPException
from faker import Faker

from app.application.use_case.auth import authenticate_use_case

fake = Faker()


class TestAuthenticateUseCase:
    def test_execute_valid_token_returns_session_with_uid(self, mocker):
        # Arrange
        session = mocker.Mock()
        session.info = {}

        token = fake.sha256()
        fake_user_id = fake.random_int(min=1, max=9999)
        fake_claims = mocker.Mock(sub=str(fake_user_id))
        fake_user = mocker.Mock(id=fake_user_id)

        mocker.patch(
            'app.application.use_case.auth.authenticate_use_case.decode_token',
            return_value=fake_claims,
        )
        mocker.patch('app.domain.repository.user_repository.find_by_id', return_value=fake_user)

        # Act
        result = authenticate_use_case.execute(session, token)

        # Assert
        assert result == session
        assert session.info['uid'] == fake_user_id

    def test_execute_expired_token_raises_401(self, mocker):
        # Arrange
        session = mocker.Mock()
        token = fake.sha256()

        # Act & Assert
        mocker.patch(
            'app.application.use_case.auth.authenticate_use_case.decode_token',
            side_effect=jwt.ExpiredSignatureError,
        )
        with pytest.raises(HTTPException) as exc_info:
            authenticate_use_case.execute(session, token)

        # Assert
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.detail == 'Token has expired'

    @pytest.mark.parametrize('err', [jwt.InvalidTokenError, jwt.DecodeError])
    def test_execute_invalid_token_raises_401(self, mocker, err):
        # Arrange
        session = mocker.Mock()
        token = fake.sha256()

        # Act & Assert
        mocker.patch(
            'app.infrastructure.helper.jwt_helper.decode_token',
            side_effect=err,
        )
        with pytest.raises(HTTPException) as exc_info:
            authenticate_use_case.execute(session, token)

        # Assert
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.detail == 'Invalid token'

    def test_execute_user_not_found_raises_401(self, mocker):
        # Arrange
        session = mocker.Mock()
        session.info = {}

        token = fake.sha256()
        fake_user_id = str(fake.random_int(min=1, max=9999))
        fake_claims = mocker.Mock(sub=fake_user_id)

        mocker.patch(
            'app.application.use_case.auth.authenticate_use_case.decode_token',
            return_value=fake_claims,
        )
        mocker.patch('app.domain.repository.user_repository.find_by_id', return_value=None)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            authenticate_use_case.execute(session, token)

        # Assert
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.detail == 'User not found'
