# Redis connection & RQ Queue setup

import redis.asyncio as aioredis
from rq import Queue, Worker, Connection
from config import settings

def get_redis_sync():  # For RQ, which uses sync API
    import redis
    return redis.Redis.from_url(settings.REDIS_URL)

def get_redis_async():  # For async usage (pub/sub, etc)
    return aioredis.from_url(settings.REDIS_URL, decode_responses=True)

def get_rq_queue(name="default"):
    return Queue(name, connection=get_redis_sync())