from __future__ import annotations
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

# -------------------------------------------------------------
# 1. SearchEyes Node Typings (prefixed with SearchEyes to avoid pytest collection warnings)
# -------------------------------------------------------------

class TypedNodePayload(BaseModel):
    """Base model payload for node-specific metadata."""
    pass


class FileNodePayload(TypedNodePayload):
    file_path: str
    language: str = "python"
    loc: int = 0


class FunctionNodePayload(TypedNodePayload):
    function_name: str
    signature: str = ""
    file_path: str


class SearchEyesTestNodePayload(TypedNodePayload):
    test_name: str
    file_path: str
    framework: str = "pytest"


class BugReportNodePayload(TypedNodePayload):
    bug_id: str
    description: str
    severity: str = "MEDIUM"


class ProposalNodePayload(TypedNodePayload):
    proposal_id: UUID
    title: str
    status: str = "DRAFT"


class DocSnippetNodePayload(TypedNodePayload):
    title: str
    content_summary: str


# -------------------------------------------------------------
# 2. SearchEyes Edge Typings
# -------------------------------------------------------------

class EdgeMetadata(BaseModel):
    provenance: str = "static_analysis"
    confidence: float = 1.0
    timestamp: float = Field(default_factory=lambda: 0.0)


# -------------------------------------------------------------
# 3. Perception-Knowledge Chain (PKC) Core Models
# -------------------------------------------------------------

class PKCHop(BaseModel):
    step_index: int
    node_id: str
    node_type: str
    edge_id: Optional[str] = None
    anchors_hit: List[str] = Field(default_factory=list)
    cost_usd: float = 0.0
    timestamp: str = Field(default_factory=lambda: "")


class PerceptionKnowledgeChain(BaseModel):
    trace_id: UUID = Field(default_factory=uuid4)
    hops: List[PKCHop] = Field(default_factory=list)
    cumulative_cost_usd: float = 0.0

    def add_hop(self, hop: PKCHop) -> None:
        self.hops.append(hop)
        self.cumulative_cost_usd += hop.cost_usd
