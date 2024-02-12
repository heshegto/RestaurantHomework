import os

from redis import Redis


def get_redis() -> Redis | None:
    return Redis.from_url('redis://{name}:{port}'.format(
        name=os.getenv('REDIS_NAME', 'localhost'),
        port=os.getenv('REDIS_PORT', '6379')
    ), decode_responses=False)


