import os

from celery import Celery

from .services import start

RABBITMQ_DATABASE_URL = 'pyamqp://{}:{}@{}:{}'.format(
    os.getenv('RABBITMQ_USER', 'guest'),
    os.getenv('RABBITMQ_PASSWORD', 'guest'),
    os.getenv('RABBITMQ_CONTAINER_NAME', 'localhost'),
    os.getenv('RABBITMQ_PORT', '5672')
)

celery_app = Celery('tasks', broker=RABBITMQ_DATABASE_URL)


# @celery_app.on_after_configure.connect
# async def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(15.0, await synchronization, name='synchronization')
celery_app.conf.beat_schedule = {
    'synchronization': {
        'task': 'app.background_tasks.tasks.synchronization',
        'schedule': 15.0
    },

}


@celery_app.task(default_retry_delay=15, max_retries=None,)
async def synchronization() -> None:
    await start()
