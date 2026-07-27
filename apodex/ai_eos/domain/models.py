"""Domain models, types, and schemas for the SERO v2.1 Operating System (Formal Spec v1.0).

This module houses the core aggregate roots and entities representing the state
of the system, ensuring strict boundaries and adhering to Domain-Driven Design.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class SubsystemMaturity(str, Enum):
    EXPERIMENTAL = "experimental"
    VALIDATED = "validated"
    PRODUCTION = "production"
    DEPRECATED = "deprecated"


class ExecutionStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class CognitiveStage(str, Enum):
    """The 7 Cognitive Stages of the SERO v2.1 architecture."""
    IMAGINE = "imagine"
    PLAN = "plan"
    EXPERIMENT = "experiment"
    LEARN = "learn"
    GENERALIZE = "generalize"
    TEACH = "teach"
    GOVERN = "govern"


class KnowledgeROI(BaseModel):
    """Structural metrics representing scientific research accountability."""
    cost_per_validated_theory: float = Field(0.0, ge=0.0)
    cost_per_uncertainty_reduction: float = Field(0.0, ge=0.0)
    cost_per_reusable_insight: float = Field(0.0, ge=0.0)
    cost_per_future_venture_unlocked: float = Field(0.0, ge=0.0)


class AuditProvenance(BaseModel):
    """Immutable audit tracking metadata for tracing decision origins."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(..., description="Entity or agent responsible for the action.")
    signature_sha256: str = Field(..., description="Cryptographic fingerprint of the inputs/state.")
    parent_provenance_id: Optional[UUID] = None


class DecisionProvenance(BaseModel):
    """An immutable record detailing the scientific backing behind a strategic decision."""
    decision_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    evidence: List[str] = Field(default_factory=list, description="Validated factual observations.")
    assumptions: List[str] = Field(default_factory=list, description="Strategic assumptions made.")
    models_consulted: List[str] = Field(default_factory=list, description="Model variants utilized.")
    experiments_consulted: List[UUID] = Field(default_factory=list, description="Experiment IDs backing this choice.")
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    uncertainty: float = Field(0.0, ge=0.0, le=1.0)
    approval_chain: List[str] = Field(default_factory=list, description="Actors signing off on the action.")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VentureCell(BaseModel):
    """A bounded venture cell representing an isolated business unit with independent financials."""
    cell_id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=2, max_length=128)
    namespace: str = Field(..., description="Isolated storage and memory partition.")
    sub_agent_ids: List[str] = Field(default_factory=list, description="Active agent composition.")

    # Financial state (P&L)
    allocated_capital_cents: int = Field(0, ge=0)
    spent_capital_cents: int = Field(0, ge=0)
    earned_revenue_cents: int = Field(0, ge=0)

    # Active Inference and Belief state tracking
    belief_state: Dict[str, Any] = Field(default_factory=dict, description="Probability distribution over market dimensions.")
    uncertainty: float = Field(0.5, ge=0.0, le=1.0, description="Entropy score of current belief state.")
    expected_free_energy: float = Field(0.0, description="Objective function score of the current policy.")
    information_gain: float = Field(0.0, description="Predicted reduction in belief entropy.")
    prediction_error: float = Field(0.0, description="Difference between model forecast and measurement.")
    confidence: float = Field(0.5, ge=0.0, le=1.0, description="Confidence score on current policy trajectory.")
    risk: float = Field(0.0, ge=0.0, description="Computed quantitative risk factor.")
    capital_allocation_score: float = Field(0.0, description="Priority score for capital reallocation.")

    # Cognitive Tracking
    current_cognitive_stage: CognitiveStage = Field(default=CognitiveStage.IMAGINE)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def net_profit_cents(self) -> int:
        return self.earned_revenue_cents - self.spent_capital_cents


