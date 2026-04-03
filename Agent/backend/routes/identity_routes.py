from fastapi import APIRouter
from services.security.identity_guard import IdentityGuard
from services.security.rate_limit import RateLimiter
from services.security.abuse_detector import AbuseDetector

router = APIRouter(prefix="/identity", tags=["Identity & Abuse"])

id_guard = IdentityGuard()
rl = RateLimiter()
abuse = AbuseDetector()

@router.post("/verify")
async def verify_identity(data: dict):
    result = id_guard.validate_identity(data)
    return {"identity_status": result}

@router.post("/rate-limit")
async def check_rate_limit(data: dict):
    result = rl.check(data["user_id"])
    return {"allowed": result}

@router.post("/detect-abuse")
async def detect_abuse(data: dict):
    result = abuse.evaluate(data)
    return {"abuse_status": result}