from __future__ import annotations

from pydantic import BaseModel


class InventoryInput(BaseModel):
    sku: str
    warehouse: str
    current_stock: int
    reorder_point: int
    demand_forecast_30d: int


class InventoryOutput(BaseModel):
    sku: str
    alert_type: str  # none | low_stock | critical | overstock
    recommended_action: str
    urgency: str  # routine | urgent | critical
    summary: str
