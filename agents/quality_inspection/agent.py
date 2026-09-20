from harness_core import AgentHarness

from agents.base import build_supply_chain_harness
from agents.quality_inspection.schemas import QualityInput, QualityOutput

_SYSTEM_PROMPT = """You are a quality engineer.
Assess the batch inspection data and return ONLY valid JSON with these fields:
  batch_id: string (copy from input)
  disposition: "accept" | "quarantine" | "reject"
  defect_rate: number 0.0-1.0 (defect_count / sample_size)
  requires_hold: boolean
  recommended_action: string
  summary: one-sentence assessment
No markdown, no prose — raw JSON only."""


def build_harness() -> AgentHarness:
    return build_supply_chain_harness(
        agent_name="quality-inspection-agent",
        agent_version="1.0.0",
        input_schema=QualityInput,
        output_schema=QualityOutput,
        system_prompt=_SYSTEM_PROMPT,
    )
