from datetime import datetime
from typing import Any, Optional


def success(data: Any, message: str = "Success") -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": None,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def failure(message: str, error_code: str = "ERROR", details: Optional[dict] = None) -> dict:
    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": {
            "code": error_code,
            "details": details or {},
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
