from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.world_graph")


class EntityNode(BaseModel):
    """Represents a physical/digital entity in the World Model (e.g. market, product, competitor, user)."""

    node_id: str
    node_type: str  # market, product, competitor, risk, customer, resource
    properties: Dict[str, Any] = Field(default_factory=dict)


class RelationshipEdge(BaseModel):
    """Represents a directed link/association between two entities (e.g. COMPETES_WITH, BUYS, CAUSES)."""

    source_id: str
    target_id: str
    relation_type: str  # COMPETES_WITH, BUYS_FROM, CAUSES, REGULATES, ASSUMES
    weight: float = 1.0  # Strength or probability of link (0.0 to 1.0)
    properties: Dict[str, Any] = Field(default_factory=dict)


class BeliefNode(BaseModel):
    """Represents an epistemic belief or hypothesis mapped to a structural relationship."""

    belief_id: str
    target_edge_id: str  # References a composite representation or specific edge
    probability: float = Field(default=0.5, ge=0.0, le=1.0)  # Bayesian belief confidence
    evidence: List[str] = Field(default_factory=list)  # Hashes or URI references to raw evidence


class WorldGraph:
    """Domain-agnostic WorldGraph abstraction for handling multi-graph entity resolution and links."""

    def __init__(self) -> None:
        self.nodes: Dict[str, EntityNode] = {}
        self.edges: List[RelationshipEdge] = []
        self.beliefs: Dict[str, BeliefNode] = {}

    def add_node(self, node: EntityNode) -> None:
        """Add or update an EntityNode in the graph."""
        self.nodes[node.node_id] = node
        logger.debug(f"Added EntityNode to WorldGraph: {node.node_id} ({node.node_type})")

    def add_relation(self, edge: RelationshipEdge) -> None:
        """Add a RelationshipEdge to the graph."""
        # Ensure nodes exist
        if edge.source_id not in self.nodes:
            self.add_node(EntityNode(node_id=edge.source_id, node_type="unknown"))
        if edge.target_id not in self.nodes:
            self.add_node(EntityNode(node_id=edge.target_id, node_type="unknown"))

        # Check for duplicates or update weight
        for existing in self.edges:
            if existing.source_id == edge.source_id and existing.target_id == edge.target_id and existing.relation_type == edge.relation_type:
                existing.weight = edge.weight
                existing.properties.update(edge.properties)
                return
        self.edges.append(edge)
        logger.debug(f"Added RelationshipEdge: {edge.source_id} --({edge.relation_type})--> {edge.target_id}")

    def add_belief(self, belief: BeliefNode) -> None:
        """Add a BeliefNode associating Bayesian confidence over some edge."""
        self.beliefs[belief.belief_id] = belief
        logger.debug(f"Added BeliefNode: {belief.belief_id} (P={belief.probability})")

    def get_relations_from(self, source_id: str) -> List[RelationshipEdge]:
        """Query relations originating from a specific node."""
        return [e for e in self.edges if e.source_id == source_id]

    def get_relations_to(self, target_id: str) -> List[RelationshipEdge]:
        """Query relations directed into a specific node."""
        return [e for e in self.edges if e.target_id == target_id]

    def find_path(self, start_id: str, end_id: str, max_depth: int = 5) -> Optional[List[str]]:
        """Find a path (directed node list) between two entity nodes using BFS."""
        if start_id not in self.nodes or end_id not in self.nodes:
            return None

        queue: List[List[str]] = [[start_id]]
        visited = {start_id}

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == end_id:
                return path

            for edge in self.get_relations_from(node):
                if edge.target_id not in visited:
                    visited.add(edge.target_id)
                    new_path = list(path)
                    new_path.append(edge.target_id)
                    queue.append(new_path)

        return None
