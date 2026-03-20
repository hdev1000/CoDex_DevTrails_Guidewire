from pydantic import BaseModel
from typing import List

class RescueStrategy(BaseModel):
    primary_objective: str
    operational_priorities: List[str]
    resource_constraints: List[str]
    forbidden_actions: List[str]

class MCPToolResponse(BaseModel):
    status: str
    rescue_strategy: RescueStrategy | None
    error: str | None = None
