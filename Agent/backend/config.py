import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # -----------------------
    # CORE APPLICATION CONFIG
    # -----------------------
    APP_NAME: str = "CoDex Multi-Agent Backend"
    API_VERSION: str = "1.0.0"

    ENV: str = os.getenv("ENV", "development")  # development / production

    # -----------------------
    # SECURITY
    # -----------------------
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret")
    JWT_ALGO: str = "HS256"
    OTP_EXPIRY_SEC: int = 180

    # -----------------------
    # DATABASE
    # -----------------------
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/codex")
    MONGO_DB: str = "codex"

    # -----------------------
    # REDIS CONFIG
    # -----------------------
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD: str | None = os.getenv("REDIS_PASSWORD", None)

    RATE_LIMIT_MAX_REQ: int = 10
    RATE_LIMIT_WINDOW_SEC: int = 60

    # -----------------------
    # H3 GEO SETTINGS
    # -----------------------
    H3_RESOLUTION: int = 9  # production recommended

    # -----------------------
    # LLM / AGENT FRAMEWORK CONFIG
    # -----------------------
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

    # Enable / Disable multi-agent layers
    ENABLE_PHASE_2: bool = True
    ENABLE_PHASE_3: bool = True
    ENABLE_PHASE_4: bool = True
    ENABLE_PHASE_5: bool = True


settings = Settings()