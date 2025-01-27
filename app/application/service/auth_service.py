import datetime
from dataclasses import asdict

from app.domain.value_object.auth_value_object import Claims
from app.infrastructure.helper.template_helper import render_template
from app.infrastructure.smtp.send_mail import Mail
from app.infrastructure.task.mail_task import send_mail_task
from app import setting

import jwt

JWT_ALGORITHM = 'HS256'


def encode_token(sub: str, expires_delta: datetime.timedelta) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    claims = Claims(sub=sub, iat=int(now.timestamp()), exp=int((now + expires_delta).timestamp()))
    return str(jwt.encode(asdict(claims), setting.JWT_SECRET, algorithm=JWT_ALGORITHM))


def decode_token(token: str) -> Claims:
    data = jwt.decode(token, setting.JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return Claims(**data)


def generate_token_pair(user_id: int) -> tuple[str, str]:
    access_token = encode_token(
        str(user_id), datetime.timedelta(seconds=setting.JWT_ACCESS_TOKEN_EXPIRES)
    )
    refresh_token = encode_token(
        str(user_id), datetime.timedelta(seconds=setting.JWT_REFRESH_TOKEN_EXPIRES)
    )
    return access_token, refresh_token


def send_welcome_mail(receiver: str, name: str) -> None:
    mail_content = render_template(
        'auth/welcome.html',
        {
            'name': name,
            'app_name': 'FastAPI',
        },
    )
    mail = Mail(
        receivers=[receiver],
        subject='Welcome to FastAPI',
        html_content=mail_content,
    )
    send_mail_task.delay([mail])
