import uuid
from models.claim import ClaimInput
from services.redis_client import cache_claim
from services.multi_agent_orchestrator import run_multi_agent_evaluation
from services.fraud.signature_engine import evaluate_fraud_signature
from services.fraud.behavior_cluster import evaluate_behavior_anomaly
from services.fraud.heuristics import evaluate_heuristics
from services.consensus_v3 import consensus_v3
from services.security.rate_limit import user_rate_limit, ip_rate_limit, claim_rate_limit
from services.security.device_fingerprint import evaluate_device_fingerprint
from services.security.identity_guard import identity_guard
from services.security.abuse_detector import detect_abuse

from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, CLAIMS_COLLECTION

mongo = MongoClient(MONGO_URI)[DB_NAME][CLAIMS_COLLECTION]

async def evaluate_claim(claim: ClaimInput):
    claim_id = str(uuid.uuid4())
    user_id = claim.user_id

        # -------------------------------
    # Rate limiting
    # -------------------------------
    ok, msg = user_rate_limit(claim.user_id)
    if not ok:
        return {"error": msg, "decision": "throttle"}

    ok, msg = ip_rate_limit(claim.network_info.get("ip"))
    if not ok:
        return {"error": msg, "decision": "throttle"}

    ok, msg = claim_rate_limit(claim.user_id)
    if not ok:
        return {"error": msg, "decision": "slow_down"}


    # -------------------------------
    # Identity Hardening
    # -------------------------------
    device_fp = evaluate_device_fingerprint(claim.user_id, claim.device_info)
    identity_res = identity_guard(claim.user_id, claim)
    abuse = detect_abuse(claim)

    identity_risk = (
        device_fp["risk"] +
        identity_res["risk"] +
        abuse["risk"]
    ) / 3

    # Phase 3 — multi-agent evaluation
    agent_results = await run_multi_agent_evaluation(claim)

    # Phase 4 — fraud engines
    sig = evaluate_fraud_signature(claim)
    behavior = evaluate_behavior_anomaly(user_id, claim)
    heur = evaluate_heuristics(claim)

    # Consensus
    final_score, decision, fraud_score = consensus_v3(
        agent_results,
        sig,
        behavior,
        heur,
        identity_risk
    )

    document = {
        "claim_id": claim_id,
        "user_id": user_id,
        "input": claim.dict(),
        "agents": agent_results,
        "fraud_signature": sig,
        "behavior_cluster": behavior,
        "heuristics": heur,
        "final_score": final_score,
        "fraud_score": fraud_score,
        "decision": decision,
        "identity_checks":{
            "device_fingerprint": device_fp,
            "identity_guard": identity_res,
            "abuse_detector": abuse,
            "identity_risk": identity_risk
            },
    }

    cache_claim(claim_id, document)
    mongo.insert_one(document)

    return document