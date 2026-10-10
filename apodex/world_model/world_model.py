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
        """Helper to create and add a CausalNode to the graph."""
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
        """Helper to create and add a RelationEdge to the graph."""
        edge = RelationEdge(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            weight=weight,
            properties=properties or {}
        )
        self.add_relation(edge)
        return edge

    def update_belief(self, key: str, confidence: float, evidence_count: int = 1) -> Dict[str, Any]:
        """Update Bayesian belief entry in WorldModel."""
        prior = self.beliefs.get(key, {"confidence": 0.5, "evidence_count": 0})
        new_evidence_count = prior["evidence_count"] + evidence_count
        # Bayesian update formula simulation
        updated_confidence = (prior["confidence"] * prior["evidence_count"] + confidence * evidence_count) / max(1, new_evidence_count)
        belief_entry = {
            "confidence": float(updated_confidence),
            "evidence_count": new_evidence_count
        }
        self.beliefs[key] = belief_entry
        return belief_entry
