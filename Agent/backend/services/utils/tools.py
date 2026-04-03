class MockSatelliteTool:
    def check_location(self, location: str) -> dict:
        # Controlled truth
        if location.lower() == "zone a":
            return {"verified": True, "details": "Heat signatures detected"}
        return {"verified": False, "details": "No activity detected"}

class MockSocialTool:
    def scan_reports(self, location: str) -> dict:
        # Controlled noise
        if location.lower() == "zone a":
            return {"reports": "Multiple distress posts"}
        return {"reports": "Unverified rumors"}
