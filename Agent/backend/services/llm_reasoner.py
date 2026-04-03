async def llm_reasoning_agent(claim):
    """
    LLM Agent returns a reasoning score between 0.0 and 1.0.
    Higher = more likely to be legitimate.
    """
    # Placeholder deterministic: replace with actual LLM call
    # Example scoring logic
    text_features = 1.0

    if claim.network_info and claim.network_info.get("vpn", False):
        text_features -= 0.4

    if claim.images is None or len(claim.images) == 0:
        text_features -= 0.3

    return max(text_features, 0.0)