import random

from control_plane.run_costs import RunCostLedger, simulate_runs


def test_ledger_flags_runs_over_budget():
    ledger = RunCostLedger()
    assert ledger.record("a", 0.4, True, budget_usd=0.5) == "within_budget"
    assert ledger.record("a", 0.6, False, budget_usd=0.5) == "over_budget"
    summary = ledger.summary("a")
    assert summary["runs"] == 2
    assert summary["successes"] == 1
    assert summary["breaches"] == 1
    assert summary["avg_cost_per_run_usd"] == 0.5


def test_ledger_summary_for_unknown_agent_is_empty():
    summary = RunCostLedger().summary("missing")
    assert summary == {"runs": 0, "successes": 0, "breaches": 0,
                       "total_cost_usd": 0.0, "avg_cost_per_run_usd": None}


def test_simulate_runs_counts_every_run():
    ledger = RunCostLedger()
    verdicts = simulate_runs(ledger, ["a", "b"], budget_usd=0.5, runs_per_agent=10,
                             rng=random.Random(7))
    assert verdicts["within_budget"] + verdicts["over_budget"] == 20
    assert ledger.summary("a")["runs"] == 10
    assert ledger.summary("b")["runs"] == 10


async def test_cp_run_cost_reports_verdict(cp_client):
    reg = await cp_client.post("/agents/register",
                               json={"agent_name": "cost-agent", "agent_version": "1.0.0"})
    agent_id = reg.json()["agent_id"]
    cheap = await cp_client.post("/runs/cost", json={
        "agent_id": agent_id, "run_id": "r1", "cost_usd": 0.10, "successful": True})
    assert cheap.json()["verdict"] == "within_budget"
    costly = await cp_client.post("/runs/cost", json={
        "agent_id": agent_id, "run_id": "r2", "cost_usd": 5.00, "successful": False})
    assert costly.json()["verdict"] == "over_budget"
    assert costly.json()["budget_usd"] == 1.0


async def test_cp_run_cost_rejects_unknown_agent(cp_client):
    resp = await cp_client.post("/runs/cost", json={
        "agent_id": "nope", "run_id": "r1", "cost_usd": 0.1, "successful": True})
    assert resp.status_code == 404


async def test_cp_run_cost_rejects_negative_cost(cp_client):
    reg = await cp_client.post("/agents/register",
                               json={"agent_name": "neg-agent", "agent_version": "1.0.0"})
    resp = await cp_client.post("/runs/cost", json={
        "agent_id": reg.json()["agent_id"], "run_id": "r1", "cost_usd": -1, "successful": True})
    assert resp.status_code == 422


async def test_cp_fleet_status_includes_cost_per_agent(cp_client):
    await cp_client.post("/demo/register-fleet")
    resp = await cp_client.get("/fleet/status")
    data = resp.json()
    assert data["run_budget_usd"] == 1.0
    assert all("cost" in agent for agent in data["agents"])


async def test_cp_simulate_runs_records_for_every_agent(cp_client):
    await cp_client.post("/demo/register-fleet")
    resp = await cp_client.post("/demo/simulate-runs", json={"runs_per_agent": 3})
    data = resp.json()
    assert data["agents"] == 7
    assert data["runs"] == 21
    assert data["within_budget"] + data["over_budget"] == 21
