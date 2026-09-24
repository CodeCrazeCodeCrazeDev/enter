from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict
from pydantic import BaseModel, Field


class CognitiveEvent(BaseModel):
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
