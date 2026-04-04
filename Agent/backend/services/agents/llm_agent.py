from backend.services.llm_reasoner import llm_reasoning_agent


async def llm_agent(claim):
    """
    LLM Agent wrapper that calls the reasoning engine.
    Returns structured result with score, confidence, and explanation.
    """
    try:
        result = await llm_reasoning_agent(claim)
        return result
    except Exception as e:
        return {
            "agent": "llm_agent",
            "score": 0.5,
            "confidence": 0.5,
            "explanation": f"LLM analysis failed: {str(e)}",
            "error": str(e),
        }
