"""Tests for agent schemas — no LLM calls."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from agents.demand_forecast.schemas import DemandOutput
from agents.inventory_monitor.schemas import InventoryInput
from agents.logistics_routing.schemas import LogisticsInput
from agents.quality_inspection.schemas import QualityOutput
from agents.risk_assessment.schemas import RiskOutput
from agents.supplier_evaluation.schemas import SupplierInput, SupplierOutput
from agents.trade_compliance.schemas import TradeInput


def test_supplier_input_schema():
    s = SupplierInput(
        supplier_id="SUP-001", name="ACME Corp", spend_usd=500000.0,
        categories=["electronics"], risk_flags=["single-source"],
    )
    assert s.supplier_id == "SUP-001"


def test_supplier_output_score_bounds():
    with pytest.raises(ValidationError):
        SupplierOutput(
            supplier_id="S1", risk_tier="high", recommendation="watch",
            score=110.0, summary="Out of bounds",
        )


def test_inventory_input_schema():
    i = InventoryInput(
        sku="SKU-A", warehouse="WH-EU", current_stock=50,
        reorder_point=100, demand_forecast_30d=200,
    )
    assert i.warehouse == "WH-EU"


def test_demand_output_confidence_bounds():
    with pytest.raises(ValidationError):
        DemandOutput(
            product_id="P1", forecast_30d=100, confidence=1.5,
            demand_drivers=[], summary="Invalid",
        )


def test_logistics_input_schema():
    l = LogisticsInput(
        shipment_id="SHP-1", origin="Shanghai", destination="Hamburg",
        weight_kg=500.0, priority="express", deadline_days=14,
    )
    assert l.priority == "express"


def test_quality_output_defect_rate_bounds():
    with pytest.raises(ValidationError):
        QualityOutput(
            batch_id="B1", disposition="accept", defect_rate=1.5,
            requires_hold=False, recommended_action="none", summary="Bad",
        )


def test_trade_input_schema():
    t = TradeInput(
        transaction_id="TXN-1", origin_country="US",
        destination_country="DE", hs_code="8471.30",
        value_usd=50000.0, product_desc="laptop computers",
    )
    assert t.hs_code == "8471.30"


def test_risk_output_score_bounds():
    with pytest.raises(ValidationError):
        RiskOutput(
            supplier_id="S1", risk_score=110.0, severity="high",
            recommended_actions=[], escalate=False, summary="Bad",
        )


def test_all_agents_build_harness_without_api_key(monkeypatch):
    monkeypatch.setenv("AIREFINERY_API_KEY", "test-key")
    from agents.inventory_monitor.agent import build_harness as build_im
    from agents.supplier_evaluation.agent import build_harness as build_se
    harness_se = build_se()
    harness_im = build_im()
    assert harness_se is not None
    assert harness_im is not None
    assert harness_se.run_count == 0
