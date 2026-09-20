from __future__ import annotations

from pydantic import BaseModel, Field


class DemandInput(BaseModel):
    product_id: str
    historical_30d: int
    seasonal_index: float
    promotions_active: bool


class DemandOutput(BaseModel):
    product_id: str
    forecast_30d: int
    confidence: float = Field(ge=0.0, le=1.0)
    demand_drivers: list[str]
    summary: str
