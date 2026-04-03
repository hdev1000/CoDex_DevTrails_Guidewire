def image_agent(claim):
    score = 1.0
    confidence = 0.85
    explanation = ""

    if not claim.images or len(claim.images) == 0:
        score -= 0.5
        explanation = "No visual evidence provided."

    elif len(claim.images) < 2:
        score -= 0.2
        explanation = "Insufficient evidence."

    return {
        "agent": "image_agent",
        "score": max(score, 0.0),
        "confidence": confidence,
        "explanation": explanation or "Image evidence adequate."
    }