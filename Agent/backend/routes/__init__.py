# backend/routes/__init__.py

from fastapi import APIRouter

from .auth_routes import router as auth_router
from .claim_routes import router as claim_router
from .device_routes import router as device_router
from .fraud_routes import router as fraud_router
from .health_routes import router as health_router
from .identity_routes import router as identity_router
from .payout_routes import router as payout_router
from .system_routes import router as system_router

router = APIRouter()

# Register all routers
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(claim_router)
router.include_router(device_router)
router.include_router(fraud_router)
router.include_router(identity_router)
router.include_router(payout_router)
router.include_router(system_router)
