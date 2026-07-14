from __future__ import annotations
from typing import Any, Dict, List
from pydantic import BaseModel, Field

from apodex.common.graph import DirectedGraph


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


class WorldGraph(DirectedGraph[EntityNode, RelationshipEdge]):
    """Domain-agnostic WorldGraph abstraction for handling multi-graph entity resolution and links."""

    def __init__(self) -> None:
        super().__init__()
        self.beliefs: Dict[str, BeliefNode] = {}

    def _make_placeholder_node(self, node_id: str) -> EntityNode:
        return EntityNode(node_id=node_id, node_type="unknown")

    def add_belief(self, belief: BeliefNode) -> None:
        """Add a BeliefNode associating Bayesian confidence over some edge."""
        self.beliefs[belief.belief_id] = belief
