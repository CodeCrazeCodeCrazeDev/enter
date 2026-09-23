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

    def ingest_cross_layer_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Ingest a cross-layer active inference event into the Causal Graph and update beliefs."""
        hyp_id = payload.get("hypothesis_id", "hyp_unknown")
        title = payload.get("title", event_type)

        node = CausalNode(
            node_id=f"research_hyp_{hyp_id}",
            node_type="research_hypothesis",
            properties={
                "title": title,
                "event_type": event_type,
                "is_validated": payload.get("is_validated", False),
                "p_value": payload.get("p_value", 1.0),
                "effect_size": payload.get("effect_size", 0.0)
            }
        )
        self.add_node(node)

        # Update Bayesian belief record
        self.beliefs[hyp_id] = {
            "title": title,
            "validated": payload.get("is_validated", False),
            "posterior_probability": 0.95 if payload.get("is_validated") else 0.10,
            "p_value": payload.get("p_value", 1.0)
        }
