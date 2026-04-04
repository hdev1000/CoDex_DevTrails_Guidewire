from fastapi import APIRouter
from backend.services.security.identity_guard import OTPManager
from backend.services.security.jwt_manager import JWTManager
from backend.utils.response import success_response, error_response

router = APIRouter(prefix="/identity", tags=["Identity"])
otp_engine = OTPManager()
jwt_engine = JWTManager()

@router.post("/register-device")
def register_device(payload: dict):
    return success_response({"registered": True, "payload": payload})

@router.post("/verify-otp")
def verify_otp(payload: dict):
    phone = payload.get("phone") or payload.get("phone_number")
    otp = payload.get("otp")
    if not phone or not otp:
        return error_response("INVALID_PAYLOAD", "Phone and OTP are required")

    if not otp_engine.verify_otp(phone, otp):
        return error_response("OTP_INVALID", "Invalid OTP")

    access = jwt_engine.create_access_token({"phone": phone})
    refresh = jwt_engine.create_refresh_token({"phone": phone})
    return success_response({"access_token": access, "refresh_token": refresh})
