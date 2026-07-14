"""Shared domain models for the AEAN (Autonomous Economic Actor Network).

All monetary values are represented in integer cents to avoid floating point
drift, matching the convention used elsewhere in the ``apodex`` codebase.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.utcnow()


class MicroCellStatus(str, Enum):
    """Lifecycle state of an autonomous micro-cell."""

    PROPOSED = "proposed"
    ACTIVE = "active"
    SCALED = "scaled"
    KILLED = "killed"


class EngineName(str, Enum):
    """The six engines that make up the AEAN organism (4 economic + 2 coordination)."""

    PAEAN = "PAEAN"
    ADE = "ADE"
    ARE = "ARE"
    AVIE = "AVIE"
    HIVE_MIND = "HiveMind"
    RESEARCH = "Research"


class DemandSignal(BaseModel):
    """A detected demand opportunity emitted by ADE and consumed by PAEAN."""

    signal_id: str = Field(default_factory=_uuid)
    market: str
    segment: str
    strength: float = Field(ge=0.0, le=1.0)
    estimated_tam_cents: int = Field(ge=0)
    elasticity: float = Field(default=-1.5, description="Price elasticity of demand (negative).")
    keywords: List[str] = Field(default_factory=list)
    detected_at: datetime = Field(default_factory=_now)


class Narrative(BaseModel):
    """A narrative/perception strategy produced by ADE for a demand signal."""

    narrative_id: str = Field(default_factory=_uuid)
    signal_id: str
    theme: str
    hook: str
    body: str
    predicted_resonance: float = Field(ge=0.0, le=1.0)
    generated_by: str = "simulation"


class VisualAsset(BaseModel):
    """A campaign-ready creative asset produced by AVIE."""

    asset_id: str = Field(default_factory=_uuid)
    narrative_id: str
    concept: str
    format: str = "social_square"
    predicted_ctr: float = Field(ge=0.0, le=1.0)
    prompt: str = ""
    generated_by: str = "simulation"


class MicroCell(BaseModel):
    """An autonomous economic unit spawned by PAEAN with bounded capital."""

    cell_id: str = Field(default_factory=_uuid)
    signal_id: str
    market: str
    segment: str
    status: MicroCellStatus = MicroCellStatus.PROPOSED
    allocated_cents: int = Field(default=0, ge=0)
    deployed_cents: int = Field(default=0, ge=0)
    revenue_cents: int = Field(default=0, ge=0)
    cycles_run: int = 0
    scale_count: int = 0
    kill_threshold_roi: float = -0.25
    scale_threshold_roi: float = 0.30
    created_at: datetime = Field(default_factory=_now)

    @property
    def roi(self) -> float:
        """Return on deployed capital for this cell."""
        if self.deployed_cents <= 0:
            return 0.0
        return (self.revenue_cents - self.deployed_cents) / self.deployed_cents


class CycleResult(BaseModel):
    """Summary of a single compounding-flywheel iteration."""

    cycle: int
    timestamp: datetime = Field(default_factory=_now)
    signals_detected: int = 0
    narratives_created: int = 0
    assets_produced: int = 0
    active_cells: int = 0
    capital_deployed_cents: int = 0
    revenue_cents: int = 0
    treasury_cents: int = 0
    portfolio_roi: float = 0.0
    cells_killed: int = 0
    cells_scaled: int = 0
    governance_blocks: int = 0
    notes: List[str] = Field(default_factory=list)


class OrganismState(BaseModel):
    """Point-in-time snapshot of the whole organism, used by the dashboard."""

    cycle: int = 0
    treasury_cents: int = 0
    initial_capital_cents: int = 0
    total_revenue_cents: int = 0
    total_deployed_cents: int = 0
    active_cells: int = 0
    killed_cells: int = 0
    scaled_cells: int = 0
    cumulative_roi: float = 0.0
    history: List[CycleResult] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=_now)
