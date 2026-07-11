from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("apodex.world_model")


class CausalNode(BaseModel):
    """Represents a state, event, or entity in the World Model (E-K-C-T-U subgraphs)."""

    node_id: str
    node_type: str  # event, state, product, competitor, market, etc.
    properties: Dict[str, Any] = Field(default_factory=dict)


class RelationEdge(BaseModel):
    """Represents a causal, temporal, or semantic link between two nodes in the World Model."""

    source_id: str
    target_id: str
    relation_type: str  # causal, temporal, semantic, buys, competes, etc.
    weight: float = 1.0  # Strength or probability bound (0.0 to 1.0)
    properties: Dict[str, Any] = Field(default_factory=dict)


class WorldModel:
    """Core Continuous World Model (E-K-C-T-U Multi-Graph) for tracking states, relations, and uncertainties."""

    def __init__(self) -> None:
        self.nodes: Dict[str, CausalNode] = {}
        self.edges: List[RelationEdge] = []
        self.beliefs: Dict[str, Dict[str, Any]] = {}

    def add_node(self, node: CausalNode) -> None:
        self.nodes[node.node_id] = node
        logger.debug(f"WorldModel: Added CausalNode {node.node_id} ({node.node_type})")

    def add_relation(self, edge: RelationEdge) -> None:
        # Ensure nodes exist
        if edge.source_id not in self.nodes:
            self.add_node(CausalNode(node_id=edge.source_id, node_type="unknown"))
        if edge.target_id not in self.nodes:
            self.add_node(CausalNode(node_id=edge.target_id, node_type="unknown"))

        # Deduplicate or update weight
        for existing in self.edges:
            if existing.source_id == edge.source_id and existing.target_id == edge.target_id and existing.relation_type == edge.relation_type:
                existing.weight = edge.weight
                existing.properties.update(edge.properties)
                return
        self.edges.append(edge)
        logger.debug(f"WorldModel: Added RelationEdge {edge.source_id} --({edge.relation_type})--> {edge.target_id}")

    def get_relations_from(self, source_id: str) -> List[RelationEdge]:
        return [e for e in self.edges if e.source_id == source_id]

    def get_relations_to(self, target_id: str) -> List[RelationEdge]:
        return [e for e in self.edges if e.target_id == target_id]

    def find_path(self, start_id: str, end_id: str) -> Optional[List[str]]:
        """Breadth-First Search (BFS) directed pathfinding from start node to end node."""
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
                    new_path = list(path)
                    new_path.append(edge.target_id)
                    queue.append(new_path)

        return None
