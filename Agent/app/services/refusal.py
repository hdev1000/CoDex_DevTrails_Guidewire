def validate_operational_summary(summary: dict) -> str | None:
    if not summary.get("location"):
        return "Missing location"

    if summary.get("people_involved", 0) <= 0:
        return "Invalid people count"

    time_to_failure = summary.get("time_to_failure")
    if time_to_failure is not None and time_to_failure <= 0:
        return "No remaining management time"

    return None
