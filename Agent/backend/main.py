# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router as api_router
from backend.config import settings

app = FastAPI(
    title="Codex Parametric Insurance API",
    description="Backend API powering multi-agent claims processing, fraud detection, and sensor verification.",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register unified router
app.include_router(api_router)

# Health root
@app.get("/")
async def root():
    return {"status": "backend running", "env": settings.ENV}