import os
import logging
from celery import Celery
from .services import push_new, del_old, check_for_updates

file_path = '../admin/Menu.xlsx'
last_date = 0
SQLALCHEMY_DATABASE_URL = 'amqp://{}:{}@{}:{}'.format(
    os.getenv('RABBITMQ_USER', 'guest'),
    os.getenv('RABBITMQ_PASSWORD', ''),
    os.getenv('RABBITMQ_CONTAINER_NAME', 'localhost'),
    os.getenv('RABBITMQ_PORT', '')
)

app = Celery('tasks', broker=SQLALCHEMY_DATABASE_URL)


@app.task(
    default_retry_delay=15,
    max_retries=None,
)
async def synchronization():
    try:
        push_new()
        del_old()

    except Exception as error:
        logging.error(error)
    finally:
        synchronization.retry()
