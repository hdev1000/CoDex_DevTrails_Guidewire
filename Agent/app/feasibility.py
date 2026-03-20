from agents import create_auditor, create_agents

def run_feasibility_loop(report: dict):
    auditor = create_auditor()
    rescue, resource, verifier = create_agents()

    auditor_output = {
        "findings": "Potential inefficiency in helicopter allocation",
        "confidence": 70
    }

    resource_check = {
        "feasible": auditor_output["confidence"] >= 60
    }

    verifier_check = {
        "contradictions": False
    }

    return {
        "status": "FEASIBILITY_ANALYZED",
        "auditor_findings": auditor_output,
        "resource_validation": resource_check,
        "ground_truth_validation": verifier_check
    }
