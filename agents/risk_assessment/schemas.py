from __future__ import annotations

from pydantic import BaseModel, Field


class RiskInput(BaseModel):
    supplier_id: str
    region: str
    disruption_type: str
    affected_volume_pct: float = Field(ge=0.0, le=100.0)
    mitigation_options: list[str]


class RiskOutput(BaseModel):
    supplier_id: str
    risk_score: float = Field(ge=0.0, le=100.0)
    severity: str  # low | medium | high | critical
    recommended_actions: list[str]
    escalate: bool
    summary: str
