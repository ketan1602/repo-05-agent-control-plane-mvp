from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class AgentCostEvent:
    run_id: str
    agent_id: str
    workflow: str
    cost_center: str
    successful: bool
    model: float = 0.0
    runtime: float = 0.0
    observability: float = 0.0
    human_review: float = 0.0
    control: float = 0.0
    remediation: float = 0.0

    @property
    def cost(self) -> float:
        return (
            self.model + self.runtime + self.observability
            + self.human_review + self.control + self.remediation
        )


@dataclass(frozen=True)
class OutcomeEconomics:
    runs: int
    successes: int
    total_cost: float

    @property
    def cost_per_run(self) -> float:
        return self.total_cost / self.runs if self.runs else float("inf")

    @property
    def cost_per_success(self) -> float:
        return self.total_cost / self.successes if self.successes else float("inf")


def summarize(events: Iterable[AgentCostEvent]) -> OutcomeEconomics:
    rows = list(events)
    return OutcomeEconomics(
        len(rows),
        sum(e.successful for e in rows),
        sum(e.cost for e in rows),
    )
