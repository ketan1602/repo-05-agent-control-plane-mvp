from __future__ import annotations

import os

import httpx
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

router = APIRouter()

_CP_URL = os.environ.get("CONTROL_PLANE_URL", "http://localhost:8001")


class PolicyUpdateBody(BaseModel):
    version: str


class SimulateRunsBody(BaseModel):
    runs_per_agent: int = 20


@router.get("/demo")
async def demo_page() -> FileResponse:
    return FileResponse("dashboard/static/demo.html")


@router.post("/api/demo/register-fleet")
async def register_fleet() -> JSONResponse:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(f"{_CP_URL}/demo/register-fleet")
        return JSONResponse(resp.json(), status_code=resp.status_code)


@router.get("/api/demo/fleet-status")
async def fleet_status() -> JSONResponse:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{_CP_URL}/fleet/status")
        return JSONResponse(resp.json(), status_code=resp.status_code)


@router.post("/api/demo/trigger-policy-update")
async def trigger_policy_update(body: PolicyUpdateBody) -> JSONResponse:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{_CP_URL}/policy/update",
            json={"version": body.version},
        )
        return JSONResponse(resp.json(), status_code=resp.status_code)


@router.post("/api/demo/simulate-runs")
async def simulate_runs(body: SimulateRunsBody) -> JSONResponse:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{_CP_URL}/demo/simulate-runs",
            json={"runs_per_agent": body.runs_per_agent},
        )
        return JSONResponse(resp.json(), status_code=resp.status_code)


@router.post("/api/demo/reset")
async def reset_demo() -> JSONResponse:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(f"{_CP_URL}/demo/reset")
        return JSONResponse(resp.json(), status_code=resp.status_code)


@router.get("/api/demo/policy")
async def current_policy() -> JSONResponse:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{_CP_URL}/policy/current")
        return JSONResponse(resp.json(), status_code=resp.status_code)
