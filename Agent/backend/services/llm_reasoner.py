import os
import httpx
from backend.config import settings


async def llm_reasoning_agent(claim):
    """
    LLM Agent returns a reasoning score between 0.0 and 1.0.
    Higher = more likely to be legitimate.
    """
    try:
        # Build context from claim data
        context = f"""
        Incident Type: {claim.incident_type}
        Location: {claim.location.get('lat')}, {claim.location.get('lng')}
        Timestamp: {claim.timestamp}
        Device: {claim.device_info.model or 'Unknown'} on {claim.device_info.os_version or 'Unknown OS'}
        Network: IP={claim.network_info.ip}, VPN={claim.network_info.vpn}, TOR={claim.network_info.tor}
        Signal Strength: {claim.device_signal_strength} dBm
        Speed: {claim.speed} km/h
        Images Provided: {len(claim.images) if claim.images else 0}
        Device ID: {claim.device_id}
        Spoof Flag: {claim.spoof_flag}
        """
        
        prompt = f"""
        You are an AI fraud detection expert analyzing an insurance claim.
        Evaluate the claim for signs of fraud or legitimacy based on the following information:
        
        {context}
        
        Return a JSON object with:
        - "score": a float between 0.0 and 1.0 (1.0 = fully legitimate, 0.0 = definitely fraudulent)
        - "reasoning": brief explanation of your assessment
        - "red_flags": list of any suspicious elements found
        - "green_flags": list of legitimacy indicators found
        """
        
        # Call LLM API based on provider
        if settings.LLM_PROVIDER == "openai":
            return await _call_openai(prompt)
        else:
            # Fallback to deterministic scoring
            return _deterministic_reasoning(claim)
            
    except Exception as e:
        # Fallback on error
        return _deterministic_reasoning(claim)


async def _call_openai(prompt):
    """Call OpenAI API for LLM reasoning."""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return _deterministic_reasoning(None)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": "You are a fraud detection expert. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 500,
                },
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                
                # Parse JSON from response
                import json
                try:
                    parsed = json.loads(content)
                    score = parsed.get("score", 0.5)
                    return {
                        "agent": "llm_agent",
                        "score": max(0.0, min(1.0, float(score))),
                        "confidence": 0.95,
                        "explanation": parsed.get("reasoning", "LLM analysis completed"),
                        "red_flags": parsed.get("red_flags", []),
                        "green_flags": parsed.get("green_flags", []),
                    }
                except json.JSONDecodeError:
                    return _deterministic_reasoning(None)
            else:
                return _deterministic_reasoning(None)
                
    except Exception:
        return _deterministic_reasoning(None)


def _deterministic_reasoning(claim):
    """Fallback deterministic reasoning when LLM is unavailable."""
    score = 1.0
    reasons = []
    
    if claim:
        # Check for red flags
        if getattr(claim.network_info, "vpn", False):
            score -= 0.3
            reasons.append("VPN detected")
        
        if getattr(claim.network_info, "tor", False):
            score -= 0.5
            reasons.append("TOR detected - high risk")
        
        if getattr(claim.device_info, "emulator", False):
            score -= 0.3
            reasons.append("Emulator detected")
        
        if claim.images is None or len(claim.images) == 0:
            score -= 0.2
            reasons.append("No images provided")
        
        if getattr(claim, "speed", None) and claim.speed > 200:
            score -= 0.4
            reasons.append("Impossible speed detected")
    
    return {
        "agent": "llm_agent",
        "score": max(0.0, min(1.0, score)),
        "confidence": 0.7,
        "explanation": "Deterministic analysis (LLM unavailable)" if not reasons else "; ".join(reasons),
    }
