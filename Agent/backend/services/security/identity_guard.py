from backend.services.redis_client import redis_client
import time
import random


def record_imei(user_id: str, imei: str):
    key = f"imei:{user_id}"
    redis_client.lpush(key, imei)
    redis_client.ltrim(key, 0, 9)  # store last 10 IMEIs


def analyze_imei_pattern(user_id: str, imei: str):
    key = f"imei:{user_id}"
    prev_imeis = redis_client.lrange(key, 0, 9) or []

    record_imei(user_id, imei)

    if not prev_imeis:
        return 0.1, "First IMEI observed."

    unique = set(prev_imeis)

    if imei in unique:
        return 0.05, "Known IMEI."

    if len(unique) > 3:
        return 0.8, "IMEI rotation pattern detected."

    return 0.4, "IMEI changed recently."


def record_otp_attempt(phone: str):
    key = f"otp:{phone}"
    ts = int(time.time())
    redis_client.lpush(key, ts)
    redis_client.ltrim(key, 0, 19)


def detect_otp_abuse(phone: str):
    key = f"otp:{phone}"
    attempts = [int(x) for x in redis_client.lrange(key, 0, 19) if x is not None]

    if len(attempts) >= 5 and attempts[0] - attempts[-1] < 300:
        return True, "Multiple OTP attempts in short period."
    return False, None


def identity_guard(user_id: str, claim):
    imei_risk, imei_msg = analyze_imei_pattern(user_id, claim.device_info.imei or "")
    otp_abuse, otp_msg = detect_otp_abuse(claim.phone_number)

    risk = imei_risk + (0.7 if otp_abuse else 0)
    message = "; ".join([x for x in [imei_msg, otp_msg] if x])

    return {
        "risk": min(risk, 1.0),
        "message": message or "Identity appears stable."
    }


class OTPManager:
    def generate_otp(self, phone: str) -> str:
        otp = f"{random.randint(100000, 999999)}"
        key = f"otp:{phone}"
        redis_client.setex(key, 180, otp)
        record_otp_attempt(phone)
        return otp

    def verify_otp(self, phone: str, otp: str) -> bool:
        key = f"otp:{phone}"
        stored = redis_client.get(key)
        if stored and str(stored) == str(otp):
            redis_client.delete(key)
            return True
        return False
