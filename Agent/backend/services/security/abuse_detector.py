def detect_abuse(claim):
    risk = 0
    reasons = []

    # IP hop
    if claim.network_info.get("ip_hop", False):
        risk += 0.4
        reasons.append("Suspicious IP hopping detected.")

    # Distance/speed anomalies
    if claim.speed and claim.speed > 150:
        risk += 0.5
        reasons.append("Travel velocity anomaly >150 km/h.")

    # GPS spoofing risk
    if claim.spoof_flag:
        risk += 0.6
        reasons.append("GPS spoofing signal detected.")

    return {
        "risk": min(risk, 1.0),
        "message": "; ".join(reasons) or "No abuse detected."
    }