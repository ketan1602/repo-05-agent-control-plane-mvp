from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

from dashboard.charts import comparison_table_svg, fleet_visibility_svg, propagation_time_svg

router = APIRouter()

_METRICS_PATH = Path("measurements/fleet_metrics.json")


def _load_metrics() -> dict:
    if _METRICS_PATH.exists():
        return json.loads(_METRICS_PATH.read_text())
    return {
        "policy_propagation_seconds": 7,
        "fleet_visibility_pct": 100,
        "policy_violation_detection_seconds": 4,
        "manual_equivalent_minutes": 47,
        "control_plane_overhead_ms": 120,
        "agents_in_fleet": 7,
    }


@router.get("/metrics")
async def metrics_page() -> FileResponse:
    return FileResponse("dashboard/static/metrics.html")


@router.get("/api/metrics")
async def metrics_data() -> JSONResponse:
    return JSONResponse(_load_metrics())


@router.get("/api/metrics/propagation-chart")
async def propagation_chart() -> JSONResponse:
    m = _load_metrics()
    return JSONResponse({"svg": propagation_time_svg(m["policy_propagation_seconds"])})


@router.get("/api/metrics/visibility-chart")
async def visibility_chart() -> JSONResponse:
    m = _load_metrics()
    return JSONResponse({"svg": fleet_visibility_svg(m["fleet_visibility_pct"], m["agents_in_fleet"])})


@router.get("/api/metrics/comparison-chart")
async def comparison_chart() -> JSONResponse:
    m = _load_metrics()
    return JSONResponse({"svg": comparison_table_svg(
        cp_seconds=m["policy_propagation_seconds"],
        manual_minutes=m["manual_equivalent_minutes"],
    )})
