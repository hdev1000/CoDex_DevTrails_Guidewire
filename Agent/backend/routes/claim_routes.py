from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.claim_service import ClaimService

router = APIRouter(prefix="/claims", tags=["Claims"])

class ClaimRequest(BaseModel):
    claim_id: str
    user_id: str
    amount: float
    description: str
    device_info: dict
    location: dict
    images: list

claim_service = ClaimService()

@router.post("/evaluate")
async def evaluate_claim(payload: ClaimRequest):
    try:
        result = await claim_service.process_claim(payload.dict())
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{claim_id}")
async def get_claim_status(claim_id: str):
    status = claim_service.get_claim_status(claim_id)
    if not status:
        raise HTTPException(status_code=404, detail="Claim not found")
    return {"claim_id": claim_id, "status": status}