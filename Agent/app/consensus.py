from typing import List, Optional
from time import time

from h3.api.basic_str import latlng_to_cell

from app.schemas import AgentOutput
from app.memory import EpisodicMemory

CONFIDENCE_DIFF_THRESHOLD = 30
REFUSAL_THRESHOLD = 65


class ConsensusManager:
    def __init__(self):
        self.memory = EpisodicMemory()
        self.claim_events = []  # list of (timestamp, h3_cell)

    # ---------------------------------------------------------
    # Core Entry Point
    # ---------------------------------------------------------
    def evaluate(
        self,
        outputs: List[AgentOutput],
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        summary: Optional[dict] = None
    ) -> dict:
        """
        summary: operational summary built from intake
        Used ONLY for confidence calibration (not agent logic)
        """

        if any(o is None for o in outputs):
            return {
                "status": "REFUSED",
                "message": "Technical validation failure"
            }

        # Market Crash Protocol (Adversarial Defense: Market Crash Protection)
        if latitude is not None and longitude is not None:
            market_hit = self._detect_market_crash(latitude, longitude)
            if market_hit:
                return {
                    "status": "DEBATE",
                    "message": "COORDINATED_FRAUD_RING",
                    "reason": "Market crash protection triggered"
                }

        decisions = [o.decision for o in outputs]

        # 0. Store memory for future analysis (not altering final status)
        # (Episodic memory is preserved but does not enforce non-standard status)
        # NOTE: We intentionally avoid returning REFLECTIVE_REUSE to keep
        # statuses within APPROVED/REFUSED/DEBATE as required.
        # self.memory.recall(decisions)

        confidences = [o.confidence for o in outputs]
        avg_confidence = sum(confidences) / len(confidences)

        # 2. Refusal Gate
        if avg_confidence < REFUSAL_THRESHOLD:
            return {
                "status": "REFUSED",
                "message": "Consensus too low",
                "average_confidence": avg_confidence,
                "agent_outputs": [
                    {"agent": o.agent_name, "confidence": o.confidence} for o in outputs
                ]
            }

        # 3. Debate Trigger
        for i in range(len(outputs)):
            for j in range(i + 1, len(outputs)):
                if abs(outputs[i].confidence - outputs[j].confidence) > CONFIDENCE_DIFF_THRESHOLD:
                    return {
                        "status": "DEBATE",
                        "message": "Confidence divergence detected",
                        "agents": [outputs[i].agent_name, outputs[j].agent_name],
                        "confidences": [outputs[i].confidence, outputs[j].confidence]
                    }

        # 4. Approved
        best = max(outputs, key=lambda o: o.confidence)
        result = {
            "status": "APPROVED",
            "final_decision": best.decision,
            "confidence": best.confidence,
            "average_confidence": avg_confidence
        }

        self.memory.store(decisions, best.decision)

        return result

    # ---------------------------------------------------------
    # Market Crash Detection
    # ---------------------------------------------------------
    def _detect_market_crash(self, latitude: float, longitude: float) -> bool:
        cell = latlng_to_cell(latitude, longitude, 8)
        now = time()
        window_start = now - 60

        # Adversarial Defense: Market Crash Protection
        self.claim_events = [(t, c) for t, c in self.claim_events if t >= window_start]
        self.claim_events.append((now, cell))

        count = sum(1 for t, c in self.claim_events if c == cell)
        return count > 10
