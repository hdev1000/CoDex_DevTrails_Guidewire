from services.redis_client import redis_client
import hashlib
import json
import time

SIGNATURE_TTL = 60 * 60 * 24 * 7  # store for 7 days

def hash_signature(data: dict):
    payload = json.dumps(data, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()

def check_signature(data: dict):
    sig = hash_signature(data)
    exists = redis_client.get(f"fraud_sig:{sig}")
    return bool(exists)

def store_signature(data: dict):
    sig = hash_signature(data)
    redis_client.setex(f"fraud_sig:{sig}", SIGNATURE_TTL, int(time.time()))

def evaluate_fraud_signature(claim):
    sig_data = {
        "lat": claim.location.get("lat"),
        "lng": claim.location.get("lng"),
        "ip": claim.network_info.get("ip"),
        "device_id": claim.device_id,
        "sensor_checksum": claim.sensor_checksum
    }

    matched = check_signature(sig_data)
    if matched:
        return {
            "risk": 0.9,
            "explanation": "Known fraud signature detected (repeated spoof pattern)."
        }

    # Store new signature after evaluation
    store_signature(sig_data)

    return {
        "risk": 0.1,
        "explanation": "No known fraud signature."
    }