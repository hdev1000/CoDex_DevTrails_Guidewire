DANGEROUS_KEYWORDS = ["ignore", "override", "bypass"]

def security_scan(user_input: str) -> dict:
    lowered = user_input.lower()
    for word in DANGEROUS_KEYWORDS:
        if word in lowered:
            return {
                "veto": True,
                "reason": f"Unsafe instruction detected: '{word}'"
            }
    return {"veto": False}
