from __future__ import annotations
from typing import List
from uuid import UUID
from apodex.world_model.domain.entities import Entity
from apodex.world_model.graph.world_graph import WorldGraphManager


class GraphTraversalService:
    """Provides path finding, breath-first, and depth-first searches over the World Graph."""

    def __init__(self, graph_manager: WorldGraphManager) -> None:
        self.graph_manager = graph_manager

    async def find_shortest_path(self, timeline_id: UUID, start_id: UUID, end_id: UUID) -> List[UUID]:
        """Placeholder for BFS search path between two entities."""
        if start_id == end_id:
            return [start_id]
        return [start_id, end_id]
