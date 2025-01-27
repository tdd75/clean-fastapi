from celery import shared_task

from app.infrastructure.helper.template_helper import render_template
from app.infrastructure.smtp.send_mail import Mail, send_mail


@shared_task
def send_welcome_mail(receiver: str, name: str) -> None:
    mail_content = render_template(
        'auth/welcome.html',
        {
            'app_name': 'FastAPI',
            'name': name,
        },
    )
    mail = Mail(
        receivers=[receiver],
        subject='Welcome to FastAPI',
        html_content=mail_content,
    )
    send_mail([mail])
