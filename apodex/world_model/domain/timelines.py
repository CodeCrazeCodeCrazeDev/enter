from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class WorldGraphDelta(BaseModel):
    """Encapsulates a single structural modification to a parent timeline graph."""
    delta_type: str  # "ADD_ENTITY", "REMOVE_ENTITY", "ADD_RELATION", "REMOVE_RELATION", "UPDATE_BELIEF"
    target_id: UUID
    payload: Dict[str, Any] = Field(default_factory=dict)


class Timeline(BaseModel):
    """Storage-independent timeline branch. Acts as an isolated simulation environment."""
    timeline_id: UUID = Field(default_factory=uuid4)
    parent_timeline_id: Optional[UUID] = None  # None for main reality timeline
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    branch_point_sim_time: datetime = Field(default_factory=datetime.utcnow)
    deltas: List[WorldGraphDelta] = Field(default_factory=list)
    is_committed: bool = False

    def commit(self) -> None:
        """Mark this timeline as committed and read-only."""
        self.is_committed = True

    def add_delta(self, delta: WorldGraphDelta) -> None:
        """Append a structural delta to this branch if not committed."""
        if self.is_committed:
            raise ValueError("Cannot append delta to a committed read-only timeline.")
        self.deltas.append(delta)
