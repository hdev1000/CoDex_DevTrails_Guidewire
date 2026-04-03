def geo_agent(claim):
    lat, lng = claim.location.get("lat"), claim.location.get("lng")

    confidence = 1.0
    score = 1.0
    explanation = ""

    # Basic sanity checks
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        score -= 0.6
        confidence = 0.9
        explanation = "Invalid coordinates."

    # Time-based plausibility example (placeholder)
    if claim.timestamp < 1000000000:
        score -= 0.2
        explanation += " Timestamp looks invalid."

    return {
        "agent": "geo_agent",
        "score": max(score, 0.0),
        "confidence": confidence,
        "explanation": explanation or "Location verified."
    }