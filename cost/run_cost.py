from __future__ import annotations

from cost.assumptions import Assumptions
from cost.model import AgentCostEvent


def run_cost_event(
    *,
    run_id: str,
    agent_id: str,
    workflow: str,
    tokens: int,
    successful: bool,
    escalated: bool,
    violated: bool,
    assumptions: Assumptions,
) -> AgentCostEvent:
    return AgentCostEvent(
        run_id=run_id,
        agent_id=agent_id,
        workflow=workflow,
        cost_center=assumptions.cost_center,
        successful=successful,
        model=tokens / 1000.0 * assumptions.token_price_per_1k,
        runtime=assumptions.platform.runtime_per_run,
        observability=assumptions.platform.observability_per_run,
        human_review=assumptions.approval_cost if escalated else 0.0,
        control=assumptions.platform.control_per_run,
        remediation=assumptions.remediation_per_violation if violated else 0.0,
    )
