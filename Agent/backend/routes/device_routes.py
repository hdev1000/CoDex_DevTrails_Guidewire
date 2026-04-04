from fastapi import APIRouter
from backend.services.agents.device_agent import DeviceAgent

router = APIRouter(prefix="/device", tags=["Device"])

agent = DeviceAgent()

@router.post("/telemetry")
async def telemetry(payload: dict):
    result = agent.evaluate(payload)
    return {"success": True, "data": {"verdict": result}, "errors": None}
