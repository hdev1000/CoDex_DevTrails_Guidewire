from services.redis_client import redis_client
import time

def record_imei(user_id, imei):
    key = f"imei:{user_id}"
    redis_client.lpush(key, imei)
    redis_client.ltrim(key, 0, 9)  # store last 10 IMEIs

def analyze_imei_pattern(user_id, imei):
    key = f"imei:{user_id}"
    prev_imeis = [i.decode() for i in redis_client.lrange(key, 0, 9)]

    record_imei(user_id, imei)

    if len(prev_imeis) == 0:
        return 0.1, "First IMEI observed."

    unique = set(prev_imeis)

    if imei in unique:
        return 0.05, "Known IMEI."

    if len(unique) > 3:
        return 0.8, "IMEI rotation pattern detected."

    return 0.4, "IMEI changed recently."

def record_otp_attempt(phone):
    key = f"otp:{phone}"
    ts = int(time.time())
    redis_client.lpush(key, ts)
    redis_client.ltrim(key, 0, 19)

def detect_otp_abuse(phone):
    key = f"otp:{phone}"
    attempts = [int(x) for x in redis_client.lrange(key, 0, 19)]

    if len(attempts) >= 5 and attempts[0] - attempts[-1] < 300:
        return True, "Multiple OTP attempts in short period."
    return False, None

def identity_guard(user_id, claim):
    imei_risk, imei_msg = analyze_imei_pattern(user_id, claim.device_info.get("imei"))

    otp_abuse, otp_msg = detect_otp_abuse(claim.phone)

    risk = imei_risk + (0.7 if otp_abuse else 0)
    message = "; ".join([x for x in [imei_msg, otp_msg] if x])

    return {
        "risk": min(risk, 1.0),
        "message": message or "Identity appears stable."
    }