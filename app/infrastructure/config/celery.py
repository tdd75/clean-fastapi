from app import setting
from celery import Celery


celery = Celery(__name__)

celery.conf.broker_url = setting.CELERY_BROKER_URL
celery.conf.result_backend = setting.CELERY_RESULT_BACKEND

celery.autodiscover_tasks(
    [
        'app.infrastructure.task.send_mail_task',
    ]
)
