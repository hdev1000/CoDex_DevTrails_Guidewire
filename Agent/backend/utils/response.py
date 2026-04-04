from datetime import datetime
from typing import Any, Optional


def success_response(data: Any, version: str = "v1") -> dict:
    """
    Standardized success response used across all endpoints.
    """
    return {
        "success": True,
        "data": data,
        "errors": None,
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": version,
        }
    }


def error_response(code: str, message: str, version: str = "v1", details: Optional[dict] = None) -> dict:
    """
    Standardized error response format.
    """
    return {
        "success": False,
        "data": None,
        "errors": {
            "code": code,
            "message": message,
            "details": details or {}
        },
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": version,
        }
    }