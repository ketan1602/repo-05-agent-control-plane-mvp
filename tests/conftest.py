from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from control_plane.config_distributor import ConfigDistributor
from control_plane.policy_engine import PolicyEngine
from control_plane.registry import AgentRegistry
from control_plane.server import app as cp_app
from dashboard.app import app as dash_app


@pytest.fixture
def registry():
    return AgentRegistry()


@pytest.fixture
def engine():
    return PolicyEngine(policies_dir="policies")


@pytest.fixture
def distributor(registry, engine):
    return ConfigDistributor(registry, engine)


@pytest.fixture
async def cp_client():
    async with AsyncClient(transport=ASGITransport(app=cp_app), base_url="http://test") as client:
        yield client


@pytest.fixture
async def dash_client():
    async with AsyncClient(transport=ASGITransport(app=dash_app), base_url="http://test") as client:
        yield client