class Hypothesis(BaseModel):
    """A registered scientific business hypothesis under statistical evaluation."""
    hypothesis_id: UUID = Field(default_factory=uuid4)

    # Formal Spec v1.0 Fields
    statement: str = Field(default="", description="The target hypothesis statement.")
    domain: str = Field(default="general", description="Scientific or business domain classification.")
    venture_id: Optional[str] = Field(None, description="Null if venture-agnostic / cross-cutting.")

    prior_confidence: float = Field(0.50, ge=0.0, le=1.0)
    posterior_confidence: float = Field(0.50, ge=0.0, le=1.0)
    confidence_distribution: Dict[str, Any] = Field(
        default_factory=lambda: {"type": "beta", "params": {"alpha": 10.0, "beta": 10.0}},
        description="Probability distribution over success ratio."
    )

    supporting_evidence: List[str] = Field(default_factory=list, description="List of supporting Evidence IDs.")
    contradicting_evidence: List[str] = Field(default_factory=list, description="List of contradicting Evidence IDs.")
    dependent_hypotheses: List[str] = Field(default_factory=list, description="Hypotheses assumed true.")
    downstream_decisions: List[str] = Field(default_factory=list, description="Decisions relying on this claim.")

    # Derived flags for Epistemic Risk queries
    assumption_count: int = Field(0, description="Count of unproven dependent hypotheses.")
    single_source_flag: bool = Field(False, description="True if evidence count == 1.")
    high_impact_low_evidence_flag: bool = Field(False, description="True if high impact and low evidence count.")

    status: str = Field("proposed", description="Status (proposed, under_test, active, falsified, superseded, theory_promoted).")

    # Backward compatibility fields
    title: Optional[str] = None
    description: Optional[str] = None
    null_hypothesis: Optional[str] = None
    target_metric: Optional[str] = None
    significance_level_alpha: float = Field(0.05, ge=0.001, le=0.2)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    def model_post_init(self, __context: Any) -> None:
        """Autofill new fields from old ones if needed."""
        if not self.statement and self.description:
            self.statement = self.description
        if not self.title and self.statement:
            self.title = self.statement[:50]
        self.assumption_count = len(self.dependent_hypotheses)
        evidence_count = len(self.supporting_evidence) + len(self.contradicting_evidence)
        self.single_source_flag = (evidence_count == 1)
        self.high_impact_low_evidence_flag = (len(self.downstream_decisions) >= 3 and evidence_count <= 1)


class Evidence(BaseModel):
    """A factual measurement node in KOS graph."""
    evidence_id: str = Field(..., description="Unique Evidence ID identifier.")
    source: str = Field(..., description="Origin of measurement, e.g. paid pilot, simulation.")
    source_type: str = Field(default="experiment", description="experiment | observation | literature | simulation.")
    method: str = Field(default="experiment", description="Method (backward compatibility): experiment, observation, literature, simulation.")
    evidence_quality_tier: str = Field(default="survey", description="rct | natural_experiment | longitudinal | survey | interview | opinion | synthetic.")
    reliability_weight: float = Field(0.50, ge=0.0, le=1.0)

    strength: Dict[str, Any] = Field(default_factory=dict, description="Contains effect_size, sample_size, p_value, interval.")
    causal_or_correlational: str = Field("correlational", description="causal or correlational classification.")
    linked_hypotheses: List[str] = Field(default_factory=list, description="Linked Hypothesis IDs.")

    replicated_by: List[str] = Field(default_factory=list, description="List of replica Evidence IDs.")
    replication_status: str = Field(default="unreplicated", description="unreplicated | replicated | failed_replication.")

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    decay_rate: float = Field(0.02, ge=0.0)
    current_relevance: float = Field(1.0, ge=0.0, le=1.0)

    def model_post_init(self, __context: Any) -> None:
        """Autofill new fields from old ones if needed."""
        if self.method and self.source_type == "experiment":
            self.source_type = self.method


