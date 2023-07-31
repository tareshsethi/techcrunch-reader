from celery import Celery
from celery.schedules import crontab

from app import app
from app.env import REDIS_URL


class CeleryConfig:
    imports = 'app.tasks'
    result_expires = 30
    timezone = 'UTC'

    accept_content = ['json', 'msgpack', 'yaml']
    task_serializer = 'json'
    result_serializer = 'json'

    beat_schedule = {
        "time_scheduler": {
            "task": "app.tasks.ingest_new_techcrunch_articles",
            "schedule": crontab(hour=4, minute=0),  # 4pm UTC = 9am PST
        }
    }


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=REDIS_URL,
        backend=REDIS_URL,
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.config_from_object(CeleryConfig)
    return celery


celery = make_celery(app)
