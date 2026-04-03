async def llm_agent(claim):
    # Placeholder until real LLM integration
    score = 1.0
    confidence = 0.9
    explanation = ""

    if claim.network_info and claim.network_info.get("tor", False):
        score -= 0.6
        explanation = "TOR detected - high risk."

    return {
        "agent": "llm_agent",
        "score": max(score, 0.0),
        "confidence": confidence,
        "explanation": explanation or "Contextual analysis clean."
    }