"""Tests for dashboard routes — no external HTTP calls."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch


async def test_dashboard_overview_html(dash_client):
    resp = await dash_client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


async def test_dashboard_api_overview(dash_client):
    resp = await dash_client.get("/api/overview")
    assert resp.status_code == 200
    data = resp.json()
    assert data["article_number"] == "05"
    assert "key_finding" in data


async def test_dashboard_metrics_page(dash_client):
    resp = await dash_client.get("/metrics")
    assert resp.status_code == 200


async def test_dashboard_api_metrics(dash_client):
    resp = await dash_client.get("/api/metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert "policy_propagation_seconds" in data
    assert "agents_in_fleet" in data


async def test_dashboard_eval_page(dash_client):
    resp = await dash_client.get("/eval")
    assert resp.status_code == 200


async def test_dashboard_eval_fixtures(dash_client):
    resp = await dash_client.get("/api/eval/fixtures")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 4
    assert len(data["fixtures"]) == 4


async def test_dashboard_demo_page(dash_client):
    resp = await dash_client.get("/demo")
    assert resp.status_code == 200


async def test_dashboard_demo_proxies_fleet_status(dash_client):
    from unittest.mock import MagicMock

    mock_resp = MagicMock()
    mock_resp.json.return_value = {"total_agents": 7, "agents": []}
    mock_resp.status_code = 200

    with patch("dashboard.routes.demo.httpx.AsyncClient") as MockClient:
        mock_ctx = AsyncMock()
        mock_ctx.__aenter__.return_value.get = AsyncMock(return_value=mock_resp)
        MockClient.return_value = mock_ctx
        resp = await dash_client.get("/api/demo/fleet-status")

    assert resp.status_code == 200


async def test_dashboard_metrics_charts(dash_client):
    resp = await dash_client.get("/api/metrics/propagation-chart")
    assert resp.status_code == 200
    assert "svg" in resp.json()
