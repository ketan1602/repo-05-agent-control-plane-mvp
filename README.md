# repo-05 — Agent Control Plane MVP (Beyond the Model, Article 05)

Fleet governance for a set of LangGraph agents. A control plane tracks which agents are running, pushes a policy version to all of them, and reports how long propagation takes. The demo fleet is seven supply chain agents; policy v1 is rolled out to v2 from the dashboard.

Article claim being demonstrated: a policy change reaches the whole fleet in about 7 seconds through the control plane, versus roughly 47 minutes if each of 7 agents is updated by hand at about 7 minutes each.

## Architecture

Two FastAPI apps run side by side:

| App | Port | Module | Role |
|---|---|---|---|
| Control plane | 8001 | `control_plane/server.py` | Fleet registry, policy engine, policy distribution |
| Dashboard | 8000 | `dashboard/app.py` | Article pages; proxies fleet and policy calls to the control plane via httpx |

Control plane components:

- `control_plane/registry.py` — `AgentRegistry`, in-memory fleet state
- `control_plane/policy_engine.py` — `PolicyEngine`, loads and caches YAML policies from `policies/`
- `control_plane/config_distributor.py` — `ConfigDistributor`, marks agents `policy_pending` and confirms each one asynchronously with a random 0.4–1.8 s delay
- `sdk/cp_plugin.py` — `ControlPlanePlugin`, used by agents to register and confirm policy

Agents are built on `agents/base.py`. Each of the seven agents (`supplier_evaluation`, `inventory_monitor`, `demand_forecast`, `logistics_routing`, `quality_inspection`, `trade_compliance`, `risk_assessment`) has a `schemas.py` (Pydantic input/output models), an `agent.py` (system prompt), and an `__init__.py`. Each one is a single-node `StateGraph(dict)` wrapped by `agent-harness-core`.

Frameworks and services:

- Agent graphs: LangGraph
- LLM calls: AI Refinery through `airefinery-sdk` (`AsyncAIRefinery`), default model `openai/gpt-oss-120b`
- Lifecycle, retry, I/O validation, audit: `agent-harness-core` (installed from `../agent-harness-core`)

## Policies

- `policies/supply_chain_v1.yaml` — baseline. Max supplier risk tier `high`, defect threshold `0.05`, no trade restrictions.
- `policies/supply_chain_v2.yaml` — tightened. Max supplier risk tier `medium`, `restricted_hs_codes` (`8471.30`, `8542.31`), `restricted_origin_countries`, stricter thresholds.

## Setup

Requirements: Python 3.11+, and `agent-harness-core` checked out as a sibling directory at `../agent-harness-core`.

1. Create a virtualenv and install the package with dev extras.

   ```bash
   python -m venv .venv
   ```

   ```bash
   source .venv/bin/activate
   ```

   ```bash
   pip install -e ".[dev]"
   ```

2. Create your local env file from the template.

   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and set `AIREFINERY_API_KEY`. Leave other values at their defaults unless you need to change them. The key is read from the environment only; it is never hardcoded or logged. `.env` is gitignored.

## Run

Open two terminals in the repo root, with the virtualenv active and `.env` loaded.

Terminal 1 — control plane:

```bash
uvicorn control_plane.server:app --port 8001
```

Terminal 2 — dashboard:

```bash
uvicorn dashboard.app:app --port 8000
```

Then open `http://localhost:8000` in a browser.

## Demo walkthrough

1. Open `http://localhost:8000/demo`.
2. On page load the dashboard calls `POST /api/demo/register-fleet`, which the control plane serves as `POST /demo/register-fleet`. This resets the registry and registers the seven agents on v1.
3. Watch the fleet table. All seven agents show policy v1 with status `policy_confirmed`.
4. Click **Trigger Policy v2**. The control plane marks all agents `policy_pending` and starts per-agent confirmations in the background. The dashboard polls `/api/demo/fleet-status` every second and shows a live propagation timer.
5. When every agent is back to `policy_confirmed` on v2, the timer stops. Compare the propagation time with the manual-equivalent figure on `/metrics`.
6. Click **Reset to v1** to run the demo again. This calls `POST /api/demo/reset` on the dashboard.

Other dashboard pages:

- `/` — article overview and key finding
- `/metrics` — stat tiles and SVG charts (propagation time, fleet visibility, comparison table)
- `/eval` — eval fixtures covering four of the seven agents

Control plane endpoints used by the demo:

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness |
| POST | `/agents/register` | Register an agent |
| DELETE | `/agents/{agent_id}` | Deregister an agent |
| POST | `/agents/{agent_id}/confirm-policy` | Agent confirms a policy version |
| GET | `/fleet/status` | Fleet state |
| GET | `/policy/current` | Current policy version |
| POST | `/policy/update` | Distribute a policy version |
| POST | `/demo/register-fleet` | Reset and seed the seven-agent fleet |
| POST | `/demo/reset` | Clear the fleet |

## Tests

```bash
pytest
```

```bash
ruff check .
```

The test suite has 30 tests covering agent schemas and harness construction (`tests/test_agents.py`), control plane registry, policy engine and endpoints (`tests/test_control_plane.py`), and dashboard pages and proxying (`tests/test_dashboard.py`). Tests use `ASGITransport` for in-process FastAPI calls and a `MagicMock` for the httpx response.

## Known limitations

- The fleet is simulated. There are no seven running agent processes; `seed_fleet()` registers seven records and `distribute_policy()` simulates their confirmation delays.
- Token usage is not captured by the harness cost tracker, because AI Refinery calls go directly through `AsyncAIRefinery` rather than LangChain callbacks. `cost_usd` reports 0.
- Registry and policy state are in-memory and reset on process restart.
- The `measurements/fleet_metrics.json` file is a placeholder with zeroed values until a demo run populates it.
