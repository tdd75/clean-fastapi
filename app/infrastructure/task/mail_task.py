from app.infrastructure.config.celery import celery
from app.infrastructure.smtp.send_mail import Mail, send_mail


@celery.task
def send_mail_task(mail_list: list[Mail]) -> None:
    send_mail(mail_list)
