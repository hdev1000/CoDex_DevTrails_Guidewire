from backend.services.redis_client import redis_client


def device_agent(claim):
    """
    Device Agent evaluates device integrity for fraud indicators.
    Returns score (0.0-1.0) and confidence.
    """
    score = 1.0
    confidence = 1.0
    explanation = []
    red_flags = []
    
    # Check network info
    if hasattr(claim, "network_info") and claim.network_info:
        if getattr(claim.network_info, "vpn", False):
            score -= 0.4
            explanation.append("VPN detected")
            red_flags.append("VPN usage")
        
        if getattr(claim.network_info, "tor", False):
            score -= 0.6
            explanation.append("TOR detected")
            red_flags.append("TOR usage - high risk")
        
        if getattr(claim.network_info, "ip_hop", False):
            score -= 0.3
            explanation.append("IP hop detected")
            red_flags.append("IP hopping")
    
    # Check device signal strength
    if hasattr(claim, "device_signal_strength") and claim.device_signal_strength is not None:
        if claim.device_signal_strength < -120:
            score -= 0.3
            explanation.append("Weak signal anomaly")
            red_flags.append("Unusually weak signal")
    
    # Check for emulator
    device_info = getattr(claim, "device_info", None) or {}
    if isinstance(device_info, dict):
        if device_info.get("emulator") or (hasattr(claim, "device_info") and getattr(claim.device_info, "emulator", False)):
            score -= 0.3
            explanation.append("Emulator detected")
            red_flags.append("Emulator environment")
    else:
        if getattr(device_info, "emulator", False):
            score -= 0.3
            explanation.append("Emulator detected")
            red_flags.append("Emulator environment")
    
    # Check device fingerprint history
    user_id = claim.user_id or claim.phone_number
    if user_id and hasattr(claim, "device_info"):
        fp_key = f"fingerprint:{user_id}"
        known_devices = redis_client.smembers(fp_key) or set()
        
        if len(known_devices) >= 5:
            score -= 0.3
            explanation.append("Multiple device registrations")
            red_flags.append("Multiple device registrations")
    
    return {
        "agent": "device_agent",
        "score": max(0.0, min(1.0, score)),
        "confidence": confidence,
        "explanation": "; ".join(explanation) if explanation else "Device integrity normal",
        "red_flags": red_flags,
    }


class DeviceAgent:
    def evaluate(self, payload: dict) -> dict:
        if not isinstance(payload, dict):
            return device_agent(payload)
        return device_agent(payload)
