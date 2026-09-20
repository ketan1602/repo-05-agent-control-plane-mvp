from __future__ import annotations

from pydantic import BaseModel


class TradeInput(BaseModel):
    transaction_id: str
    origin_country: str
    destination_country: str
    hs_code: str
    value_usd: float
    product_desc: str


class TradeOutput(BaseModel):
    transaction_id: str
    compliant: bool
    flags: list[str]
    required_licenses: list[str]
    risk_level: str  # low | medium | high
    summary: str
