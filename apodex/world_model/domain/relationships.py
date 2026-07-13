from __future__ import annotations
from typing import Any, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Relationship(BaseModel):
    """Storage-independent domain Relationship representing a directed causal or semantic link."""
    relationship_id: UUID = Field(default_factory=uuid4)
    source_id: UUID
    target_id: UUID
    relation_type: str  # e.g., "COMPETES_WITH", "INFLUENCES", "REGULATES", "SUPPLIES", "CAUSES"
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    properties: Dict[str, Any] = Field(default_factory=dict)
