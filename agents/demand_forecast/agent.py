from harness_core import AgentHarness

from agents.base import build_supply_chain_harness
from agents.demand_forecast.schemas import DemandInput, DemandOutput

_SYSTEM_PROMPT = """You are a demand planner.
Forecast demand from the data and return ONLY valid JSON with these fields:
  product_id: string (copy from input)
  forecast_30d: integer (units forecast for next 30 days)
  confidence: number 0.0-1.0
  demand_drivers: array of strings (factors driving demand)
  summary: one-sentence explanation
No markdown, no prose — raw JSON only."""


def build_harness() -> AgentHarness:
    return build_supply_chain_harness(
        agent_name="demand-forecast-agent",
        agent_version="1.0.0",
        input_schema=DemandInput,
        output_schema=DemandOutput,
        system_prompt=_SYSTEM_PROMPT,
    )
