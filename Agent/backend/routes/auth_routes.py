from fastapi import APIRouter
from backend.services.security.identity_guard import OTPManager
from backend.services.security.jwt_manager import JWTManager
from backend.utils.response import success_response, error_response

router = APIRouter(prefix="/auth", tags=["Authentication"])
otp_engine = OTPManager()
jwt_engine = JWTManager()

@router.post("/request_otp")
def request_otp(payload: dict):
    phone = payload.get("phone") or payload.get("phone_number")
    if not phone:
        return error_response("INVALID_PAYLOAD", "phone or phone_number is required")
    otp_engine.generate_otp(phone)
    return success_response({"otp_sent": True})

@router.post("/verify_otp")
def verify_otp(payload: dict):
    phone = payload.get("phone") or payload.get("phone_number")
    otp = payload.get("otp")
    if not phone or not otp:
        return error_response("INVALID_PAYLOAD", "phone and otp are required")
    if not otp_engine.verify_otp(phone, otp):
        return error_response("OTP_INVALID", "Invalid OTP")
    access = jwt_engine.create_access_token({"phone": phone})
    refresh = jwt_engine.create_refresh_token({"phone": phone})
    return success_response({"access_token": access, "refresh_token": refresh})

@router.post("/refresh")
def refresh_token(payload: dict):
    refresh_token = payload.get("refresh_token")
    if not refresh_token:
        return error_response("INVALID_PAYLOAD", "refresh_token is required")
    new_token = jwt_engine.refresh_access_token(refresh_token)
    if not new_token:
        return error_response("TOKEN_INVALID", "Invalid refresh token")
    return success_response({"access_token": new_token})

@router.post("/logout")
def logout(payload: dict):
    user_id = payload.get("user_id")
    if not user_id:
        return error_response("INVALID_PAYLOAD", "user_id is required")
    jwt_engine.invalidate(user_id)
    return success_response({"logged_out": True})
