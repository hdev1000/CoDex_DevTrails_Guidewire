from __future__ import annotations

from pydantic import BaseModel, conint
from typing import Dict, Any

from .intake import EmergencyIntake, AgentOutput as IntakeAgentOutput


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


AgentOutput = IntakeAgentOutput

__all__ = [
    "EmergencyIntake",
    "AgentOutput",
    "ClaimRequest",
]
