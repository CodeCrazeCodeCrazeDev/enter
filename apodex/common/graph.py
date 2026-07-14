"""Shared directed-graph primitives for World Model style graphs.

Several subsystems maintain a directed multigraph of typed nodes and weighted
relations (entity/causal graphs). This module centralises the storage, edge
deduplication and breadth-first pathfinding logic so those subsystems only need
to declare their concrete node/edge models.
"""

from __future__ import annotations

import logging
from typing import Dict, Generic, List, Optional, Protocol, TypeVar

logger = logging.getLogger("apodex.common.graph")


class GraphNodeProtocol(Protocol):
    node_id: str
    node_type: str


class GraphEdgeProtocol(Protocol):
    source_id: str
    target_id: str
    relation_type: str
    weight: float
    properties: Dict


NodeT = TypeVar("NodeT", bound=GraphNodeProtocol)
EdgeT = TypeVar("EdgeT", bound=GraphEdgeProtocol)


class DirectedGraph(Generic[NodeT, EdgeT]):
    """Directed multigraph with node storage, edge dedup and BFS pathfinding.

    Subclasses implement :meth:`_make_placeholder_node` to describe how an
    unknown endpoint referenced by a relation should be materialised.
    """

    def __init__(self) -> None:
        self.nodes: Dict[str, NodeT] = {}
        self.edges: List[EdgeT] = []

    def _make_placeholder_node(self, node_id: str) -> NodeT:
        """Create a node for an endpoint referenced by a relation but not yet added."""
        raise NotImplementedError

    def add_node(self, node: NodeT) -> None:
        """Add or update a node in the graph."""
        self.nodes[node.node_id] = node
        logger.debug("Added node %s (%s)", node.node_id, node.node_type)

    def add_relation(self, edge: EdgeT) -> None:
        """Add a relation, creating missing endpoints and deduplicating by triple."""
        if edge.source_id not in self.nodes:
            self.add_node(self._make_placeholder_node(edge.source_id))
        if edge.target_id not in self.nodes:
            self.add_node(self._make_placeholder_node(edge.target_id))

        for existing in self.edges:
            if (
                existing.source_id == edge.source_id
                and existing.target_id == edge.target_id
                and existing.relation_type == edge.relation_type
            ):
                existing.weight = edge.weight
                existing.properties.update(edge.properties)
                return
        self.edges.append(edge)
        logger.debug(
            "Added relation %s --(%s)--> %s",
            edge.source_id,
            edge.relation_type,
            edge.target_id,
        )

    def get_relations_from(self, source_id: str) -> List[EdgeT]:
        """Query relations originating from a specific node."""
        return [e for e in self.edges if e.source_id == source_id]

    def get_relations_to(self, target_id: str) -> List[EdgeT]:
        """Query relations directed into a specific node."""
        return [e for e in self.edges if e.target_id == target_id]

    def find_path(
        self, start_id: str, end_id: str, max_depth: int = 5
    ) -> Optional[List[str]]:
        """Find a directed path between two nodes using breadth-first search."""
        if start_id not in self.nodes or end_id not in self.nodes:
            return None

        queue: List[List[str]] = [[start_id]]
        visited = {start_id}

        while queue:
            path = queue.pop(0)
            current = path[-1]

            if current == end_id:
                return path

            for edge in self.get_relations_from(current):
                if edge.target_id not in visited:
                    visited.add(edge.target_id)
                    queue.append([*path, edge.target_id])

        return None
