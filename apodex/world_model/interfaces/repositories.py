from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from apodex.world_model.domain.timelines import Timeline


class ITimelineRepository(ABC):
    """Repository port for loading and saving versioned Timelines."""

    @abstractmethod
    async def save_timeline(self, timeline: Timeline) -> None:
        """Persist a timeline instance to storage."""
        pass

    @abstractmethod
    async def get_timeline(self, timeline_id: UUID) -> Optional[Timeline]:
        """Load a timeline instance from storage."""
        pass
