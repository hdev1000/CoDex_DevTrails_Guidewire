from fastapi import APIRouter
from backend.utils.response import success_response, error_response
from backend.services.security.rate_limit import user_rate_limit
from backend.services.security.abuse_detector import detect_abuse
from backend.config import settings

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/health")
def health():
    return success_response({"status": "ok"})

@router.get("/config")
def config():
    return success_response({
        "env": settings.ENV,
        "version": settings.API_VERSION,
        "allowed_origins": settings.ALLOWED_ORIGINS,
    })

@router.post("/abuse/check")
def abuse_check(payload: dict):
    try:
        result = detect_abuse(type("Claim", (), payload))
        return success_response(result)
    except Exception as e:
        return error_response("ABUSE_CHECK_ERROR", str(e))
