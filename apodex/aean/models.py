"""Shared domain models for the AEAN (Autonomous Economic Actor Network).

All monetary values are represented in integer cents to avoid floating point
drift, matching the convention used elsewhere in the ``apodex`` codebase.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.utcnow()


class MicroCellStatus(str, Enum):
    """Lifecycle state of an autonomous micro-cell."""

    PROPOSED = "proposed"
    ACTIVE = "active"
    SCALED = "scaled"
    KILLED = "killed"


class EngineName(str, Enum):
    """The six engines that make up the AEAN organism (4 economic + 2 coordination)."""

    PAEAN = "PAEAN"
    ADE = "ADE"
    ARE = "ARE"
    AVIE = "AVIE"
    HIVE_MIND = "HiveMind"
    RESEARCH = "Research"


class DemandSignal(BaseModel):
    """A detected demand opportunity emitted by ADE and consumed by PAEAN."""

    signal_id: str = Field(default_factory=_uuid)
    market: str
    segment: str
    strength: float = Field(ge=0.0, le=1.0)
    estimated_tam_cents: int = Field(ge=0)
    elasticity: float = Field(default=-1.5, description="Price elasticity of demand (negative).")
    keywords: List[str] = Field(default_factory=list)
    detected_at: datetime = Field(default_factory=_now)


class Narrative(BaseModel):
    """A narrative/perception strategy produced by ADE for a demand signal."""

    narrative_id: str = Field(default_factory=_uuid)
    signal_id: str
    theme: str
    hook: str
    body: str
    predicted_resonance: float = Field(ge=0.0, le=1.0)
    generated_by: str = "simulation"
    core_narrative: str = ""
    key_messages: List[str] = Field(default_factory=list)
    differentiation_angle: str = ""


class VisualAsset(BaseModel):
    """A campaign-ready creative asset produced by AVIE."""

    asset_id: str = Field(default_factory=_uuid)
    narrative_id: str
    concept: str
    format: str = "social_square"
    predicted_ctr: float = Field(ge=0.0, le=1.0)
    prompt: str = ""
    generated_by: str = "simulation"


class MicroCell(BaseModel):
    """An autonomous economic unit spawned by PAEAN with bounded capital."""

    cell_id: str = Field(default_factory=_uuid)
    signal_id: str
    market: str
    segment: str
    status: MicroCellStatus = MicroCellStatus.PROPOSED
    allocated_cents: int = Field(default=0, ge=0)
    deployed_cents: int = Field(default=0, ge=0)
    revenue_cents: int = Field(default=0, ge=0)
    cycles_run: int = 0
    scale_count: int = 0
    kill_threshold_roi: float = -0.25
    scale_threshold_roi: float = 0.30
    created_at: datetime = Field(default_factory=_now)

    @property
    def roi(self) -> float:
        """Return on deployed capital for this cell."""
        if self.deployed_cents <= 0:
            return 0.0
        return (self.revenue_cents - self.deployed_cents) / self.deployed_cents


class CycleResult(BaseModel):
    """Summary of a single compounding-flywheel iteration."""

    cycle: int
    timestamp: datetime = Field(default_factory=_now)
    signals_detected: int = 0
    narratives_created: int = 0
    assets_produced: int = 0
    assets_validated: int = 0
    active_cells: int = 0
    capital_deployed_cents: int = 0
    revenue_cents: int = 0
    treasury_cents: int = 0
    portfolio_roi: float = 0.0
    cells_killed: int = 0
    cells_scaled: int = 0
    governance_blocks: int = 0
    notes: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Reality-Grounded Adaptive Engine (RGAE) — perception + three-layer validation
# ---------------------------------------------------------------------------
class ValidationStage(str, Enum):
    """Screening stage reached by a creative asset in the RGAE pipeline."""

    SIMULATION = "simulation"        # Layer 1: TRIBE neural-response simulation.
    REALITY_TEST = "reality_test"    # Layer 2: controlled micro-budget live test.
    REVENUE_GATE = "revenue_gate"    # Layer 3: profitability / unit-economics gate.
    PASSED = "passed"                # Cleared all three layers.
    REJECTED = "rejected"            # Terminated at some layer.


class PerceptionScore(BaseModel):
    """TRIBEv2 four-dimensional perception prediction for a creative asset.

    Each dimension is normalised to ``[0, 1]``. The engine deliberately keeps
    ``attention`` and ``engagement`` distinct from the downstream economic
    signal so the calibration layer can discount attention-only "decoys".
    """

    attention: float = Field(ge=0.0, le=1.0)          # Will they look?
    valence: float = Field(ge=0.0, le=1.0)            # Emotional positivity.
    arousal: float = Field(ge=0.0, le=1.0)            # Emotional intensity.
    cognitive_load: float = Field(ge=0.0, le=1.0)     # Will they understand?
    engagement_likelihood: float = Field(ge=0.0, le=1.0)  # Will they act?


class ValidationRecord(BaseModel):
    """Outcome of running a creative asset through the RGAE pipeline."""

    asset_id: str
    narrative_id: str
    segment: str = ""
    stage_reached: ValidationStage = ValidationStage.SIMULATION
    passed: bool = False
    perception: Optional[PerceptionScore] = None
    calibrated_value: float = 0.0
    predicted_ctr: float = 0.0
    observed_ctr: float = 0.0
    ltv_cpa_ratio: float = 0.0
    notes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_now)


# ---------------------------------------------------------------------------
# Three-Critic Stack — Truth / Policy / Strategy review of every action
# ---------------------------------------------------------------------------
class CriticName(str, Enum):
    TRUTH = "truth"        # Factual correctness / grounded projections.
    POLICY = "policy"      # Constraint & constitutional alignment.
    STRATEGY = "strategy"  # Objective optimality of the action.


class CriticReview(BaseModel):
    critic: CriticName
    passed: bool
    score: float = Field(ge=0.0, le=1.0)
    rationale: str = ""


class CriticVerdict(BaseModel):
    """Aggregated verdict of the Three-Critic Stack for a single action."""

    action: str
    approved: bool
    reviews: List[CriticReview] = Field(default_factory=list)
    latency_ms: float = 0.0

    @property
    def score(self) -> float:
        if not self.reviews:
            return 0.0
        return sum(r.score for r in self.reviews) / len(self.reviews)


# ---------------------------------------------------------------------------
# Epistemic firewall — reality validation of inbound demand signals
# ---------------------------------------------------------------------------
class SignalValidation(BaseModel):
    """Three-layer reality-validation verdict for a demand signal.

    Oracle verification checks the signal against known priors, cross-source
    consensus requires corroboration across independent sources, and the
    adversarial red-team probes for manipulation. ``credibility`` combines all
    three with a temporal-decay factor.
    """

    signal_id: str
    passed: bool = False
    credibility: float = Field(default=0.0, ge=0.0, le=1.0)
    oracle_ok: bool = False
    consensus_ok: bool = False
    red_team_ok: bool = False
    corroborating_sources: int = 0
    notes: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Pre-Trade Validation Engine — "should we even try this?" before capital
# ---------------------------------------------------------------------------
class EvidencePillar(BaseModel):
    """One of the four evidence pillars screened before capital deployment."""

    name: str
    score: float = Field(ge=0.0, le=1.0)
    passed: bool = False
    detail: str = ""


class PreTradeAssessment(BaseModel):
    """Verdict of the Simulation & Pre-Trade Validation Engine for a signal.

    A hypothesis is authorised only if (a) all four evidence pillars clear their
    thresholds (the gate), (b) the Monte-Carlo synthetic test is favourable, and
    (c) the counterfactual probes do not expose fatal fragility.
    """

    signal_id: str
    market: str = ""
    segment: str = ""
    gate_passed: bool = False
    sim_passed: bool = False
    counterfactual_passed: bool = False
    passed: bool = False
    pillars: List[EvidencePillar] = Field(default_factory=list)
    sim_p05: float = 0.0
    sim_mean: float = 0.0
    sim_cv: float = 0.0
    fragility_index: float = 0.0
    discriminatory: bool = True
    notes: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Governed Cognitive Evolution System — three-layer governed self-improvement
# ---------------------------------------------------------------------------
class EvolutionLayer(str, Enum):
    """The three layers of the Governed Cognitive Evolution System."""

    CAPABILITY = "capability"      # Layer 1: behavioural (prompts/strategies).
    ARCHITECTURE = "architecture"  # Layer 2: structural (topology/graph).
    OBJECTIVE = "objective"        # Layer 3: teleological (never evolves).


class StrategyGenome(BaseModel):
    """A Layer-1 behavioural strategy candidate (the *contents* of cognition).

    These parameters tune behaviour *within* the fixed architecture; they can
    never alter risk controls or capital limits (those live in Layer 3).
    """

    allocation_pct: float = Field(default=0.15, ge=0.0, le=1.0)
    exploration: float = Field(default=0.5, ge=0.0, le=1.0)
    diversification: float = Field(default=0.5, ge=0.0, le=1.0)
    patience: float = Field(default=0.5, ge=0.0, le=1.0)


class CapabilityEvolutionResult(BaseModel):
    """Outcome of a Layer-1 variation→measurement→selection round."""

    generations: int = 0
    incumbent_fitness: float = 0.0
    champion_fitness: float = 0.0
    improvement: float = 0.0
    promoted: bool = False
    rejected_by_objective: int = 0
    notes: List[str] = Field(default_factory=list)


class PipelineStage(str, Enum):
    """Sequential stages of the Layer-2 architecture-evolution pipeline."""

    SANDBOX = "sandbox"
    BENCHMARK = "benchmark"
    STRESS = "stress"
    SECURITY = "security"
    ECONOMIC = "economic"
    CANARY = "canary"
    SCALE = "scale"


class StageResult(BaseModel):
    stage: PipelineStage
    passed: bool
    detail: str = ""


class ArchitectureEvolutionResult(BaseModel):
    """Outcome of pushing a structural candidate through the seven-stage gate."""

    candidate: str
    stage_reached: PipelineStage = PipelineStage.SANDBOX
    promoted: bool = False
    rejected_by_objective: bool = False
    stages: List[StageResult] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class OrganismState(BaseModel):
    """Point-in-time snapshot of the whole organism, used by the dashboard."""

    cycle: int = 0
    treasury_cents: int = 0
    initial_capital_cents: int = 0
    total_revenue_cents: int = 0
    total_deployed_cents: int = 0
    active_cells: int = 0
    killed_cells: int = 0
    scaled_cells: int = 0
    cumulative_roi: float = 0.0
    history: List[CycleResult] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=_now)


# ===========================================================================
# AI-EOS Section 6 Inter-Engine API Contracts & Models
# ===========================================================================

class Opportunity(BaseModel):
    """ADE L1 Opportunity model for inter-engine API contracts."""
    id: str = Field(default_factory=_uuid)
    description: str
    market_size: int = Field(default=0, ge=0, description="Estimated market size in cents.")
    competition: str = "low"  # low|med|high
    probability: float = Field(default=0.0, ge=0.0, le=1.0)
    supporting_signals: List[str] = Field(default_factory=list)

    @property
    def signal_id(self) -> str:
        return self.id

    @property
    def market(self) -> str:
        return self.description.split(":")[0] if ":" in self.description else "devtools"

    @property
    def segment(self) -> str:
        return self.description.split(":")[1] if ":" in self.description else "startups"

    @property
    def strength(self) -> float:
        return self.probability

    @property
    def estimated_tam_cents(self) -> int:
        return self.market_size


class CustomerGraphEntry(BaseModel):
    """Customer Intelligence profile of problem/desire/objection/buying trigger/channel."""
    customer_id: str = Field(default_factory=_uuid)
    problem: str
    desire: str
    objection: str
    buying_trigger: str
    preferred_channel: str
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class GenerationBrief(BaseModel):
    """Visual Psychology Engine output for asset generation."""
    required_features: List[str] = Field(default_factory=list)
    avoid_features: List[str] = Field(default_factory=list)
    target_emotion: str = ""
    target_segment: str = ""
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class Visual(BaseModel):
    """Visual asset contract with output outcome optimization features."""
    visual_id: str = Field(default_factory=_uuid)
    narrative_id: str
    features: Dict[str, Any] = Field(default_factory=dict)
    channel_variants: List[str] = Field(default_factory=list)

    @property
    def asset_id(self) -> str:
        return self.visual_id

    @property
    def concept(self) -> str:
        return self.features.get("concept", "bold_typographic")

    @property
    def format(self) -> str:
        return self.features.get("format", "social_square")

    @property
    def predicted_ctr(self) -> float:
        return self.features.get("predicted_ctr", 0.05)

    @property
    def prompt(self) -> str:
        return self.features.get("prompt", "")

    @property
    def generated_by(self) -> str:
        return self.features.get("generated_by", "simulation")


class Offer(BaseModel):
    """ARE Offer details for a customer segment."""
    offer_statement: str
    bundle_options: List[str] = Field(default_factory=list)
    price_floor: int = Field(ge=0, description="In cents")
    price_ceiling: int = Field(ge=0, description="In cents")
    guarantee: str = ""


class LeadScore(BaseModel):
    intent: float = Field(default=0.5, ge=0.0, le=1.0)
    need: float = Field(default=0.5, ge=0.0, le=1.0)
    budget: float = Field(default=0.5, ge=0.0, le=1.0)
    timing: float = Field(default=0.5, ge=0.0, le=1.0)
    fit: float = Field(default=0.5, ge=0.0, le=1.0)

    @property
    def total_score(self) -> float:
        return round((self.intent + self.need + self.budget + self.timing + self.fit) / 5.0, 4)


class Lead(BaseModel):
    """Lead tracking for the Autonomous Sales Engine."""
    lead_id: str = Field(default_factory=_uuid)
    lead_score: LeadScore
    customer_id: str
    narrative_id: str
    visual_id: str


class WinningPattern(BaseModel):
    """A pattern written back into the shared Revenue Memory Graph."""
    pattern_type: str
    segment: str
    channel: str
    feature_set: Dict[str, Any] = Field(default_factory=dict)
    outcome_metric: float
    sample_size: int = 0
    confidence: float = Field(ge=0.0, le=1.0)


# ===========================================================================
# KOS/ROS Spec — Addendum v1.1: Production Patterns
# ===========================================================================

class Event(BaseModel):
    id: str = Field(default_factory=_uuid)
    type: str  # e.g., "EvidenceCreated" | "HypothesisUpdated" | "TheoryPromoted" | ...
    payload: Dict[str, Any] = Field(default_factory=dict)
    caused_by: Optional[str] = None
    timestamp: datetime = Field(default_factory=_now)


class Evidence(BaseModel):
    id: str = Field(default_factory=_uuid)
    statement: str
    evidence_quality_tier: str  # "RCT" | "COHORT" | "ANECDOTAL"
    reliability_weight: float = Field(ge=0.0, le=1.0)
    effect_size: Optional[float] = None
    interval: Optional[str] = None
    version: int = 1
    current: bool = True
    timestamp: datetime = Field(default_factory=_now)


class Hypothesis(BaseModel):
    id: str = Field(default_factory=_uuid)
    statement: str
    confidence: float = Field(ge=0.0, le=1.0)
    version: int = 1
    current: bool = True
    timestamp: datetime = Field(default_factory=_now)


class Theory(BaseModel):
    id: str = Field(default_factory=_uuid)
    statement: str
    predictive_success_rate: float = Field(ge=0.0, le=1.0)
    version: int = 1
    current: bool = True
    timestamp: datetime = Field(default_factory=_now)


class DecisionProposal(BaseModel):
    id: str = Field(default_factory=_uuid)
    decision: str
    supporting_hypotheses: List[str] = Field(default_factory=list)  # Pinned to specific Hypothesis version ids
    proposed_by: str  # AgentRef
    status: str = "proposed"  # "proposed" | "simulating" | "approved" | "rejected" | "executed" | "cancelled"
    simulation_result: Optional[Dict[str, Any]] = None
    approval: Dict[str, Any] = Field(default_factory=lambda: {
        "required": False,
        "approved_by": None,
        "approved_at": None
    })
    execution_result: Optional[Dict[str, Any]] = None
    decision_record: Optional[str] = None


class AgentScope(BaseModel):
    agent_id: str
    can_call: List[str] = Field(default_factory=list)
    can_approve: List[str] = Field(default_factory=list)
