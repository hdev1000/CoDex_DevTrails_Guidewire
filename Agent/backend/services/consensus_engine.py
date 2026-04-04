def consensus_v4(agent_outputs, fraud_sig, behavior_anom, heuristics, identity_risk):
    """
    Security-focused consensus engine with weighted scoring.
    Returns: (final_score, decision, fraud_score)
    """
    # Calculate fraud score from multiple signals
    fraud_score = (
        fraud_sig["risk"] * 0.4 +
        behavior_anom["risk"] * 0.3 +
        heuristics["risk"] * 0.3
    )

    # Multi-agent score (weighted by confidence)
    total_weight = 0
    weighted = 0
    for agent in agent_outputs:
        s = agent["score"]
        c = agent["confidence"]
        weighted += s * c
        total_weight += c
    multi_agent_score = weighted / max(total_weight, 0.001)

    # Combine with identity risk
    final_score = (
        multi_agent_score * 0.6 +
        (1 - fraud_score) * 0.25 +
        (1 - identity_risk) * 0.15
    )

    # Decision thresholds
    if fraud_score > 0.8:
        return final_score, "reject", fraud_score

    if final_score < 0.4:
        return final_score, "reject", fraud_score

    if final_score < 0.65:
        return final_score, "manual_review", fraud_score

    return final_score, "approve", fraud_score
