import time
import jwt
from backend.config import settings

class JWTManager:
    def create_access_token(self, payload):
        payload["exp"] = int(time.time()) + settings.JWT_ACCESS_EXP
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)
    
    def create_refresh_token(self, payload):
        payload["exp"] = int(time.time()) + settings.JWT_REFRESH_EXP
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)

    def refresh_access_token(self, refresh_token):
        try:
            decoded = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])
            return self.create_access_token({"phone": decoded["phone"]})
        except Exception:
            return None

    def invalidate(self, user_id: str):
        return True  # no blacklist yet
