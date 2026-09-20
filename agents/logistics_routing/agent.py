from harness_core import AgentHarness

from agents.base import build_supply_chain_harness
from agents.logistics_routing.schemas import LogisticsInput, LogisticsOutput

_SYSTEM_PROMPT = """You are a logistics optimizer.
Route the shipment and return ONLY valid JSON with these fields:
  shipment_id: string (copy from input)
  route: string (e.g. "Origin → Hub → Destination")
  carrier: string (carrier name)
  estimated_days: integer
  cost_usd: number
  summary: one-sentence explanation
No markdown, no prose — raw JSON only."""


def build_harness() -> AgentHarness:
    return build_supply_chain_harness(
        agent_name="logistics-routing-agent",
        agent_version="1.0.0",
        input_schema=LogisticsInput,
        output_schema=LogisticsOutput,
        system_prompt=_SYSTEM_PROMPT,
    )
