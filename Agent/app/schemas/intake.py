from pydantic import BaseModel
from typing import Optional, Literal, Any, Dict


class EmergencyIntake(BaseModel):
    location: str
    incident_cause: str
    injured: Optional[bool]
    people_count: int
    time_since: Literal["just_now", "<30_min", ">30_min"]
    manageable_minutes: Optional[int]
    first_aid_available: bool


class AgentOutput(BaseModel):
    agent_name: Optional[str] = None
    decision: str
    rationale: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    reasoning: Optional[str] = None

    class Config:
        allow_population_by_field_name = True

