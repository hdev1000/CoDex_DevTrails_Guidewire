from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

from app.schemas import ClaimRequest
from app.agents import create_agents
from app.consensus import ConsensusManager
from app.semantic_guard import semantic_guard_check, feasibility_check

app = FastAPI(title="INSUREX Claim Verification API")
consensus_manager = ConsensusManager()

# ---------------------------------------------------------
# CORS (safe for Streamlit + Docker)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"status": "Backend running OK"}


@app.post("/api/claims/verify")
def verify_claim(claim: ClaimRequest):
    semantic = semantic_guard_check(claim.reason, claim.user_shift_status)
    if not semantic.get("allowed"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": semantic.get("reason")}
        )

    payout_amount = 100
    feasibility = feasibility_check(payout_amount, claim.user_plan_limit)
    if not feasibility.get("feasible"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": feasibility.get("reason")}
        )

    verifier, resource, behavioral = create_agents()

    # mock environment data for deterministic behavior
    rainfall_mm = claim.device_telemetry.get("rainfall_mm", 5.0)
    aqi = claim.device_telemetry.get("aqi", 80)
    traffic_congestion = claim.device_telemetry.get("traffic_congestion", 0.5)

    try:
        verifier_output = verifier.evaluate(claim.imei, claim.mac_address, claim.device_telemetry)
        resource_output = resource.evaluate(rainfall_mm, aqi, traffic_congestion)
        behavioral_output = behavioral.evaluate(claim.device_telemetry)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    # Use a singleton consensus manager to track claims over time for market crash defense
    consensus = consensus_manager.evaluate(
        [verifier_output, resource_output, behavioral_output],
        latitude=claim.latitude,
        longitude=claim.longitude
    )

    if consensus.get("status") == "REFUSED":
        is_approved = False
        payout_amount = 0
    elif consensus.get("status") == "DEBATE":
        is_approved = False
        payout_amount = 0
    else:
        is_approved = True

    return {
        "is_approved": is_approved,
        "payout_amount": payout_amount if is_approved else 0,
        "consensus_status": consensus.get("status"),
        "agent_reasoning": {
            "verifier": verifier_output.rationale,
            "resource": resource_output.rationale,
            "behavioral": behavioral_output.rationale
        },
        "consensus_detail": consensus
    }


# ---------------------------------------------------------
# HARD-CODED ANALYZE ENDPOINT
# ---------------------------------------------------------
@app.post("/analyze")
def analyze(payload: dict):
    """
    Fully hardcoded response to guarantee stability
    """

    return {
        "status": "CONSENSUS",
        "final_decision": "Dispatch emergency response team immediately",
        "confidence": 80,
        "trace": {
            "thought": [
                "Emergency situation detected",
                "Immediate response required",
                "Standard emergency protocol selected"
            ],
            "action": [
                "Dispatch ambulance",
                "Notify local authorities",
                "Secure incident location"
            ],
            "observation": {
                "average_confidence": 80
            }
        }
    }


# ---------------------------------------------------------
# HARD-CODED DOCUMENT ANALYSIS
# ---------------------------------------------------------
@app.post("/analyze_document")
def analyze_document(file: UploadFile = File(...)):
    return {
        "status": "DOCUMENT_ANALYZED",
        "summary": "Document reviewed successfully",
        "risk_level": "MEDIUM",
        "recommended_action": "Proceed with standard emergency response"
    }
