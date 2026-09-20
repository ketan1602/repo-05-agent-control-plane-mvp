"""Tests for the control plane registry, policy engine, and API."""
from __future__ import annotations

from control_plane.registry import AgentRegistry


def test_registry_register_returns_record():
    reg = AgentRegistry()
    record = reg.register("test-agent", "1.0.0")
    assert record.agent_name == "test-agent"
    assert record.agent_version == "1.0.0"
    assert record.status == "registered"
    assert record.policy_version == "v1"


def test_registry_deregister_removes_agent():
    reg = AgentRegistry()
    record = reg.register("test-agent", "1.0.0")
    reg.deregister(record.agent_id)
    assert reg.get(record.agent_id) is None


def test_registry_confirm_policy():
    reg = AgentRegistry()
    r = reg.register("test-agent", "1.0.0")
    reg.mark_policy_pending("v2")
    ok = reg.confirm_policy(r.agent_id, "v2")
    assert ok is True
    assert reg.get(r.agent_id).status == "policy_confirmed"
    assert reg.fleet_confirmed_count() == 1


def test_registry_fleet_status_dict_structure():
    reg = AgentRegistry()
    reg.register("agent-a", "1.0.0")
    reg.register("agent-b", "1.0.0")
    status = reg.fleet_status_dict()
    assert status["total_agents"] == 2
    assert status["confirmed_agents"] == 0
    assert len(status["agents"]) == 2


def test_policy_engine_load_v1(engine):
    policy = engine.load_policy("v1")
    assert policy["version"] == "v1"
    assert "rules" in policy


def test_policy_engine_load_v2(engine):
    policy = engine.load_policy("v2")
    assert policy["version"] == "v2"
    assert "restricted_origin_countries" in policy["rules"]["trade_compliance"]


def test_policy_engine_available_versions(engine):
    versions = engine.available_versions()
    assert "v1" in versions
    assert "v2" in versions


def test_policy_engine_set_current_version(engine):
    engine.set_current_version("v2")
    assert engine.current_version() == "v2"


async def test_cp_health(cp_client):
    resp = await cp_client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


async def test_cp_register_agent(cp_client):
    resp = await cp_client.post(
        "/agents/register",
        json={"agent_name": "test-agent", "agent_version": "1.0.0"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "agent_id" in data
    assert data["policy_version"] == "v1"


async def test_cp_fleet_status(cp_client):
    await cp_client.post("/demo/register-fleet")
    resp = await cp_client.get("/fleet/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_agents"] == 7
    assert "agents" in data


async def test_cp_current_policy(cp_client):
    resp = await cp_client.get("/policy/current")
    assert resp.status_code == 200
    data = resp.json()
    assert "version" in data
    assert "content" in data
