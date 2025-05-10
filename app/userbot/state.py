# For managing temporary state (multi-step commands) via Redis

from app.shared.redis_client import get_redis_async

async def store_status_message(request_id: str, message_id: int):
    redis = get_redis_async()
    try:
        await redis.set(f"status_msg:{request_id}", message_id)
    finally:
        await redis.close()

async def get_status_message(request_id: str) -> int | None:
    redis = get_redis_async()
    try:
        val = await redis.get(f"status_msg:{request_id}")
        if val is not None:
            try:
                return int(val)
            except Exception:
                return None
        return None
    finally:
        await redis.close()