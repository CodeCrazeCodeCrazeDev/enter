from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Entity(BaseModel):
    """Storage-independent domain Entity representing any object, place, or concept."""
    entity_id: UUID = Field(default_factory=uuid4)
    name: str
    entity_type: str  # e.g., "PERSON", "ORGANIZATION", "METRIC", "GEOGRAPHY", "TECHNOLOGY"
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

    def update_property(self, key: str, value: Any) -> None:
        """Update a specific metadata property of the Entity."""
        self.properties[key] = value
        self.updated_at = datetime.now(timezone.utc)
