from typing import Dict

from app.agent_cards import AGENT_CARDS
from app.schemas import AgentOutput


class VerifierAgent:
    """Domain: Device Integrity / Anti-Fraud."""

    def __init__(self):
        self.agent_name = AGENT_CARDS["verifier_agent"]["agent_name"]

    def evaluate(self, imei: str, mac_address: str, device_metadata: Dict[str, str]) -> AgentOutput:
        # Basic heuristics
        fraud_reasons = []
        score = 100

        if not imei or len(imei) < 14 or not imei.isdigit():
            fraud_reasons.append("Invalid IMEI")
            score -= 45

        if mac_address and "00:00:00" in mac_address:
            fraud_reasons.append("Spoofed MAC address")
            score -= 30

        if device_metadata.get("is_emulator"):
            fraud_reasons.append("Emulator usage detected")
            score -= 40

        if device_metadata.get("is_rooted") or device_metadata.get("is_jailbroken"):
            fraud_reasons.append("Rooted/jailbroken device")
            score -= 30

        if score < 0:
            score = 0

        status = "FRAUD" if score < 65 or fraud_reasons else "VALID"
        reasoning = ", ".join(fraud_reasons) or "Device integrity validated"

        return AgentOutput(
            agent_name=self.agent_name,
            decision=status,
            confidence=int(score),
            rationale=reasoning
        )


class ResourceAgent:
    """Domain: Environmental Validation."""

    def __init__(self):
        self.agent_name = AGENT_CARDS["resource_agent"]["agent_name"]

    def evaluate(self, rainfall_mm: float, aqi: int, traffic_congestion: float) -> AgentOutput:
        # Deterministic risk model
        score = 100
        reasons = []

        if rainfall_mm < 1:
            score -= 40
            reasons.append("Minimal rainfall for loss-of-income claim")

        if aqi > 200:
            score -= 20
            reasons.append("Very poor AQI reduces validity")

        if traffic_congestion > 0.8:
            score += 5
            reasons.append("High congestion supports delay claims")

        score = max(0, min(100, score))
        decision = "VALID" if score >= 65 else "INVALID"
        reasoning = ", ".join(reasons) if reasons else "Environmental context validates claim"

        return AgentOutput(
            agent_name=self.agent_name,
            decision=decision,
            confidence=int(score),
            rationale=reasoning
        )


class BehavioralAgent:
    """Domain: Human vs Bot Detection."""

    def __init__(self):
        self.agent_name = AGENT_CARDS["behavioral_agent"]["agent_name"]

    def evaluate(self, telemetry: Dict[str, float]) -> AgentOutput:
        accel_var = telemetry.get("accelerometer_variance", 0)
        gyro_noise = telemetry.get("gyroscope_noise", 0)
        gps_smoothness = telemetry.get("gps_smoothness", 0)

        score = 100
        reasons = []

        if accel_var < 0.01:
            score -= 40
            reasons.append("Low accelerometer variance indicates simulated motion")

        if gyro_noise < 0.02:
            score -= 30
            reasons.append("Low gyroscope noise indicates spoofed behavior")

        if gps_smoothness > 0.9:
            score -= 30
            reasons.append("Perfect linear GPS path indicates likely spoofing")

        if accel_var > 0.1 and gyro_noise > 0.05 and gps_smoothness < 0.7:
            reasons.append("Human movement patterns detected")
            score += 5

        score = max(0, min(100, score))
        decision = "VALID" if score >= 65 else "FRAUD"
        reasoning = ", ".join(reasons) if reasons else "Behavioral telemetry normal"

        return AgentOutput(
            agent_name=self.agent_name,
            decision=decision,
            confidence=int(score),
            rationale=reasoning
        )


def create_agents():
    return VerifierAgent(), ResourceAgent(), BehavioralAgent()

