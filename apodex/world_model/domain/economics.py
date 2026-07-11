from __future__ import annotations
from typing import Dict, List
from pydantic import BaseModel, Field


class UnitEconomics(BaseModel):
    """SaaS metrics or project business unit economics."""
    customer_acquisition_cost_usd: float = 0.0
    lifetime_value_usd: float = 0.0
    monthly_recurring_revenue_usd: float = 0.0
    churn_rate: float = 0.0


class SupplyChainNode(BaseModel):
    """Coordinates of a logistics or supply-chain simulation segment."""
    capacity: float = 0.0
    latency_hours: float = 0.0
    unit_cost_usd: float = 0.0
    inventory_volume: float = 0.0


class PriceElasticityCurve(BaseModel):
    """Mathematical mapping of price points to projected conversion rates."""
    points: Dict[float, float] = Field(default_factory=dict)  # e.g., {29.99: 0.12, 49.99: 0.08}
