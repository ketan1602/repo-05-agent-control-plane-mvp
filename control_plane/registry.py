from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class AgentRecord:
    agent_id: str
    agent_name: str
    agent_version: str
    registered_at: datetime
    policy_version: str
    status: str  # registered | policy_pending | policy_confirmed


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, AgentRecord] = {}

    def register(self, agent_name: str, agent_version: str) -> AgentRecord:
        agent_id = str(uuid.uuid4())
        record = AgentRecord(
            agent_id=agent_id,
            agent_name=agent_name,
            agent_version=agent_version,
            registered_at=datetime.now(UTC),
            policy_version="v1",
            status="registered",
        )
        self._agents[agent_id] = record
        return record

    def deregister(self, agent_id: str) -> None:
        self._agents.pop(agent_id, None)

    def get(self, agent_id: str) -> AgentRecord | None:
        return self._agents.get(agent_id)

    def all_agents(self) -> list[AgentRecord]:
        return list(self._agents.values())

    def mark_policy_pending(self, policy_version: str) -> None:
        for record in self._agents.values():
            record.status = "policy_pending"
            record.policy_version = policy_version

    def confirm_policy(self, agent_id: str, policy_version: str) -> bool:
        record = self._agents.get(agent_id)
        if not record:
            return False
        record.status = "policy_confirmed"
        record.policy_version = policy_version
        return True

    def fleet_confirmed_count(self) -> int:
        return sum(1 for r in self._agents.values() if r.status == "policy_confirmed")

    def fleet_status_dict(self) -> dict:
        agents = [
            {
                "agent_id": r.agent_id,
                "agent_name": r.agent_name,
                "agent_version": r.agent_version,
                "policy_version": r.policy_version,
                "status": r.status,
                "registered_at": r.registered_at.isoformat(),
            }
            for r in self._agents.values()
        ]
        total = len(agents)
        confirmed = self.fleet_confirmed_count()
        return {
            "total_agents": total,
            "confirmed_agents": confirmed,
            "visibility_pct": round(confirmed / total * 100, 1) if total > 0 else 0.0,
            "agents": agents,
        }