class Theory(BaseModel):
    """A promoted general explanatory model built from validated hypotheses."""
    theory_id: str = Field(..., description="Unique Theory ID identifier.")
    statement: str = Field(..., description="General explanatory model statement.")
    constituent_hypotheses: List[str] = Field(default_factory=list, description="Validated Hypothesis IDs backing this theory.")
    predictive_scope: List[str] = Field(default_factory=list, description="Untested predictions queued for validation.")
    confidence: float = Field(0.50, ge=0.0, le=1.0)

    # Formal Spec v1.0 predictive track record and promotion criteria
    predictive_track_record: Dict[str, Any] = Field(
        default_factory=lambda: {
            "predictions_made": 0,
            "predictions_confirmed": 0,
            "predictions_falsified": 0,
            "accuracy_rate": 1.0
        }
    )
    promotion_criteria_met: Dict[str, Any] = Field(
        default_factory=lambda: {
            "independent_evidence_count": 0,
            "generalization_tested": False,
            "predictive_success_threshold_met": False
        }
    )

    contradictions: List[str] = Field(default_factory=list, description="List of raised Contradiction IDs.")
    status: str = Field("draft", description="Status (draft, active, contradicted, retired).")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Contradiction(BaseModel):
    """An identified inconsistency between hypothesis beliefs."""
    contradiction_id: str = Field(..., description="Unique Contradiction ID identifier.")
    node_a: str = Field(..., description="First inconsistent Hypothesis ID.")
    node_b: str = Field(..., description="Second inconsistent Hypothesis ID.")
    detected_by: str = Field(..., description="Agent or module that identified the mismatch.")
    severity: str = Field(default="low", description="low | medium | high.")
    resolution_status: str = Field(default="pending", description="Status of resolution: pending, resolved.")
    resolution_action: Optional[str] = None
    routed_to: str = Field(default="chairman_agent", description="chairman_agent | human_governance.")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Relationship(BaseModel):
    """Typed relationship edges connecting epistemic nodes."""
    relationship_id: str = Field(default_factory=lambda: f"rel_{uuid4().hex[:12]}")
    from_node: str = Field(..., description="Source node ID.")
    to_node: str = Field(..., description="Target node ID.")
    type: str = Field(..., description="supports | contradicts | causes | correlates | derived_from | generalizes | specializes.")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DecisionRecord(BaseModel):
    """Institutional memory record representing strategic choices made."""
    decision_id: str = Field(..., description="Unique Decision ID identifier.")
    decision: str = Field(..., description="Decision summary statement.")
    supporting_hypotheses: List[str] = Field(default_factory=list, description="Supporting Hypothesis IDs.")
    confidence_at_decision: float = Field(0.50, ge=0.0, le=1.0)
    rejected_alternatives: List[str] = Field(default_factory=list, description="Rejected alternative statements.")
    rationale: str = Field(..., description="Textual rationale backing the choice.")
    made_by: str = Field(default="agent", description="agent | human.")
    outcome: Dict[str, Any] = Field(
        default_factory=lambda: {
            "realized": False,
            "actual_result": None,
            "confidence_in_hindsight": None
        }
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Experiment(BaseModel):
    """An execution instance of a scientific experiment in an isolated Sandbox."""
    experiment_id: UUID = Field(default_factory=uuid4)
    hypothesis_tested: Optional[str] = Field(None, description="Hypothesis tested ID reference.")
    design: Dict[str, Any] = Field(
        default_factory=lambda: {
            "method": "simulation",
            "sample_size_planned": 100,
            "power": 0.80,
            "pre_registered": True
        }
    )
    status: str = Field(default="designed", description="designed | running | complete | aborted.")
    result_evidence: Optional[str] = Field(None, description="Resulting Evidence ID pointer.")

    # Backward compatibility fields
    hypothesis_id: UUID = Field(default_factory=uuid4)
    dataset_id: Optional[UUID] = None
    seed: int = Field(default=42)
    reproducibility_hash: str = Field(default="", description="Hash representation of sandbox state and seed.")
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    # Statistical validation outputs
    p_value: Optional[float] = None
    effect_size: Optional[float] = None
    deflated_sharpe_ratio: Optional[float] = None
    is_statistically_significant: bool = Field(default=False)

    metadata: Dict[str, Any] = Field(default_factory=dict)


class Capability(BaseModel):
    """A version-controlled, verified, and audited operational behavior or system tool."""
    capability_id: str = Field(..., description="UUID or structured string identifier.")
    name: str = Field(..., min_length=2, max_length=128)
    description: str = Field(..., description="Functional behavior description.")
    source: str = Field(..., description="Source code file path or model endpoint.")
    origin: str = Field(..., description="Origin of the capability, e.g. 'internal', 'arXiv:2502.20422', 'GitHub:some-repo'.")
    evidence: List[str] = Field(default_factory=list, description="Pointers to validated Sandbox experiments or papers.")
    benchmark_results: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics scored on evaluation.")
    risk_score: float = Field(0.0, ge=0.0, le=1.0)
    dependencies: List[str] = Field(default_factory=list, description="IDs of other required capabilities.")
    owner: str = Field(..., description="Subsystem or division owning this capability.")
    maturity: SubsystemMaturity = Field(default=SubsystemMaturity.EXPERIMENTAL)
    deployment_status: str = Field(default="staged", description="Status, e.g. staged, shadow, production, retired.")
    rollback_trigger: str = Field(..., description="Metric threshold or exception pattern triggering auto-rollback.")
    retirement_policy: str = Field(..., description="Condition for automatic deprecation.")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
