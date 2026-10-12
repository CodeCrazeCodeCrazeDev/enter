from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from apodex.common.graph import DirectedGraph, GraphNodeProtocol, GraphEdgeProtocol
from apodex.world_model.graph.searcheyes_models import PerceptionKnowledgeChain


class CausalNode(BaseModel):
    """Represents a state, event, or entity in the World Model (E-K-C-T-U subgraphs)."""

    node_id: str
    node_type: str  # event, state, file, function, test, bug_report, proposal, doc_snippet, etc.
    properties: Dict[str, Any] = Field(default_factory=dict)


class RelationEdge(BaseModel):
    """Represents a causal, temporal, or semantic link between two nodes in the World Model."""

    source_id: str
    target_id: str
    relation_type: str  # causal, temporal, semantic, calls, tests, regresses, documents, proposes_fix_for, etc.
    weight: float = 1.0  # Strength or probability bound (0.0 to 1.0)
    properties: Dict[str, Any] = Field(default_factory=dict)


class WorldModel(DirectedGraph[CausalNode, RelationEdge]):
    """Core Continuous World Model (E-K-C-T-U Multi-Graph) for tracking states, relations, and uncertainties."""

    def __init__(self) -> None:
        super().__init__()
        self.beliefs: Dict[str, Dict[str, Any]] = {}
        # Support for Perception-Knowledge Chain (PKC) trace logging
        self.pkc_traces: Dict[str, PerceptionKnowledgeChain] = {}

    def _make_placeholder_node(self, node_id: str) -> CausalNode:
        return CausalNode(node_id=node_id, node_type="unknown")

    def register_pkc_trace(self, trace: PerceptionKnowledgeChain) -> None:
        """Register a search or reasoning trace with the World Model."""
        self.pkc_traces[str(trace.trace_id)] = trace

    def create_node(self, node_id: str, node_type: str, properties: Optional[Dict[str, Any]] = None) -> CausalNode:
        """Helper method to instantiate and register a CausalNode in the world graph."""
        node = CausalNode(node_id=node_id, node_type=node_type, properties=properties or {})
        self.add_node(node)
        return node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        weight: float = 1.0,
        properties: Optional[Dict[str, Any]] = None
    ) -> RelationEdge:
        """Helper method to instantiate and register a RelationEdge in the world graph."""
        edge = RelationEdge(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            weight=weight,
            properties=properties or {}
        )
        self.add_relation(edge)
        return edge

    def update_belief(self, belief_key: str, prior_probability: float, evidence_weight: float) -> float:
        """Update Bayesian belief posterior state for a given key using evidence weight."""
        existing = self.beliefs.get(belief_key, {})
        prior = existing.get("probability", prior_probability)
        # Bayesian update approximation
        likelihood = max(0.01, min(0.99, evidence_weight))
        numerator = likelihood * prior
        denominator = numerator + ((1.0 - likelihood) * (1.0 - prior))
        posterior = numerator / denominator if denominator > 0 else prior

        self.beliefs[belief_key] = {
            "probability": float(posterior),
            "updated_at": datetime_now_iso(),
            "updates_count": existing.get("updates_count", 0) + 1
        }
        return float(posterior)


def datetime_now_iso() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
