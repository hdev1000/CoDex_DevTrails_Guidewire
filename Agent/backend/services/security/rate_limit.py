from backend.services.redis_client import redis_client
import time


def rate_limit(key: str, limit: int, window: int):
    now = int(time.time())
    bucket = f"rate:{key}:{now // window}"
    count = redis_client.incr(bucket)
    redis_client.expire(bucket, window)

    if count > limit:
        return False, f"Rate limit exceeded ({limit}/{window}s)."
    return True, None


def user_rate_limit(user_id: str):
    return rate_limit(f"user:{user_id}", limit=10, window=60)


def ip_rate_limit(ip: str):
    return rate_limit(f"ip:{ip}", limit=20, window=60)


def claim_rate_limit(user_id: str):
    return rate_limit(f"claim:{user_id}", limit=1, window=30)
