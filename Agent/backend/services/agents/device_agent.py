def device_agent(claim):
    score = 1.0
    conf = 1.0
    explanation = ""

    net = claim.network_info or {}

    # VPN detection
    if net.get("vpn", False):
        score -= 0.4
        conf = 0.95
        explanation += "VPN detected. "

    # Signal consistency
    if claim.device_signal_strength is not None:
        if claim.device_signal_strength < -120:
            score -= 0.3
            explanation += "Weak signal anomaly. "

    return {
        "agent": "device_agent",
        "score": max(score, 0.0),
        "confidence": conf,
        "explanation": explanation or "Device integrity normal."
    }