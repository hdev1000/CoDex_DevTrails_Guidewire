def semantic_guard_check(claim_reason: str, user_shift_status: str) -> dict:
    """
    Semantic guard ensures user claims are contextually valid for shift status.
    """
    if user_shift_status.upper() != "ON-DUTY":
        return {
            "allowed": False,
            "reason": "User is OFF-DUTY; claim cannot be processed"
        }

    if "off-duty" in claim_reason.lower() or "not working" in claim_reason.lower():
        return {
            "allowed": False,
            "reason": "Claim reason conflicts with OFF-DUTY statements"
        }

    return {"allowed": True, "reason": "Semantic check passed"}


def feasibility_check(payout: int, user_plan_limit: int) -> dict:
    allowed_values = {50, 100, 150}
    if payout not in allowed_values:
        return {
            "feasible": False,
            "reason": "Payout amount must be one of 50, 100, 150"
        }

    if payout > user_plan_limit:
        return {
            "feasible": False,
            "reason": "Payout exceeds user plan limit"
        }

    return {"feasible": True, "reason": "Feasibility check passed"}

