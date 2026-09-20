from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from control_plane.config_distributor import ConfigDistributor
from control_plane.policy_engine import PolicyEngine
from control_plane.registry import AgentRegistry

app = FastAPI(title="Supply Chain Control Plane", docs_url=None, redoc_url=None)

_registry = AgentRegistry()
_engine = PolicyEngine()
_distributor = ConfigDistributor(_registry, _engine)


class RegisterRequest(BaseModel):
    agent_name: str
    agent_version: str


class PolicyUpdateRequest(BaseModel):
    version: str


class ConfirmRequest(BaseModel):
    policy_version: str


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "control-plane"})


@app.post("/agents/register")
async def register_agent(req: RegisterRequest) -> JSONResponse:
    record = _registry.register(req.agent_name, req.agent_version)
    return JSONResponse({"agent_id": record.agent_id, "policy_version": record.policy_version})


@app.delete("/agents/{agent_id}")
async def deregister_agent(agent_id: str) -> JSONResponse:
    _registry.deregister(agent_id)
    return JSONResponse({"status": "deregistered"})


@app.post("/agents/{agent_id}/confirm-policy")
async def confirm_policy(agent_id: str, req: ConfirmRequest) -> JSONResponse:
    ok = _registry.confirm_policy(agent_id, req.policy_version)
    if not ok:
        raise HTTPException(status_code=404, detail="Agent not found")
    return JSONResponse({"status": "confirmed"})


@app.get("/fleet/status")
async def fleet_status() -> JSONResponse:
    status = _registry.fleet_status_dict()
    status["current_policy_version"] = _engine.current_version()
    status["propagation_elapsed_seconds"] = _distributor.propagation_elapsed_seconds()
    return JSONResponse(status)


@app.get("/policy/current")
async def current_policy() -> JSONResponse:
    return JSONResponse({
        "version": _engine.current_version(),
        "available": _engine.available_versions(),
        "content": _engine.current_policy(),
    })


@app.post("/policy/update")
async def update_policy(req: PolicyUpdateRequest) -> JSONResponse:
    try:
        await _distributor.distribute_policy(req.version)
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return JSONResponse({
        "status": "distributing",
        "version": req.version,
        "agents_notified": len(_registry.all_agents()),
    })


@app.post("/demo/register-fleet")
async def register_fleet() -> JSONResponse:
    _distributor.seed_fleet()
    return JSONResponse(_registry.fleet_status_dict())


@app.post("/demo/reset")
async def reset_demo() -> JSONResponse:
    await _distributor.distribute_policy("v1")
    return JSONResponse({"status": "reset", "policy_version": "v1"})
