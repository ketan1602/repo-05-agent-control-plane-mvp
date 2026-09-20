from __future__ import annotations

from pydantic import BaseModel


class LogisticsInput(BaseModel):
    shipment_id: str
    origin: str
    destination: str
    weight_kg: float
    priority: str  # standard | express | critical
    deadline_days: int


class LogisticsOutput(BaseModel):
    shipment_id: str
    route: str
    carrier: str
    estimated_days: int
    cost_usd: float
    summary: str
