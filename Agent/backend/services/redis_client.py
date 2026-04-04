import redis
from backend.config import settings

if settings.REDIS_URL:
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
else:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
    )


def cache_claim(claim_id: str, payload: dict, ttl: int = 3600):
    redis_client.setex(f"claim:{claim_id}", ttl, str(payload))


def get_cached_claim(claim_id: str):
    return redis_client.get(f"claim:{claim_id}")


def clear_cached_claim(claim_id: str):
    redis_client.delete(f"claim:{claim_id}")
