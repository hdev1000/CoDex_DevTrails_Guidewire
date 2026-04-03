from GITHUB.Agent.backend.services.agents.geo_agent import geo_agent
from GITHUB.Agent.backend.services.agents.device_agent import device_agent
from GITHUB.Agent.backend.services.agents.image_agent import image_agent
from GITHUB.Agent.backend.services.agents.llm_agent import llm_agent

async def run_multi_agent_evaluation(claim):
    results = []

    results.append(geo_agent(claim))
    results.append(device_agent(claim))
    results.append(image_agent(claim))
    results.append(await llm_agent(claim))

    return results