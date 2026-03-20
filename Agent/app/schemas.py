from pydantic import BaseModel, conint
from typing import Dict, Any

class AgentOutput(BaseModel):
    agent_name: str
    decision: str
    confidence: conint(ge=0, le=100)
    reasoning: str


class ClaimRequest(BaseModel):
    phone_number: str
    latitude: float
    longitude: float
    reason: str
    device_telemetry: Dict[str, Any]
    imei: str
    mac_address: str
    user_shift_status: str  # ON-DUTY or OFF-DUTY
    user_plan_limit: int

