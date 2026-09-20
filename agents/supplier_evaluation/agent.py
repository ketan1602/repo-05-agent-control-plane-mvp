from harness_core import AgentHarness

from agents.base import build_supply_chain_harness
from agents.supplier_evaluation.schemas import SupplierInput, SupplierOutput

_SYSTEM_PROMPT = """You are a supply chain risk analyst.
Evaluate the supplier data and return ONLY valid JSON with these fields:
  supplier_id: string (copy from input)
  risk_tier: "low" | "medium" | "high" | "critical"
  recommendation: "approve" | "watch" | "audit" | "terminate"
  score: number 0-100 (higher = safer supplier)
  summary: one-sentence assessment
No markdown, no prose — raw JSON only."""


def build_harness() -> AgentHarness:
    return build_supply_chain_harness(
        agent_name="supplier-evaluation-agent",
        agent_version="1.0.0",
        input_schema=SupplierInput,
        output_schema=SupplierOutput,
        system_prompt=_SYSTEM_PROMPT,
    )
