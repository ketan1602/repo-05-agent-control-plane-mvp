from __future__ import annotations

import os

import httpx
from harness_core import get_logger

from cost import Assumptions, run_cost_event

logger = get_logger(__name__)

_DEFAULT_CP_URL = "http://localhost:8001"


class ControlPlanePlugin:
    """Registers an agent with the control plane and handles policy confirmations."""

    def __init__(self, agent_name: str, agent_version: str, cp_url: str | None = None) -> None:
        self._agent_name = agent_name
        self._agent_version = agent_version
        self._cp_url = (cp_url or os.environ.get("CONTROL_PLANE_URL", _DEFAULT_CP_URL)).rstrip("/")
        self._agent_id: str | None = None

    async def register(self) -> str:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self._cp_url}/agents/register",
                json={"agent_name": self._agent_name, "agent_version": self._agent_version},
            )
            resp.raise_for_status()
            data = resp.json()
            self._agent_id = data["agent_id"]
            logger.info(
                "agent_registered",
                agent=self._agent_name,
                agent_id=self._agent_id,
                policy_version=data.get("policy_version"),
            )
            return self._agent_id

    async def confirm_policy(self, policy_version: str) -> None:
        if not self._agent_id:
            raise RuntimeError("Agent not registered — call register() first")
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self._cp_url}/agents/{self._agent_id}/confirm-policy",
                json={"policy_version": policy_version},
            )
            resp.raise_for_status()
        logger.info("policy_confirmed", agent=self._agent_name, version=policy_version)

    async def report_run_cost(
        self, run_id: str, tokens: int, successful: bool, escalated: bool, violated: bool
    ) -> str:
        if not self._agent_id:
            raise RuntimeError("Agent not registered — call register() first")
        event = run_cost_event(
            run_id=run_id, agent_id=self._agent_id, workflow=self._agent_name, tokens=tokens,
            successful=successful, escalated=escalated, violated=violated,
            assumptions=Assumptions.from_env(),
        )
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self._cp_url}/runs/cost",
                json={"agent_id": self._agent_id, "run_id": run_id,
                      "cost_usd": event.cost, "successful": successful},
            )
            resp.raise_for_status()
        verdict = resp.json()["verdict"]
        logger.info("run_cost_reported", agent=self._agent_name, run_id=run_id,
                    cost_usd=round(event.cost, 6), verdict=verdict)
        return verdict

    async def deregister(self) -> None:
        if not self._agent_id:
            return
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.delete(f"{self._cp_url}/agents/{self._agent_id}")
        logger.info("agent_deregistered", agent=self._agent_name, agent_id=self._agent_id)
        self._agent_id = None

    @property
    def agent_id(self) -> str | None:
        return self._agent_id
