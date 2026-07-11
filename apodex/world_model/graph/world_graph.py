from __future__ import annotations
from typing import Any, Dict, List, Optional
from uuid import UUID

from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.relationships import Relationship
from apodex.world_model.domain.beliefs import Belief
from apodex.world_model.graph.interfaces import IWorldGraphQueryService


class WorldGraphManager(IWorldGraphQueryService):
    """Storage-independent World Graph manager coordinating structural traversals."""

    def __init__(self, entities: Optional[Dict[UUID, Entity]] = None,
                 relationships: Optional[List[Relationship]] = None,
                 beliefs: Optional[Dict[UUID, Belief]] = None) -> None:
        self._entities = entities or {}
        self._relationships = relationships or []
        self._beliefs = beliefs or {}

    async def get_entity(self, timeline_id: UUID, entity_id: UUID) -> Optional[Entity]:
        return self._entities.get(entity_id)

    async def get_neighbors(self, timeline_id: UUID, entity_id: UUID,
                            relation_types: Optional[List[str]] = None) -> List[Entity]:
        neighbors = []
        for rel in self._relationships:
            if rel.source_id == entity_id:
                if relation_types is None or rel.relation_type in relation_types:
                    if rel.target_id in self._entities:
                        neighbors.append(self._entities[rel.target_id])
        return neighbors

    async def get_relationships(self, timeline_id: UUID, entity_id: UUID) -> List[Relationship]:
        return [rel for rel in self._relationships if rel.source_id == entity_id or rel.target_id == entity_id]

    async def get_belief_state(self, timeline_id: UUID, target_id: UUID) -> Optional[Belief]:
        return self._beliefs.get(target_id)
