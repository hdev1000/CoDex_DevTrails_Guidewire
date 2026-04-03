from pydantic import BaseModel, Field
from typing import Optional, Dict

class ClaimInput(BaseModel):
    user_id: str
    incident_type: str
    timestamp: int
    location: Dict[str, float]
    images: Optional[list] = None
    device_signal_strength: Optional[float] = None
    network_info: Optional[dict] = None


class ClaimEvaluationResponse(BaseModel):
    claim_id: str
    deterministic_score: float
    llm_score: float
    final_score: float
    decision: str