def run_deterministic_checks(claim):
    score = 1.0

    # Rule 1: Validate coordinate ranges
    if not (-90 <= claim.location["lat"] <= 90 and -180 <= claim.location["lng"] <= 180):
        score -= 0.4

    # Rule 2: Device signal anomaly check
    if claim.device_signal_strength is not None:
        if claim.device_signal_strength < -120:
            score -= 0.3

    # Rule 3: Missing critical fields
    if claim.incident_type == "" or claim.timestamp == 0:
        score -= 0.5

    # Final normalization
    return max(score, 0.0)