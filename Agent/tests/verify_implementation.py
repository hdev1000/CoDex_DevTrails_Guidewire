import pytest
from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)

VALID_PAYLOAD = {
    "phone_number": "9999999999",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "reason": "Loss of income due to weather-induced delivery delay",
    "imei": "123456789012345",
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "user_shift_status": "ON-DUTY",
    "user_plan_limit": 150,
    "device_telemetry": {
        "rainfall_mm": 15,
        "aqi": 55,
        "traffic_congestion": 0.7,
        "accelerometer_variance": 0.2,
        "gyroscope_noise": 0.08,
        "gps_smoothness": 0.3,
        "is_emulator": False,
        "is_rooted": False
    }
}

FRAUD_PAYLOAD = {
    "phone_number": "9999999999",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "reason": "No rain at all",
    "imei": "000000000000000",
    "mac_address": "00:00:00:00:00:00",
    "user_shift_status": "ON-DUTY",
    "user_plan_limit": 150,
    "device_telemetry": {
        "rainfall_mm": 0,
        "aqi": 30,
        "traffic_congestion": 0.1,
        "accelerometer_variance": 0.001,
        "gyroscope_noise": 0.001,
        "gps_smoothness": 0.99,
        "is_emulator": True,
        "is_rooted": True
    }
}


def test_valid_claim_approved():
    resp = client.post("/api/claims/verify", json=VALID_PAYLOAD)
    assert resp.status_code == 200
    body = resp.json()
    assert body["consensus_status"] in ("APPROVED", "CONSENSUS")
    assert body["is_approved"] is True


def test_fraud_claim_refused():
    resp = client.post("/api/claims/verify", json=FRAUD_PAYLOAD)
    assert resp.status_code == 200
    body = resp.json()
    assert body["consensus_status"] == "REFUSED"
    assert body["is_approved"] is False


def test_market_crash_debate():
    payload = VALID_PAYLOAD.copy()
    for i in range(15):
        payload["phone_number"] = f"99999999{i:02d}"
        resp = client.post("/api/claims/verify", json=payload)
        assert resp.status_code == 200

    final_resp = resp.json()
    assert final_resp["consensus_status"] == "DEBATE"
    assert final_resp["is_approved"] is False
