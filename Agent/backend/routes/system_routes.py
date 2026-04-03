from fastapi import APIRouter
from services.consensus_v3 import ConsensusEngineV3
from services.redis_client import redis_client

router = APIRouter(prefix="/system", tags=["System"])

consensus = ConsensusEngineV3()

@router.get("/health")
async def health_check():
    redis_ok = redis_client.ping()
    return {
        "status": "ok",
        "redis": redis_ok,
        "consensus_engine": "v3"
    }

@router.get("/consensus-test/{claim_id}")
async def consensus_test(claim_id: str):
    result = consensus.test_consensus(claim_id)
    return {"claim_id": claim_id, "consensus": result}