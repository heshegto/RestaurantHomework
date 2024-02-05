import pickle

from redis import Redis
from sqlalchemy.orm.query import Query


def get_redis():
    return Redis(host='localhost', port=6379, decode_responses=False)


def delete_cache(keywords: list[str], cache: Redis):
    for keyword in keywords:
        cache.delete(keyword)


def create_cache(keyword: str, db_data: list | Query, cache: Redis):
    cache.set(keyword, pickle.dumps(db_data))


def read_cache(keyword: str, cache: Redis):
    result = cache.get(keyword)
    if result is None:
        return None
    return pickle.loads(result)


def delete_kids_cache(keyword: str, cache: Redis):
    for i in cache.scan_iter(keyword):
        delete_cache(i, cache)
