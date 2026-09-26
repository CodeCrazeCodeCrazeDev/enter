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

    def create_node(self, node_id: str, name: str, description: str = "") -> CausalNode:
        """Creates and registers a causal node in the World Model."""
        node = CausalNode(node_id=node_id, node_type="hypothesis_node", properties={"name": name, "description": description})
        self.add_node(node)
        return node

    def update_belief(self, node_id: str, observed_outcome: bool, confidence: float = 0.95) -> Dict[str, Any]:
        """Updates recursive Bayesian belief for a node."""
        belief_entry = self.beliefs.get(node_id, {"p_prior": 0.5, "updates_count": 0})
        prior = belief_entry["p_prior"]

        # Conjugate update: likelihood given observation
        likelihood = confidence if observed_outcome else (1.0 - confidence)
        posterior = (likelihood * prior) / max(1e-5, (likelihood * prior + (1.0 - likelihood) * (1.0 - prior)))

        updated_entry = {
            "p_prior": posterior,
            "updates_count": belief_entry["updates_count"] + 1,
            "last_outcome": observed_outcome
        }
        self.beliefs[node_id] = updated_entry
        return updated_entry

    def register_pkc_trace(self, trace: PerceptionKnowledgeChain) -> None:
        """Register a search or reasoning trace with the World Model."""
        self.pkc_traces[str(trace.trace_id)] = trace
