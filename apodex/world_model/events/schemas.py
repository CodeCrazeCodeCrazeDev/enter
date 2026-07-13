from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class WmcDomainEvent(BaseModel):
    """Base schema for all events published by the WMC."""
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"


class RealityStateUpdatedEvent(WmcDomainEvent):
    """Published when the ground-truth model of the real world is updated with fresh observations."""
    update_id: UUID
    affected_entity_ids: List[UUID] = Field(default_factory=list)
    new_relationships_asserted: List[UUID] = Field(default_factory=list)


class AnomalousTrendDetectedEvent(WmcDomainEvent):
    """Published when an ingestion pattern exceeds statistical variance thresholds."""
    trend_id: UUID
    description: str
    signal_strength: float
    affected_sectors: List[str] = Field(default_factory=list)


class TimelineBranchedEvent(WmcDomainEvent):
    """Published when a branched simulation environment is successfully initialized."""
    new_timeline_id: UUID
    parent_timeline_id: UUID
    branch_name: str


class SimulationStepCompletedEvent(WmcDomainEvent):
    """Published when a timeline advances, signaling downstream engines to evaluate consequences."""
    timeline_id: UUID
    current_logical_time: datetime
    applied_deltas_count: int


class CausalInconsistencyDetectedEvent(WmcDomainEvent):
    """Published when causal validation fails, triggering automated rollback or adjustments."""
    timeline_id: UUID
    offending_node_ids: List[UUID] = Field(default_factory=list)
    inconsistency_score: float
    error_details: str


class CohortBeliefShiftedEvent(WmcDomainEvent):
    """Published when simulation results show a shift in a target segment's beliefs or values."""
    cohort_id: str
    affected_beliefs: Dict[str, float] = Field(default_factory=dict)
    catalyst_event_id: UUID


class AttentionFatigueAlert(WmcDomainEvent):
    """Published when an audience's response to specific content drops below performance thresholds."""
    cohort_id: str
    theme_or_creative_id: UUID
    fatigue_coefficient: float


class CreativeCandidateEvaluatedEvent(WmcDomainEvent):
    """Published when a creative concept has completed simulation testing and is ready for rendering."""
    candidate_id: UUID
    estimated_engagement: float
    estimated_conversion: float
    risk_score: float
    score_metadata: Dict[str, float] = Field(default_factory=dict)


class MediaGenerationPlannedEvent(WmcDomainEvent):
    """Published when a multi-modal generation and model-routing path is compiled."""
    plan_id: UUID
    creative_concept_id: UUID
    required_models: List[str] = Field(default_factory=list)
    estimated_tokens_or_dollars: float


class AssetRenderCompletedEvent(WmcDomainEvent):
    """Published when rendering finishes and media assets are safely stored."""
    asset_id: UUID
    plan_id: UUID
    media_url: str
    checksum_sha256: str
    generation_metadata: Dict[str, Any] = Field(default_factory=dict)


class PolicyViolationDetectedEvent(WmcDomainEvent):
    """Published when a simulation path or generation proposal violates safety or brand policies."""
    violation_id: UUID = Field(default_factory=uuid4)
    violating_agent_id: str
    policy_id: str
    severity_level: str
    evidence_context: Dict[str, Any] = Field(default_factory=dict)
