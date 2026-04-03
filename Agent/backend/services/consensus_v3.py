def consensus_v3(agent_outputs, fraud_sig, behavior_anom, heuristics):
    fraud_score = (fraud_sig["risk"] + behavior_anom["risk"] + heuristics["risk"]) / 3

    # multi-agent score (Phase 3)
    total_weight = 0
    weighted = 0
    for agent in agent_outputs:
        s = agent["score"]
        c = agent["confidence"]
        weighted += s * c
        total_weight += c
    multi_agent_score = weighted / total_weight

    # Combined final score
    final = (multi_agent_score * 0.7) + ((1 - fraud_score) * 0.3)

    if fraud_score > 0.7:
        return final, "reject", fraud_score

    if final < 0.45:
        return final, "reject", fraud_score

    if final < 0.6:
        return final, "manual_review", fraud_score

    return final, "approve", fraud_score