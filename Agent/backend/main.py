from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.claim_routes import router as claim_router
from routes.fraud_routes import router as fraud_router
from routes.device_routes import router as device_router
from routes.identity_routes import router as identity_router
from routes.system_routes import router as system_router

from services.redis_client import redis_client
from backend.routes.health_routes import router as health_router

app.include_router(health_router)

app = FastAPI(
    title="CoDex Multi-Agent Insurance Backend",
    description="Backend for multi-agent fraud detection, LLM reasoning, identity hardening, and claim evaluation.",
    version="1.0.0"
)


# --------------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # replace with your Flutter Web origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------
# STARTUP EVENT
# --------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    print("[System] Starting backend services...")

    # Test Redis on boot
    try:
        redis_client.ping()
        print("[Redis] Connected successfully")
    except Exception as e:
        print("[Redis] Connection failed:", str(e))


# --------------------------------------------------------
# SHUTDOWN EVENT
# --------------------------------------------------------
@app.on_event("shutdown")
async def shutdown_event():
    print("[System] Backend shutting down...")
    try:
        redis_client.close()
        print("[Redis] Closed connection pool")
    except:
        pass


# --------------------------------------------------------
# REGISTER ROUTES
# --------------------------------------------------------
app.include_router(claim_router)
app.include_router(fraud_router)
app.include_router(device_router)
app.include_router(identity_router)
app.include_router(system_router)


# --------------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------------
@app.get("/")
async def home():
    return {"message": "CoDex Backend Running", "status": "ok"}


# --------------------------------------------------------
# DEVELOPMENT ENTRYPOINT
# --------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)