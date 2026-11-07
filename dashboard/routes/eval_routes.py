from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

router = APIRouter()

_EVAL_FIXTURES = [
    {
        "agent": "supplier-evaluation-agent",
        "description": "High-risk supplier review",
        "expected_outcome": "risk_tier in [high, critical]",
    },
    {
        "agent": "inventory-monitor-agent",
        "description": "Low stock alert detection",
        "expected_outcome": "alert_type != none",
    },
    {
        "agent": "trade-compliance-agent",
        "description": "Restricted country check (v2 policy)",
        "expected_outcome": "compliant == false",
    },
    {
        "agent": "risk-assessment-agent",
        "description": "Critical disruption escalation",
        "expected_outcome": "escalate == true",
    },
]


@router.get("/eval")
async def eval_page() -> FileResponse:
    return FileResponse("dashboard/static/eval.html")


@router.get("/api/eval/fixtures")
async def eval_fixtures() -> JSONResponse:
    return JSONResponse({"fixtures": _EVAL_FIXTURES, "total": len(_EVAL_FIXTURES)})


@router.get("/api/eval/summary")
async def eval_summary() -> JSONResponse:
    return JSONResponse({
        "total_fixtures": len(_EVAL_FIXTURES),
        "agents_covered": 4,
        "fleet_size": 7,
        "note": "Run eval suite with LLM_API_KEY and LLM_BASE_URL set to execute live agent calls.",
    })
