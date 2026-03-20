import os
from crewai.llm import LLM

def get_llm():
    mode = os.getenv("LLM_MODE", "mock")

    # ---------------- REAL LLM (Gemini) ----------------
    if mode == "real":
        return LLM(
            model="gemini-2.5-flash-lite",
            temperature=0.2,
            api_key=os.getenv("GEMINI_API_KEY")
        )

    # ---------------- MOCK / DETERMINISTIC ----------------
    return LLM(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key="DUMMY_KEY"
    )
