from fastapi import APIRouter
from services.security.device_fingerprint import DeviceFingerprint
from services.agents.device_agent import DeviceAgent

router = APIRouter(prefix="/device", tags=["Device"])

fp = DeviceFingerprint()
device_agent = DeviceAgent()

@router.post("/fingerprint")
async def fingerprint(data: dict):
    fingerprint = fp.generate_fingerprint(data)
    return {"fingerprint": fingerprint}

@router.post("/validate")
async def validate_device(data: dict):
    result = device_agent.analyze(data)
    return {"device_validation": result}