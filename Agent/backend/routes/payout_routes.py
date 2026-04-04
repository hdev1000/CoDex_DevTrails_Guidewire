from fastapi import APIRouter
from backend.services.claim_service import ClaimService
from backend.utils.response import success_response

router = APIRouter(prefix="/payouts", tags=["Payouts"])
cs = ClaimService()

@router.get("/history")
def payout_history(user_id: str):
    return success_response(cs.get_payouts(user_id))
