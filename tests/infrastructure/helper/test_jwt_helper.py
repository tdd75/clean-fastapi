import datetime

import jwt
import pytest
import time_machine
from faker import Faker

from app import setting
from app.domain.value_object.auth_value_object import Claims
from app.infrastructure.helper.jwt_helper import encode_token, decode_token, generate_token_pair

fake = Faker()


class TestEncodeToken:
    @time_machine.travel('2025-01-01T00:00:00Z')
    def test_encode_token(self):
        # Arrange
        user_id = fake.uuid4()
        delta = datetime.timedelta(minutes=30)

        # Act
        token = encode_token(user_id, delta)
        decoded = jwt.decode(token, setting.JWT_SECRET, algorithms=['HS256'])

        # Assert
        assert decoded['sub'] == user_id
        assert decoded['iat'] == int(datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc).timestamp())
        assert decoded['exp'] == int((datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc) + delta).timestamp())

    def test_token_expired(self):
        # Arrange
        user_id = str(fake.random_int(min=1, max=10000))

        with time_machine.travel('2025-01-01T00:00:00Z'):
            token = encode_token(user_id, datetime.timedelta(seconds=60))

        # Act & Assert
        with time_machine.travel('2025-01-01T00:02:00Z'):
            with pytest.raises(jwt.ExpiredSignatureError):
                jwt.decode(token, setting.JWT_SECRET, algorithms=['HS256'])


class TestDecodeToken:
    @time_machine.travel('2025-01-01T00:00:00Z')
    def test_decode_token(self):
        # Arrange
        user_id = str(fake.random_int(min=1, max=10000))
        issued_at = int(datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc).timestamp())
        expires_at = int(
            (datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(minutes=30)).timestamp()
        )
        claims = {'sub': user_id, 'iat': issued_at, 'exp': expires_at}
        token = jwt.encode(claims, setting.JWT_SECRET, algorithm='HS256')

        # Act
        result = decode_token(token)

        # Assert
        assert isinstance(result, Claims)
        assert result.sub == user_id
        assert result.iat == issued_at
        assert result.exp == expires_at


class TestGenerateTokenPair:
    def test_generate_token_pair(self, monkeypatch):
        # Arrange
        monkeypatch.setattr(
            'app.infrastructure.helper.jwt_helper.encode_token',
            lambda sub, delta: f'token-{sub}-{delta.seconds}',
        )
        setting.JWT_ACCESS_TOKEN_EXPIRES = 300
        setting.JWT_REFRESH_TOKEN_EXPIRES = 600
        user_id = fake.random_int(min=1, max=10000)

        # Act
        access_token, refresh_token = generate_token_pair(user_id)

        # Assert
        assert access_token == f'token-{user_id}-300'
        assert refresh_token == f'token-{user_id}-600'
