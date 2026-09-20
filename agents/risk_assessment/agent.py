from harness_core import AgentHarness

from agents.base import build_supply_chain_harness
from agents.risk_assessment.schemas import RiskInput, RiskOutput

_SYSTEM_PROMPT = """You are a supply chain risk manager.
Assess the disruption risk and return ONLY valid JSON with these fields:
  supplier_id: string (copy from input)
  risk_score: number 0-100 (higher = more risk)
  severity: "low" | "medium" | "high" | "critical"
  recommended_actions: array of strings
  escalate: boolean (true if human escalation required)
  summary: one-sentence risk assessment
No markdown, no prose — raw JSON only."""


def build_harness() -> AgentHarness:
    return build_supply_chain_harness(
        agent_name="risk-assessment-agent",
        agent_version="1.0.0",
        input_schema=RiskInput,
        output_schema=RiskOutput,
        system_prompt=_SYSTEM_PROMPT,
    )
