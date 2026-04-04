from fastapi import APIRouter
from backend.models.claim import ClaimInput
from backend.services.claim_service import ClaimService
from backend.utils.response import success_response, error_response

router = APIRouter(prefix="/claims", tags=["Claims"])
cs = ClaimService()

@router.post("/submit")
async def submit_claim(payload: dict):
    try:
        claim = ClaimInput.parse_obj(payload)
        result = await cs.create_claim(claim)
        return success_response(result)
    except Exception as e:
        return error_response("CLAIM_SUBMIT_FAILED", str(e))

@router.post("/verify")
async def verify_claim(payload: dict):
    try:
        claim = ClaimInput.parse_obj(payload)
        result = await cs.create_claim(claim)
        return success_response(result)
    except Exception as e:
        return error_response("CLAIM_VERIFY_FAILED", str(e))

@router.get("/list")
def list_claims(user_id: str):
    try:
        return success_response(cs.list_claims(user_id))
    except Exception as e:
        return error_response("CLAIM_LIST_FAILED", str(e))

@router.get("/{claim_id}")
def get_claim(claim_id: str):
    try:
        data = cs.get_claim(claim_id)
        if not data:
            return error_response("CLAIM_NOT_FOUND", "Claim not found")
        return success_response(data)
    except Exception as e:
        return error_response("CLAIM_GET_FAILED", str(e))

@router.get("/status/{claim_id}")
def claim_status(claim_id: str):
    try:
        return success_response({"status": cs.get_status(claim_id)})
    except Exception as e:
        return error_response("CLAIM_STATUS_FAILED", str(e))
