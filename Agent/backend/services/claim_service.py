import uuid
from datetime import datetime
from backend.models.claim import ClaimInput
from backend.services.redis_client import cache_claim, get_cached_claim
from backend.services.multi_agent_orchestrator import run_multi_agent_evaluation
from backend.services.fraud.signature_engine import evaluate_fraud_signature
from backend.services.fraud.behavior_cluster import evaluate_behavior_anomaly
from backend.services.fraud.heuristics import evaluate_heuristics
from backend.services.consensus_v3 import consensus_v3
from backend.services.consensus_engine import consensus_v4
from backend.services.security.rate_limit import user_rate_limit, ip_rate_limit, claim_rate_limit
from backend.services.security.device_fingerprint import evaluate_device_fingerprint
from backend.services.security.identity_guard import identity_guard
from backend.services.security.abuse_detector import detect_abuse
from backend.services.deterministic_rules import run_deterministic_checks
from backend.services.llm_reasoner import llm_reasoning_agent
from backend.config import settings
from pymongo import MongoClient

mongo = MongoClient(settings.MONGO_URI)[settings.MONGO_DB][settings.CLAIMS_COLLECTION]


class ClaimService:
    def __init__(self):
        self.collection = mongo

    async def evaluate_claim(self, claim: ClaimInput) -> dict:
        claim_id = str(uuid.uuid4())
        user_id = claim.user_id or claim.phone_number
        claim.user_id = user_id

        # Check rate limits
        ok, msg = user_rate_limit(user_id)
        if not ok:
            return {"error": msg, "decision": "throttle"}

        ok, msg = ip_rate_limit(claim.network_info.ip or "unknown")
        if not ok:
            return {"error": msg, "decision": "throttle"}

        ok, msg = claim_rate_limit(user_id)
        if not ok:
            return {"error": msg, "decision": "slow_down"}

        # Identity and device checks
        identity_risk = 0.0
        device_fp = evaluate_device_fingerprint(user_id, claim.device_info.dict())
        identity_res = identity_guard(user_id, claim)
        abuse = detect_abuse(claim)

        identity_risk = (
            device_fp["risk"] + identity_res["risk"] + abuse["risk"]
        ) / 3

        # Run multi-agent evaluation
        agent_results = await run_multi_agent_evaluation(claim)

        # Get individual fraud scores
        det_score = run_deterministic_checks(claim)
        llm_score = await llm_reasoning_agent(claim)

        sig = evaluate_fraud_signature(claim)
        behavior = evaluate_behavior_anomaly(user_id, claim)
        heur = evaluate_heuristics(claim)

        # Use consensus_v4 (security-focused) for final decision
        final_score, decision, fraud_score = consensus_v4(
            agent_results,
            sig,
            behavior,
            heur,
            identity_risk,
        )

        # Calculate payout
        payout_amount = 0
        if decision == "approve":
            payout_amount = min(5000, max(500, int(final_score * 7500)))

        # Build complete document
        document = {
            "claim_id": claim_id,
            "user_id": user_id,
            "phone_number": claim.phone_number,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "input": claim.dict(),
            "deterministic_score": det_score,
            "llm_score": llm_score,
            "agents": agent_results,
            "fraud_signature": sig,
            "behavior_cluster": behavior,
            "heuristics": heur,
            "final_score": final_score,
            "fraud_score": fraud_score,
            "decision": decision,
            "payout_amount": payout_amount,
            "identity_checks": {
                "device_fingerprint": device_fp,
                "identity_guard": identity_res,
                "abuse_detector": abuse,
                "identity_risk": identity_risk,
            },
        }

        # Cache and persist
        cache_claim(claim_id, document)
        self.collection.insert_one(document)
        
        return document

    async def create_claim(self, claim: ClaimInput) -> dict:
        return await self.evaluate_claim(claim)

    def list_claims(self, user_id: str) -> list[dict]:
        results = self.collection.find({"user_id": user_id}).sort("created_at", -1)
        return [self._clean_doc(r) for r in results]

    def get_claim(self, claim_id: str) -> dict | None:
        doc = self.collection.find_one({"claim_id": claim_id})
        return self._clean_doc(doc) if doc else None

    def get_status(self, claim_id: str) -> str:
        doc = self.collection.find_one({"claim_id": claim_id})
        return doc.get("decision", "unknown") if doc else "not_found"

    def get_payouts(self, user_id: str) -> list[dict]:
        results = self.collection.find({"user_id": user_id, "decision": "approve"}).sort("created_at", -1)
        return [{"claim_id": r.get("claim_id"), "amount": r.get("payout_amount", 0), "created_at": r.get("created_at")} for r in results]

    def _clean_doc(self, doc: dict) -> dict:
        if not doc:
            return {}
        doc.pop("_id", None)
        return doc
