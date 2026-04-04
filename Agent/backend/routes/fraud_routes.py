from fastapi import APIRouter
from backend.utils.response import success_response, error_response
from backend.models.claim import ClaimInput
from backend.services.fraud.heuristics import evaluate_heuristics
from backend.services.fraud.behavior_cluster import evaluate_behavior_anomaly

router = APIRouter(prefix="/fraud", tags=["Fraud"])

@router.post("/risk-check")
def check_fraud(payload: dict):
    try:
        claim = ClaimInput.parse_obj(payload)
        score = evaluate_heuristics(claim)
        return success_response({"fraud_score": score})
    except Exception as e:
        return error_response("FRAUD_CHECK_FAILED", str(e))

@router.post("/cluster")
def cluster_behavior(payload: dict):
    try:
        claim = ClaimInput.parse_obj(payload)
        user_id = payload.get("user_id") or payload.get("phone_number")
        result = evaluate_behavior_anomaly(user_id, claim)
        return success_response(result)
    except Exception as e:
        return error_response("BEHAVIOR_CLUSTER_FAILED", str(e))
