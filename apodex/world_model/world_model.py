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

    def update_bayesian_belief(self, belief_key: str, new_evidence_weight: float, domain: str = "general") -> None:
        """Update Bayesian belief state in the World Model."""
        current = self.beliefs.get(belief_key, {"probability": 0.5, "weight": 1.0})
        prior_p = current.get("probability", 0.5)
        posterior_p = prior_p * (1.0 + 0.1 * new_evidence_weight)
        posterior_p = max(0.01, min(0.99, posterior_p))
        self.beliefs[belief_key] = {
            "probability": posterior_p,
            "weight": current.get("weight", 1.0) + new_evidence_weight,
            "domain": domain
        }

    def add_causal_relation(self, source: str, target: str, effect_size: float = 0.5) -> None:
        """Add a causal relationship edge between two domain nodes."""
        src_node = CausalNode(node_id=source, node_type="domain_concept")
        tgt_node = CausalNode(node_id=target, node_type="domain_concept")
        self.add_node(src_node)
        self.add_node(tgt_node)
        edge = RelationEdge(source_id=source, target_id=target, relation_type="causal", weight=effect_size)
        self.add_relation(edge)
