def aggregate_scores(det_score: float, llm_score: float):
    final = (0.6 * det_score) + (0.4 * llm_score)

    decision = "approve" if final >= 0.6 else "manual_review"

    return final, decision