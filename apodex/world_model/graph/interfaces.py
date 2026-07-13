from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID

from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.relationships import Relationship
from apodex.world_model.domain.beliefs import Belief


class IWorldGraphQueryService(ABC):
    """Abstract interface for querying World Graph topologies and entities across timelines."""

    @abstractmethod
    async def get_entity(self, timeline_id: UUID, entity_id: UUID) -> Optional[Entity]:
        """Fetch an Entity by ID from a given timeline view."""
        pass

    @abstractmethod
    async def get_neighbors(self, timeline_id: UUID, entity_id: UUID, relation_types: Optional[List[str]] = None) -> List[Entity]:
        """Traverse neighbors of an Entity in a given timeline view."""
        pass

    @abstractmethod
    async def get_relationships(self, timeline_id: UUID, entity_id: UUID) -> List[Relationship]:
        """Get all relationships attached to an Entity."""
        pass

    @abstractmethod
    async def get_belief_state(self, timeline_id: UUID, target_id: UUID) -> Optional[Belief]:
        """Fetch the active Bayesian belief state for an Entity or Relationship."""
        pass
