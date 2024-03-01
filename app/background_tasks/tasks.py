import os
import asyncio
from celery import Celery

from .services import start

RABBITMQ_DATABASE_URL = 'pyamqp://{}:{}@{}:{}'.format(
    os.getenv('RABBITMQ_USER', 'guest'),
    os.getenv('RABBITMQ_PASSWORD', 'guest'),
    os.getenv('RABBITMQ_CONTAINER_NAME', 'localhost'),
    os.getenv('RABBITMQ_PORT', '5672')
)

celery_app = Celery('tasks', broker=RABBITMQ_DATABASE_URL)

loop = asyncio.get_event_loop()

celery_app.conf.beat_schedule = {
    'synchronization': {
        'task': 'app.background_tasks.tasks.synchronization',
        'schedule': 15.0
    },

}


@celery_app.task(default_retry_delay=15, max_retries=None,)
def synchronization() -> None:
    loop.run_until_complete(start())
