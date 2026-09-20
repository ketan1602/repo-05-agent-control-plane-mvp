from __future__ import annotations

import asyncio
import random
from datetime import UTC, datetime

from harness_core import get_logger

from control_plane.policy_engine import PolicyEngine
from control_plane.registry import AgentRegistry

logger = get_logger(__name__)

_FLEET_AGENT_NAMES: list[str] = [
    "supplier-evaluation-agent",
    "inventory-monitor-agent",
    "demand-forecast-agent",
    "logistics-routing-agent",
    "quality-inspection-agent",
    "trade-compliance-agent",
    "risk-assessment-agent",
]


class ConfigDistributor:
    def __init__(self, registry: AgentRegistry, policy_engine: PolicyEngine) -> None:
        self._registry = registry
        self._policy_engine = policy_engine
        self._propagation_started_at: datetime | None = None
        self._propagation_completed_at: datetime | None = None

    async def distribute_policy(self, version: str) -> dict:
        policy = self._policy_engine.set_current_version(version)
        self._registry.mark_policy_pending(version)
        self._propagation_started_at = datetime.now(UTC)
        self._propagation_completed_at = None
        logger.info("policy_distribution_started", version=version)
        asyncio.create_task(self._confirm_agents_async(version))
        return policy

    async def _confirm_agents_async(self, version: str) -> None:
        agents = self._registry.all_agents()
        for agent in agents:
            delay = random.uniform(0.4, 1.8)  # simulate realistic propagation
            await asyncio.sleep(delay)
            self._registry.confirm_policy(agent.agent_id, version)
            logger.info("agent_policy_confirmed", agent=agent.agent_name, version=version)
        self._propagation_completed_at = datetime.now(UTC)
        elapsed = (self._propagation_completed_at - self._propagation_started_at).total_seconds()
        logger.info("policy_propagation_complete", version=version, elapsed_seconds=elapsed)

    def propagation_elapsed_seconds(self) -> float | None:
        if not self._propagation_started_at:
            return None
        end = self._propagation_completed_at or datetime.now(UTC)
        return round((end - self._propagation_started_at).total_seconds(), 2)

    def seed_fleet(self) -> None:
        for record in list(self._registry.all_agents()):
            self._registry.deregister(record.agent_id)
        for name in _FLEET_AGENT_NAMES:
            self._registry.register(agent_name=name, agent_version="1.0.0")
        logger.info("fleet_seeded", total=len(self._registry.all_agents()))
