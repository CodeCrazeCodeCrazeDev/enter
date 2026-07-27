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
