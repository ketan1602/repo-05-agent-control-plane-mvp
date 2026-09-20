from __future__ import annotations

from pydantic import BaseModel, Field


class QualityInput(BaseModel):
    batch_id: str
    supplier_id: str
    product_sku: str
    defect_count: int
    sample_size: int
    defect_types: list[str]


class QualityOutput(BaseModel):
    batch_id: str
    disposition: str  # accept | quarantine | reject
    defect_rate: float = Field(ge=0.0, le=1.0)
    requires_hold: bool
    recommended_action: str
    summary: str
