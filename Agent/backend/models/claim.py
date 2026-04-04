from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class DeviceInfo(BaseModel):
    imei: Optional[str] = None
    emulator: Optional[bool] = False
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None


class NetworkInfo(BaseModel):
    ip: Optional[str] = None
    vpn: Optional[bool] = False
    tor: Optional[bool] = False
    ip_hop: Optional[bool] = False
    net_switch: Optional[int] = 0


class ClaimInput(BaseModel):
    user_id: Optional[str] = None
    phone_number: str
    incident_type: str
    timestamp: int
    location: Dict[str, float]
    images: Optional[List[str]] = []
    device_signal_strength: Optional[float] = None
    network_info: NetworkInfo = NetworkInfo()
    device_info: DeviceInfo = DeviceInfo()
    speed: Optional[float] = None
    repeated_coordinate_flag: Optional[bool] = False
    motion_entropy: Optional[float] = 0.0
    device_id: Optional[str] = None
    sensor_checksum: Optional[str] = None
    spoof_flag: Optional[bool] = False


class ClaimEvaluationResponse(BaseModel):
    claim_id: str
    user_id: str
    deterministic_score: float
    llm_score: float
    final_score: float
    decision: str
    fraud_score: float
    details: Dict[str, Any] = Field(default_factory=dict)
