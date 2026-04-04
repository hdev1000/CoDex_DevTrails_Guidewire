from fastapi import APIRouter
from backend.utils.response import success_response

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/ping")
async def ping():
    return success_response({"status": "ok"})