"""Polymorphic Data Models for the Cognitive Memory Operating System (CMOS).

Defines the specialized nodes and edges constituting the active CMOS Memory Graph.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class CMOSNodeType(str, Enum):
    CLAIM = "claim"
    EVIDENCE = "evidence"
    THEORY = "theory"
    STRATEGY = "strategy"
    REGIME = "regime"
    MODEL = "model"
    DECISION = "decision"
    LESSON = "lesson"
    FAILURE = "failure"
    HYPOTHESIS = "hypothesis"
    EXPERIMENT = "experiment"


class CMOSEdgeType(str, Enum):
    CAUSAL = "causal"
    SUPPORT = "support"
    CONTRADICTS = "contradicts"
    LINEAGE = "lineage"
    TEMPORAL = "temporal"


class NodeState(str, Enum):
    PROPOSED = "proposed"
    VALIDATED = "validated"
    REFUTED = "refuted"
    ARCHIVED = "archived"


class ProvenanceBlock(BaseModel):
    """Immutable metadata tracking the origin, creation, and authorization of memory entities."""
    origin: str = Field(..., description="Subsystem or component that generated this entity.")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    creator_id: str = Field(..., description="Identifier of the executing agent or actor.")
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    git_sha: str = Field("unknown", description="System code version fingerprint.")
    experiment_id: Optional[UUID] = Field(None, description="Optional link to active scientific test context.")
    reasoning_path: List[str] = Field(default_factory=list, description="Sequence of accessed nodes.")


class MemoryNode(BaseModel):
    """Core polymorphic Node schema for CMOS."""
    node_id: str = Field(default_factory=lambda: f"node_{uuid4().hex[:12]}")
    node_type: CMOSNodeType = Field(...)
    state: NodeState = Field(default=NodeState.PROPOSED)
    label: str = Field(..., min_length=2, max_length=256)
    content: str = Field(..., description="Assertion, observation, or configuration content.")
    provenance: ProvenanceBlock = Field(...)
    utility: float = Field(1.0, ge=0.0, description="Computed resource economics utility score.")
    retrieval_count: int = Field(0, ge=0)
    last_retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryEdge(BaseModel):
    """Core polymorphic Edge schema for CMOS."""
    edge_id: str = Field(default_factory=lambda: f"edge_{uuid4().hex[:12]}")
    source_id: str = Field(..., description="Origin node UUID.")
    target_id: str = Field(..., description="Target node UUID.")
    edge_type: CMOSEdgeType = Field(...)
    strength: float = Field(1.0, description="Quantified relationship or support strength.")
    provenance: ProvenanceBlock = Field(...)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryGraph(BaseModel):
    """Representational logical slice of the Memory Graph."""
    nodes: Dict[str, MemoryNode] = Field(default_factory=dict)
    edges: List[MemoryEdge] = Field(default_factory=list)
