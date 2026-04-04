import math
from backend.services.redis_client import redis_client


def h3_distance(lat1, lng1, lat2, lng2):
    """Calculate approximate distance between two coordinates in km."""
    R = 6371  # Earth's radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


def geo_agent(claim):
    """
    Geo Agent validates location data for fraud indicators.
    Returns score (0.0-1.0) and confidence.
    """
    score = 1.0
    confidence = 0.9
    explanation = []
    red_flags = []
    
    lat = claim.location.get("lat")
    lng = claim.location.get("lng")
    
    # Basic coordinate validation
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        score -= 0.6
        explanation.append("Invalid coordinates")
        red_flags.append("Invalid GPS coordinates")
    
    # Timestamp validation
    if claim.timestamp < 1000000000:
        score -= 0.2
        explanation.append("Invalid timestamp")
        red_flags.append("Suspicious timestamp")
    
    # Check for location history anomalies
    user_id = claim.user_id or claim.phone_number
    if user_id:
        key = f"location_history:{user_id}"
        history = redis_client.lrange(key, 0, 9)
        
        if history:
            # Compare with recent locations
            for prev_loc in history:
                try:
                    prev_lat, prev_lng = map(float, prev_loc.split(","))
                    distance = h3_distance(lat, lng, prev_lat, prev_lng)
                    
                    # Check impossible travel
                    if claim.timestamp > 1000000000:
                        time_diff = claim.timestamp - int(prev_loc.split(",")[2]) if "," in prev_loc else 0
                        if time_diff > 0 and time_diff < 3600:  # Less than 1 hour
                            if distance > 500:  # More than 500km in 1 hour
                                score -= 0.5
                                explanation.append("Impossible travel detected")
                                red_flags.append("Impossible travel (>500km in <1hr)")
                except Exception:
                    pass
        
        # Add current location to history
        redis_client.lpush(key, f"{lat},{lng},{claim.timestamp}")
        redis_client.ltrim(key, 0, 9)
    
    # Check for known fraud locations (placeholder - would need real database)
    fraud_zones = []  # In production, load from database
    if lat == 0.0 and lng == 0.0:
        score -= 0.3
        explanation.append("Null island coordinates")
        red_flags.append("Null island coordinates")
    
    return {
        "agent": "geo_agent",
        "score": max(0.0, min(1.0, score)),
        "confidence": confidence,
        "explanation": "; ".join(explanation) if explanation else "Location verified",
        "red_flags": red_flags,
    }
