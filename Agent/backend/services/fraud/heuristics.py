def evaluate_heuristics(claim):
    risk = 0.0
    reasons = []

    # Impossible movement
    if getattr(claim, "speed", None) and claim.speed > 200:
        risk += 0.6
        reasons.append("Impossible travel speed (>200 km/h).")

    # Duplicate coordinates across accounts
    if getattr(claim, "repeated_coordinate_flag", False):
        risk += 0.5
        reasons.append("Repeated coordinates across multiple accounts.")

    # Sudden network changes
    if getattr(claim.network_info, "ip_hop", False):
        risk += 0.3
        reasons.append("Abrupt IP hop detected.")

    # Emulator detection
    if getattr(claim.device_info, "emulator", False):
        risk += 0.7
        reasons.append("Emulator environment detected.")

    return {
        "risk": min(risk, 1.0),
        "explanation": "; ".join(reasons) or "No heuristic anomalies."
    }