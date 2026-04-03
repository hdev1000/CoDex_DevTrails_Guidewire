def consensus_v4(agent_outputs, sig, behavior, heuristics, identity_risk):
    fraud_score = (sig["risk"] + behavior["risk"] + heuristics["risk"] + identity_risk) / 4

    # Compute agent score
    total_weight, weighted = 0, 0
    for agent in agent_outputs:
        s = agent["score"]
        c = agent["confidence"]
        weighted += s * c
        total_weight += c
    multi_agent_score = weighted / total_weight

    final = (multi_agent_score * 0.65) + ((1 - fraud_score) * 0.35)

    if fraud_score > 0.7:
        return final, "reject", fraud_score

    if final < 0.45:
        return final, "reject", fraud_score

    if final < 0.6:
        return final, "manual_review", fraud_score

    return final, "approve", fraud_score