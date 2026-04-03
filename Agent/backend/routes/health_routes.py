from fastapi import APIRouter
from backend.config import settings
from backend.services.redis_client import redis_client
from pymongo import MongoClient
import time

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():
    timestamp = time.time()

    # Redis check
    try:
        redis_client.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "down"

    # Mongo check
    try:
        MongoClient(settings.MONGO_URI).server_info()
        mongo_status = "ok"
    except Exception:
        mongo_status = "down"

    status = (
        "healthy" if redis_status == "ok" and mongo_status == "ok" else "degraded"
    )

    return {
        "status": status,
        "timestamp": timestamp,
        "services": {
            "redis": redis_status,
            "mongo": mongo_status,
        },
        "env": settings.ENV,
        "version": settings.API_VERSION,
    }

@router.get("/liveness")
def liveness():
    return {"status": "alive"}


@router.get("/readiness")
def readiness():
    try:
        redis_client.ping()
        MongoClient(settings.MONGO_URI).server_info()
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}
    
