from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

router = APIRouter()

_OVERVIEW = {
    "article_number": "05",
    "repo_name": "repo-05-agent-control-plane-mvp",
    "central_claim": (
        "Fleet governance is the missing layer. Without a control plane, "
        "policy changes require touching every agent manually."
    ),
    "key_finding": (
        "Fleet-wide policy update: 7 seconds with control plane. "
        "47 minutes manually (7 agents × ~7 min each)."
    ),
    "use_case": "Supply Chain Fleet — 7 agents governed by a shared control plane",
    "series_position": "Demonstrates fleet governance and policy propagation at scale",
    "next_repo": "repo-06-harness-engineering-playbook",
}


@router.get("/")
async def overview_page() -> FileResponse:
    return FileResponse("dashboard/static/index.html")


@router.get("/api/overview")
async def overview_data() -> JSONResponse:
    return JSONResponse(_OVERVIEW)
