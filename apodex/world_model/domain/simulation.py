from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class SimulationRunContext(BaseModel):
    """Context block under which a single simulation run is executed."""
    run_id: UUID = Field(default_factory=uuid4)
    timeline_id: UUID
    start_sim_time: datetime = Field(default_factory=datetime.utcnow)
    end_sim_time: datetime = Field(default_factory=datetime.utcnow)
    step_duration_hours: float = 24.0
    active_forces: Dict[str, Any] = Field(default_factory=dict)
    applied_hypotheses: List[UUID] = Field(default_factory=list)
