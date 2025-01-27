from datetime import timedelta

from celery import current_app, Celery

from app.infrastructure.config.setting import Setting


def config_celery(setting: Setting) -> Celery:
    current_app.conf.broker_url = setting.CELERY_BROKER_URL
    current_app.conf.result_backend = setting.CELERY_RESULT_BACKEND

    current_app.autodiscover_tasks(
        [
            'app.infrastructure.task.health_check',
            'app.infrastructure.task.mail_task',
        ],
    )

    current_app.conf.beat_schedule = {
        'health-check': {
            'task': 'app.infrastructure.task.health_check.ping',
            'schedule': timedelta(hours=1),
            'args': (),
        },
    }

    return current_app
