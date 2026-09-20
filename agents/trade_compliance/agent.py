from harness_core import AgentHarness

from agents.base import build_supply_chain_harness
from agents.trade_compliance.schemas import TradeInput, TradeOutput

_SYSTEM_PROMPT = """You are a trade compliance officer.
Check the transaction for compliance and return ONLY valid JSON with these fields:
  transaction_id: string (copy from input)
  compliant: boolean
  flags: array of strings (compliance issues found, empty if compliant)
  required_licenses: array of strings (licenses needed, empty if none)
  risk_level: "low" | "medium" | "high"
  summary: one-sentence compliance assessment
No markdown, no prose — raw JSON only."""


def build_harness() -> AgentHarness:
    return build_supply_chain_harness(
        agent_name="trade-compliance-agent",
        agent_version="1.0.0",
        input_schema=TradeInput,
        output_schema=TradeOutput,
        system_prompt=_SYSTEM_PROMPT,
    )
