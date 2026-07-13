from __future__ import annotations
from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Entity(BaseModel):
    """Storage-independent domain Entity representing any object, place, or concept."""
    entity_id: UUID = Field(default_factory=uuid4)
    name: str
    entity_type: str  # e.g., "PERSON", "ORGANIZATION", "METRIC", "GEOGRAPHY", "TECHNOLOGY"
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_property(self, key: str, value: Any) -> None:
        """Update a specific metadata property of the Entity."""
        self.properties[key] = value
        self.updated_at = datetime.utcnow()
