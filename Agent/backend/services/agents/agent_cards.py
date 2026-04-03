AGENT_CARDS = {
    "behavioral_agent": {
        "agent_name": "Behavioral Agent",
        "role": "Human vs Bot Movement Pattern Analyzer",
        "goal": "Detect movement authenticity and GPS spoofing",
        "constraints": [
            "Must return a clear fraud likelihood score",
            "Must prefer human-like noise patterns"
        ]
    },

    "resource_agent": {
        "agent_name": "Resource Agent",
        "role": "Environmental Data Validator",
        "goal": "Validate claim context using weather/aqi/traffic",
        "constraints": [
            "Must use deterministic or mock API data",
            "Cannot pass claims with impossible environmental states"
        ]
    },

    "verifier_agent": {
        "agent_name": "Verifier Agent",
        "role": "Device Integrity and Anti-Fraud Screening",
        "goal": "Detect emulator/rooting and spoofed hardware signatures",
        "constraints": [
            "Must validate IMEI/MAC etc",
            "Must decide VALID vs FRAUD"
        ]
    }
}

