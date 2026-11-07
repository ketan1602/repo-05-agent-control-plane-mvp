from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class _AgentCosts:
    runs: int = 0
    successes: int = 0
    total_cost_usd: float = 0.0
    breaches: int = 0


class RunCostLedger:
    def __init__(self) -> None:
        self._by_agent: dict[str, _AgentCosts] = {}

    def record(self, agent_id: str, cost_usd: float, successful: bool, budget_usd: float) -> str:
        stats = self._by_agent.setdefault(agent_id, _AgentCosts())
        stats.runs += 1
        stats.successes += int(successful)
        stats.total_cost_usd += cost_usd
        if cost_usd > budget_usd:
            stats.breaches += 1
            return "over_budget"
        return "within_budget"

    def summary(self, agent_id: str) -> dict:
        stats = self._by_agent.get(agent_id, _AgentCosts())
        return {
            "runs": stats.runs,
            "successes": stats.successes,
            "breaches": stats.breaches,
            "total_cost_usd": round(stats.total_cost_usd, 4),
            "avg_cost_per_run_usd": round(stats.total_cost_usd / stats.runs, 4) if stats.runs else None,
        }

    def clear(self) -> None:
        self._by_agent.clear()


def simulate_runs(
    ledger: RunCostLedger,
    agent_ids: list[str],
    budget_usd: float,
    runs_per_agent: int,
    rng: random.Random | None = None,
) -> dict:
    rng = rng or random.Random()
    verdicts = {"within_budget": 0, "over_budget": 0}
    for agent_id in agent_ids:
        for _ in range(runs_per_agent):
            cost_usd = rng.uniform(0.2, 0.9)
            verdict = ledger.record(agent_id, cost_usd, rng.random() < 0.8, budget_usd)
            verdicts[verdict] += 1
    return verdicts
