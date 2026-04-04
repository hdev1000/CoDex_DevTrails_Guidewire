import hashlib
from backend.services.redis_client import redis_client


def analyze_image_hash(image_data: str) -> dict:
    """Analyze image hash for fraud pattern detection."""
    if not image_data:
        return {"risk": 0.5, "message": "No image data provided"}
    
    # Hash the image data
    img_hash = hashlib.md5(image_data.encode()).hexdigest()[:16]
    
    # Check if this hash exists in Redis (known fraud patterns)
    key = f"image_hash:{img_hash}"
    exists = redis_client.get(key)
    
    if exists:
        return {
            "risk": 0.85,
            "message": "Known fraud image pattern detected",
            "hash_match": img_hash,
        }
    
    return {
        "risk": 0.1,
        "message": "Image hash not in fraud database",
        "hash": img_hash,
    }


def image_agent(claim):
    """
    Image Agent evaluates claim images for fraud indicators.
    Returns score (0.0-1.0) and confidence.
    """
    score = 1.0
    confidence = 0.85
    explanation = []
    red_flags = []
    
    # Check if images are provided
    if not claim.images or len(claim.images) == 0:
        score -= 0.5
        explanation.append("No visual evidence provided")
        red_flags.append("Missing images")
    
    elif len(claim.images) < 2:
        score -= 0.2
        explanation.append("Insufficient evidence (minimum 2 images recommended)")
    
    # Analyze each image for fraud patterns
    for i, image in enumerate(claim.images[:3]):  # Limit to first 3 images
        try:
            result = analyze_image_hash(image)
            if result["risk"] > 0.5:
                score -= result["risk"] * 0.3
                red_flags.append(f"Image {i+1} matches known fraud pattern")
        except Exception:
            pass  # Skip if analysis fails
    
    # Check for duplicate images across claims
    if claim.images:
        for image in claim.images:
            img_hash = hashlib.md5(image.encode()).hexdigest()
            key = f"image_used:{img_hash}"
            existing_user = redis_client.get(key)
            
            if existing_user:
                score -= 0.4
                explanation.append(f"Image previously used in claim by {existing_user}")
                red_flags.append(f"Duplicate image from claim by {existing_user}")
            else:
                # Store image hash for 7 days
                redis_client.setex(key, 604800, claim.user_id or "unknown")
    
    return {
        "agent": "image_agent",
        "score": max(0.0, min(1.0, score)),
        "confidence": confidence,
        "explanation": "; ".join(explanation) if explanation else "Image evidence adequate",
        "red_flags": red_flags,
    }
