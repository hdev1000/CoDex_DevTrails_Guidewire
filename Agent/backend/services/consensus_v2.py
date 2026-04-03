def consensus_v2(agent_outputs):
    total_weight = 0
    weighted_score = 0

    for agent in agent_outputs:
        score = agent["score"]
        conf = agent["confidence"]

        weighted_score += score * conf
        total_weight += conf

    final_score = weighted_score / total_weight

    if final_score < 0.4:
        decision = "reject"
    elif final_score < 0.6:
        decision = "manual_review"
    else:
        decision = "approve"

    return final_score, decision