"""Event taxonomy and Event Bus contracts for the AI-EOS operating system.

Every major state transition in the OS publishes an event inheriting from `DomainEvent`.
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    """Base schema for all domain events in AI-EOS."""
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    schema_version: str = Field(default="1.0")


class VentureCellCreatedEvent(DomainEvent):
    """Fired when a new venture cell is initialized with independent capital."""
    cell_id: UUID
    name: str
    namespace: str
    allocated_capital_cents: int


class HypothesisRegisteredEvent(DomainEvent):
    """Fired when a new scientific hypothesis is recorded in the Research OS."""
    hypothesis_id: UUID
    title: str
    target_metric: str


class ExperimentExecutedEvent(DomainEvent):
    """Fired when a Sandbox experiment completes, yielding statistical results."""
    experiment_id: UUID
    hypothesis_id: UUID
    p_value: float
    reproducibility_hash: str
    is_statistically_significant: bool


class FactValidatedEvent(DomainEvent):
    """Fired when a hypothesis passes statistical validation and is promoted."""
    atom_id: UUID
    content: str
    confidence: float
    source_experiment_id: UUID


class CapabilityDiscoveredEvent(DomainEvent):
    """Fired when Frontier Capability Intelligence discovers a new candidate capability."""
    candidate_id: str
    name: str
    source: str
    origin: str


class CapabilityPromotedEvent(DomainEvent):
    """Fired when a capability successfully transitions to production rollout."""
    capability_id: str
    name: str
    maturity: str
    owner: str


class SLAExceptionDetectedEvent(DomainEvent):
    """Fired when an anomaly, budget violation, or safety breach is detected."""
    exception_id: UUID = Field(default_factory=uuid4)
    exception_type: str
    severity: str
    details: str
    related_cell_id: Optional[UUID] = None


class CapabilityRolledBackEvent(DomainEvent):
    """Fired when an auto-rollback is triggered, reverting system configuration."""
    capability_id: str
    reason: str
    rollback_sha256: str
