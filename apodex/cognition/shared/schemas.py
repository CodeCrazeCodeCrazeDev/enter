from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class StrategicGoal(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    description: str
    priority_score: float = Field(..., description="Value between 0.0 (low) and 1.0 (critical)")
    budget_cents: int
    constraints: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Hypothesis(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    goal_id: uuid.UUID
    statement: str
    rationale: str
    confidence: float = Field(0.5, description="Bayesian confidence score between 0.0 and 1.0")
    evidence_ids: List[uuid.UUID] = Field(default_factory=list)

    # Research Opportunity Metrics (arXiv:2605.15245 Portfolio Management)
    expected_scientific_value: float = Field(0.5, description="Scale of 0.0 to 1.0")
    expected_engineering_impact: float = Field(0.5, description="Scale of 0.0 to 1.0")
    expected_business_value: float = Field(0.5, description="Scale of 0.0 to 1.0")
    cost_of_investigation_cents: int = Field(50_000, description="Cost in cents")
    probability_of_success: float = Field(0.5, description="Bayesian estimate 0.0 to 1.0")
    information_gain: float = Field(0.5, description="Entropy reduction / expected info gain 0.0 to 1.0")
    priority_score: float = Field(0.5, description="Computed portfolio priority rank")


class EvidenceCard(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    source: str
    description: str
    reliability: float = Field(0.5, description="Source reliability score (0.0 to 1.0)")
    contradicts_hypothesis_ids: List[uuid.UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RiskAssessment(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    risk_factor: float = Field(..., description="Risk score from 0.0 to 1.0")
    mitigations: List[str] = Field(default_factory=list)
    description: str


class FeasibilityReport(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    is_feasible: bool
    confidence: float
    estimated_development_cost_cents: int
    risks: RiskAssessment
    architecture_score: float = Field(1.0, description="Structural quality rating")
    dependencies: List[str] = Field(default_factory=list)


class ValueReport(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    expected_return_cents: int
    roi_multiple: float
    market_size_cents: int
    competitor_strength: float = Field(0.5, description="0.0 to 1.0 scale")
    customer_interest_score: float = Field(0.5, description="0.0 to 1.0 scale")


class ExecutionStep(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    sequence: int
    action_name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    assigned_role: str


class ExecutionPlan(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    goal_id: uuid.UUID
    steps: List[ExecutionStep] = Field(default_factory=list)
    estimated_duration_sec: float
    total_cost_projection_cents: int


class ExecutionOutcome(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    success: bool
    actual_cost_cents: int
    actual_duration_sec: float
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)
    error_logs: List[str] = Field(default_factory=list)


class Lesson(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    category: str  # "workflow", "planner", "research_source", "engineering_pattern", "execution_strategy"
    summary: str
    context: str
    impact_delta: float = Field(0.0, description="Change in performance metric if applied")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DecisionProvenance(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    objective: StrategicGoal
    hypotheses: List[Hypothesis] = Field(default_factory=list)
    evidence: List[EvidenceCard] = Field(default_factory=list)
    feasibility: Optional[FeasibilityReport] = None
    value_assessment: Optional[ValueReport] = None
    execution_plan: Optional[ExecutionPlan] = None
    assumptions: List[str] = Field(default_factory=list)
    confidence: float
    uncertainty: float
    alternatives_considered: List[str] = Field(default_factory=list)
    final_decision: str  # e.g. "APPROVED", "REJECTED_GOVERNANCE", "HALTED_FEASIBILITY"
    predicted_expectations: Dict[str, Any] = Field(default_factory=dict, description="Simulated expectations prior to execution")
    execution_outcome: Optional[ExecutionOutcome] = None
    discrepancy_analysis: Dict[str, Any] = Field(default_factory=dict, description="Outcome actuals compared against predicted expectations")
    lessons_learned: List[Lesson] = Field(default_factory=list)


class Recommendation(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    action_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float


class VerificationResult(BaseModel):
    is_valid: bool
    reason: str
    rejection_tags: List[str] = Field(default_factory=list)


class HealthStatus(BaseModel):
    status: str  # "OK", "DEGRADED", "FAILED"
    cache_hits: int = 0
    cache_misses: int = 0
    latency_p95_ms: float = 0.0
    errors_count: int = 0


# Shared contextual envelope passed between layers
class CognitiveContext(BaseModel):
    active_goal: Optional[StrategicGoal] = None
    hypotheses: List[Hypothesis] = Field(default_factory=list)
    evidence: List[EvidenceCard] = Field(default_factory=list)
    feasibility: Optional[FeasibilityReport] = None
    value: Optional[ValueReport] = None
    execution_plan: Optional[ExecutionPlan] = None
    execution_outcome: Optional[ExecutionOutcome] = None
    lessons: List[Lesson] = Field(default_factory=list)
    provenance_log: List[DecisionProvenance] = Field(default_factory=list)
    system_metrics: Dict[str, Any] = Field(default_factory=dict)
