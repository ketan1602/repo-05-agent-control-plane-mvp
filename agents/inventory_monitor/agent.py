from harness_core import AgentHarness

from agents.base import build_supply_chain_harness
from agents.inventory_monitor.schemas import InventoryInput, InventoryOutput

_SYSTEM_PROMPT = """You are an inventory analyst.
Assess the stock level data and return ONLY valid JSON with these fields:
  sku: string (copy from input)
  alert_type: "none" | "low_stock" | "critical" | "overstock"
  recommended_action: string (what to do)
  urgency: "routine" | "urgent" | "critical"
  summary: one-sentence assessment
No markdown, no prose — raw JSON only."""


def build_harness() -> AgentHarness:
    return build_supply_chain_harness(
        agent_name="inventory-monitor-agent",
        agent_version="1.0.0",
        input_schema=InventoryInput,
        output_schema=InventoryOutput,
        system_prompt=_SYSTEM_PROMPT,
    )
