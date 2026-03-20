from schemas.intake import EmergencyIntake

def build_operational_summary(intake: EmergencyIntake) -> dict:
    return {
        "location": intake.location,
        "incident_type": intake.incident_cause,
        "people_involved": intake.people_count,
        "injuries_reported": intake.injured,
        "time_since": intake.time_since,
        "time_to_failure": intake.manageable_minutes,
        "first_aid_available": intake.first_aid_available,
        "immediate_danger": (
            intake.injured is True or intake.people_count > 0
        )
    }
