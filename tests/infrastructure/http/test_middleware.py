import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from faker import Faker

from app.infrastructure.http.middleware import log_request_response_middleware

fake = Faker()


@pytest.fixture
def test_app() -> TestClient:
    app = FastAPI()

    @app.middleware('http')
    async def middleware(request: Request, call_next):
        return await log_request_response_middleware(request, call_next)

    @app.post('/login')
    async def login(request: Request):
        try:
            data = await request.json()
        except Exception:
            return JSONResponse({'error': 'invalid json'}, status_code=400)
        return JSONResponse({'user': data.get('username'), 'status': 'ok'})

    return TestClient(app)


class TestLogRequestResponseMiddleware:
    def test_masked_password_in_log(self, test_app, capsys):
        # Arrange
        username = fake.user_name()
        password = fake.password()
        payload = {'username': username, 'password': password}

        # Act
        response = test_app.post('/login', json=payload)

        # Assert
        assert response.status_code == 200
        assert response.json() == {'user': username, 'status': 'ok'}

        output = capsys.readouterr().out
        assert '"password": "***"' in output
        assert f'"username": "{username}"' in output
        assert 'POST http://testserver/login' in output

    def test_non_json_body_prints_raw(self, test_app, capsys):
        # Arrange
        non_json_body = fake.sentence(nb_words=5)

        # Act
        response = test_app.post(
            '/login',
            content=non_json_body,
            headers={'Content-Type': 'application/json'},
        )

        # Assert
        assert response.status_code == 400
        assert response.json() == {'error': 'invalid json'}

        output = capsys.readouterr().out
        assert non_json_body in output
        assert 'POST http://testserver/login' in output

    def test_empty_body(self, test_app, capsys):
        # Act
        response = test_app.post('/login', content=b'')

        # Assert
        assert response.status_code == 400
        assert response.json() == {'error': 'invalid json'}

        output = capsys.readouterr().out
        assert output == ''

    def test_request_body_raises_exception(self, caplog):
        # Arrange
        app = FastAPI()

        async def broken_body_middleware(request: Request, call_next):
            class BrokenRequest(Request):
                async def body(self):
                    raise ValueError('body failed')

            return await log_request_response_middleware(BrokenRequest(request.scope), call_next)

        app.middleware('http')(broken_body_middleware)

        @app.get('/')
        async def root():
            return {'msg': 'ok'}

        client = TestClient(app)

        # Act
        with caplog.at_level('ERROR'):
            response = client.get('/')

        # Assert
        assert response.status_code == 200
        assert any('Error reading request body' in r.message for r in caplog.records)
