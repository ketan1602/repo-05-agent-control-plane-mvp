from __future__ import annotations

from pydantic import BaseModel, Field


class SupplierInput(BaseModel):
    supplier_id: str
    name: str
    spend_usd: float
    categories: list[str]
    risk_flags: list[str]


class SupplierOutput(BaseModel):
    supplier_id: str
    risk_tier: str  # low | medium | high | critical
    recommendation: str  # approve | watch | audit | terminate
    score: float = Field(ge=0.0, le=100.0)
    summary: str
