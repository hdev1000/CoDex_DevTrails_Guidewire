from fastapi import APIRouter
from services.fraud.behavior_cluster import BehaviorClusterEngine
from services.fraud.heuristics import HeuristicEngine
from services.fraud.signature_engine import SignatureEngine

router = APIRouter(prefix="/fraud", tags=["Fraud Analysis"])

bc = BehaviorClusterEngine()
heur = HeuristicEngine()
sig = SignatureEngine()

@router.get("/cluster/{user_id}")
async def fraud_cluster(user_id: str):
    result = bc.get_user_cluster(user_id)
    return {"user_id": user_id, "cluster": result}

@router.post("/heuristics")
async def run_heuristics(data: dict):
    score = heur.evaluate(data)
    return {"heuristic_score": score}

@router.post("/signature")
async def signature_analysis(data: dict):
    flags = sig.match(data)
    return {"flags": flags}