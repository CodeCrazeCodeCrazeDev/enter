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

    def create_node(self, node: CausalNode) -> None:
        """Alias for add_node to support unified 4-layer WorldModel creation contract."""
        self.add_node(node)

    def update_belief(self, hypothesis_id: str, evidence_signal: float, source_agent: str = "system") -> None:
        """Update or initialize a Bayesian belief entry in the world model."""
        from apodex.world_model.domain.beliefs import Belief
        if hypothesis_id in self.beliefs:
            existing = self.beliefs[hypothesis_id]
            if isinstance(existing, Belief):
                existing.prior_probability = 0.5 * existing.prior_probability + 0.5 * evidence_signal
            else:
                existing["prior_probability"] = 0.5 * existing.get("prior_probability", 0.5) + 0.5 * evidence_signal
        else:
            belief = Belief(
                belief_id=hypothesis_id,
                target_id=hypothesis_id,
                probability=evidence_signal,
                evidence=[f"source:{source_agent}"]
            )
            self.beliefs[hypothesis_id] = belief
