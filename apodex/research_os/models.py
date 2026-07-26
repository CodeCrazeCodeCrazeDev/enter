from __future__ import annotations
import hashlib
import json
import time
from uuid import UUID, uuid4
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

# =====================================================================
# Base Immutable Artifact
# =====================================================================

class BaseArtifact(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    version: int = 1
    lineage_parent_uuids: List[UUID] = Field(default_factory=list)
    author: str = "unknown_agent"
    timestamp: float = Field(default_factory=time.time)
    confidence: float = 1.0
    validation_status: str = "PENDING"  # "PENDING" | "VALIDATED" | "FALSIFIED"
    digital_signature: str = ""

    # Advanced Institutional Metadata Fields
    uncertainty_meta: Dict[str, Any] = Field(
        default_factory=lambda: {"beta_alpha": 1.0, "beta_beta": 1.0, "epistemic_pct": 0.5, "lambda_decay": 0.05}
    )
    reproducibility_meta: Dict[str, Any] = Field(
        default_factory=lambda: {"seed": 42, "docker_hash": "sha256:88383", "dataset_hash": "sha256:99381"}
    )

    model_config = {"frozen": True}

    def compute_signature(self) -> str:
        """Deterministically serializes the artifact's state and returns a SHA-256 hash."""
        data_to_hash = {
            "uuid": str(self.uuid),
            "version": self.version,
            "lineage": [str(u) for u in self.lineage_parent_uuids],
            "author": self.author,
            "confidence": self.confidence,
            "validation_status": self.validation_status,
            "uncertainty": str(self.uncertainty_meta),
            "reproducibility": str(self.reproducibility_meta),
        }
        # Add all fields except excluded system ones
        for k, v in self.__dict__.items():
            if k not in ["uuid", "lineage_parent_uuids", "digital_signature"]:
                data_to_hash[k] = str(v)
        serialized = json.dumps(data_to_hash, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def with_signature(self) -> BaseArtifact:
        """Returns a copy of the artifact with its digital signature computed and attached."""
        sig = self.compute_signature()
        kwargs = self.dict() if hasattr(self, "dict") else self.model_dump()
        kwargs["digital_signature"] = sig
        return self.__class__(**kwargs)


# =====================================================================
# Research Artifact Subtypes
# =====================================================================

class ResearchProject(BaseArtifact):
    name: str
    funding_budget: float
    metrics_goals: Dict[str, Any] = Field(default_factory=dict)
    priority_score: float = 0.5  # Managed by Portfolio Scheduler
    expected_discovery_value: float = 1000.0


class ResearchProposal(BaseArtifact):
    project_uuid: UUID
    proposal_title: str
    proposal_abstract: str


class ResearchAgenda(BaseArtifact):
    prioritized_proposals: List[UUID] = Field(default_factory=list)


class ResearchQuestion(BaseArtifact):
    question_text: str
    domain: str


class LiteratureCorpus(BaseArtifact):
    query: str
    paper_titles: List[str] = Field(default_factory=list)
    abstracts: List[str] = Field(default_factory=list)


class KnowledgeGapAnalysis(BaseArtifact):
    corpus_uuid: UUID
    gaps: List[str] = Field(default_factory=list)


class Hypothesis(BaseArtifact):
    statement: str
    predicted_expectations: Dict[str, Any] = Field(default_factory=dict)


class ExperimentDesign(BaseArtifact):
    hypothesis_uuid: UUID
    parameters: Dict[str, Any] = Field(default_factory=dict)
    code_snippet: str
    execution_backend: str


class ExperimentResult(BaseArtifact):
    design_uuid: UUID
    success: bool
    metrics: Dict[str, Any] = Field(default_factory=dict)
    logs: List[str] = Field(default_factory=list)


class ReproducibilityReport(BaseArtifact):
    experiment_uuid: UUID
    reproducibility_rate: float
    reproduced: bool


class BenchmarkResult(BaseArtifact):
    experiment_uuid: UUID
    benchmark_name: str
    score: float


class DecisionRecord(BaseArtifact):
    target_uuid: UUID
    board_name: str
    decision_outcome: str  # "APPROVE" | "REJECT" | "REQUEST_REVISION" | "ESCALATE" | "SUSPEND" | "ARCHIVE" | "REQUIRE_INDEPENDENT_REVIEW"
    reason: str


class GovernanceDecision(BaseArtifact):
    decisions: List[DecisionRecord] = Field(default_factory=list)


class PeerReviewCritique(BaseArtifact):
    approved: bool
    comment: str


class Publication(BaseArtifact):
    title: str
    content: str
    citation_graph_uuid: UUID


class CitationGraph(BaseArtifact):
    citations: Dict[str, List[str]] = Field(default_factory=dict)


class ResearchRoadmap(BaseArtifact):
    milestones: List[str] = Field(default_factory=list)


class InstitutionalPolicy(BaseArtifact):
    policy_name: str
    rules: List[str] = Field(default_factory=list)


class ContradictionNode(BaseArtifact):
    conflict_node_a: UUID
    conflict_node_b: UUID
    explanation: str


# =====================================================================
# Knowledge Graph Nodes
# =====================================================================

class ConceptNode(BaseArtifact):
    concept_name: str
    definition: str


class TheoryNode(BaseArtifact):
    theory_name: str
    description: str
    linked_claims: List[UUID] = Field(default_factory=list)


class ClaimNode(BaseArtifact):
    assertion: str
    evidence_ids: List[UUID] = Field(default_factory=list)
    known_limitations: List[str] = Field(default_factory=list)


class EvidenceNode(BaseArtifact):
    source_url: str
    content: str
    provenance: str
