import hashlib
import json
from backend.services.redis_client import redis_client

DEVICE_FINGERPRINT_TTL = 60 * 60 * 24 * 30  # 30 days


def build_fingerprint(device_info):
    payload = json.dumps(device_info, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def track_device(user_id, fingerprint):
    key = f"fingerprint:{user_id}"
    redis_client.sadd(key, fingerprint)
    redis_client.expire(key, DEVICE_FINGERPRINT_TTL)


def evaluate_device_fingerprint(user_id, device_info):
    fp = build_fingerprint(device_info or {})
    key = f"fingerprint:{user_id}"

    known_devices = redis_client.smembers(key) or set()

    track_device(user_id, fp)

    if fp in known_devices:
        return {
            "risk": 0.05,
            "message": "Device recognized."
        }

    if not known_devices:
        return {
            "risk": 0.1,
            "message": "First-time device registration."
        }

    if len(known_devices) >= 3:
        return {
            "risk": 0.8,
            "message": "Multiple device identities detected."
        }

    return {
        "risk": 0.4,
        "message": "New device fingerprint ??? medium risk."
    }
