from __future__ import annotations
from typing import Dict
from pydantic import BaseModel, Field


class EnvironmentVector(BaseModel):
    """Domain model representing high-dimensional global background variables."""
    meteorological_state: Dict[str, float] = Field(default_factory=dict)
    macroeconomic_indicators: Dict[str, float] = Field(default_factory=dict)
    regulatory_frame_indices: Dict[str, float] = Field(default_factory=dict)
    geopolitical_risk_factors: Dict[str, float] = Field(default_factory=dict)
