import os
from app.mcp_contracts import MCPToolResponse, RescueStrategy

class MCPDocumentServer:
    """
    Mock MCP-compatible document intelligence server.
    In production, this would be replaced by a real MCP service.
    """

    def read_crisis_report(self, file_path: str) -> MCPToolResponse:
        if not os.path.exists(file_path):
            return MCPToolResponse(
                status="ERROR",
                rescue_strategy=None,
                error="File not found"
            )

        # ---- MOCKED DOCUMENT EXTRACTION ----
        # This simulates reading a Crisis SOP PDF
        strategy = RescueStrategy(
            primary_objective="Evacuate civilians from high-risk zones",
            operational_priorities=[
                "Life-saving operations first",
                "Multi-source intelligence validation",
                "Avoid resource exhaustion"
            ],
            resource_constraints=[
                "Limited helicopter fuel",
                "Finite medical personnel",
                "Weather-dependent air operations"
            ],
            forbidden_actions=[
                "Deployment based on single-source intelligence",
                "Ignoring safety verification steps",
                "Unbounded resource allocation"
            ]
        )

        return MCPToolResponse(
            status="OK",
            rescue_strategy=strategy
        )


# -------------------------------------------------------------------
# MCP TOOL EXPORT (THIS IS WHAT FASTAPI IMPORTS)
# -------------------------------------------------------------------

_mcp_server = MCPDocumentServer()

def read_crisis_report(file_path: str) -> MCPToolResponse:
    """
    MCP-compatible tool entrypoint.
    This is the function imported by FastAPI and agents.
    """
    return _mcp_server.read_crisis_report(file_path)
