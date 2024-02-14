import os
from celery import Celery
from .services import start

SQLALCHEMY_DATABASE_URL = 'pyamqp://{}:{}@{}:{}'.format(
    os.getenv('RABBITMQ_USER', 'guest'),
    os.getenv('RABBITMQ_PASSWORD', 'guest'),
    os.getenv('RABBITMQ_CONTAINER_NAME', 'localhost'),
    os.getenv('RABBITMQ_PORT', '5672')
)

celery_app = Celery('tasks', broker=SQLALCHEMY_DATABASE_URL)


@celery_app.task()
async def synchronization() -> None:
    await start()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(15.0, synchronization(), name='synchronization')
