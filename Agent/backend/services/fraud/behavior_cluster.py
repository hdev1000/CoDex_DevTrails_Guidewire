import json
import math
from backend.services.redis_client import redis_client

WINDOW_SIZE = 20  # past 20 claims


def compute_behavior_vector(claim):
    return {
        "tod": claim.timestamp % 86400,
        "lat": claim.location.get("lat", 0.0),
        "lng": claim.location.get("lng", 0.0),
        "device": claim.device_id or "unknown",
        "motion_entropy": claim.motion_entropy or 0.0,
        "network_switch": claim.network_info.net_switch,
    }


def save_behavior(user_id, vector):
    key = f"behaviors:{user_id}"
    redis_client.lpush(key, json.dumps(vector))
    redis_client.ltrim(key, 0, WINDOW_SIZE - 1)


def euclidean_distance(v1, v2):
    return math.sqrt(
        (v1["tod"] - v2["tod"])**2 +
        (v1["lat"] - v2["lat"])**2 +
        (v1["lng"] - v2["lng"])**2 +
        (v1["motion_entropy"] - v2["motion_entropy"])**2 +
        (v1["network_switch"] - v2["network_switch"])**2
    )


def evaluate_behavior_anomaly(user_id, claim):
    vector = compute_behavior_vector(claim)
    key = f"behaviors:{user_id}"
    history = redis_client.lrange(key, 0, WINDOW_SIZE - 1) or []

    if not history:
        save_behavior(user_id, vector)
        return {
            "risk": 0.05,
            "explanation": "No behavioral history; baseline created."
        }

    distances = []
    for item in history:
        prev = json.loads(item)
        distances.append(euclidean_distance(vector, prev))

    mean_dist = sum(distances) / len(distances)
    threshold = 25000

    save_behavior(user_id, vector)

    if mean_dist > threshold:
        return {
            "risk": 0.75,
            "explanation": "Behavior anomaly detected (outlier cluster)."
        }

    return {
        "risk": 0.1,
        "explanation": "Behavior fits expected cluster."
    }
