from __future__ import annotations
import collections
import time
from typing import Any, Callable, Dict, List, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

# =====================================================================
# Events
# =====================================================================

class BaseEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: float = Field(default_factory=time.time)


class WorkflowStarted(BaseEvent):
    workflow_id: str
    domain: str
    project_uuid: UUID


class ArtifactCreated(BaseEvent):
    artifact_uuid: UUID
    artifact_type: str
    author: str
    confidence: float
    parent_uuids: List[UUID]


class ExperimentCompleted(BaseEvent):
    experiment_uuid: UUID
    design_uuid: UUID
    backend: str
    success: bool
    metrics: Dict[str, Any] = Field(default_factory=dict)
    cost: float = 0.0


class ReviewFailed(BaseEvent):
    review_uuid: UUID
    artifact_uuid: UUID
    critique_summary: str


class GovernanceRejected(BaseEvent):
    governance_uuid: UUID
    board_name: str
    target_uuid: UUID
    reason: str


class PublicationAccepted(BaseEvent):
    publication_uuid: UUID
    citation_graph_uuid: UUID
    project_uuid: UUID
    timestamp_started: float


class HypothesisFalsified(BaseEvent):
    hypothesis_uuid: UUID
    reason: str


# =====================================================================
# Event Bus (Publisher-Subscriber)
# =====================================================================

class EventBus:
    """Thread-safe, synchronous Event Bus to decouple components and compute metrics."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, Set[Callable[[Any], None]]] = collections.defaultdict(set)

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        self._subscribers[event_type.__name__].add(handler)

    def unsubscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        if event_type.__name__ in self._subscribers:
            self._subscribers[event_type.__name__].discard(handler)

    def publish(self, event: BaseEvent) -> None:
        event_name = event.__class__.__name__
        # Call direct handlers
        for handler in list(self._subscribers[event_name]):
            try:
                handler(event)
            except Exception as e:
                # In robust production systems, we log but don't crash the publisher
                print(f"Error in subscriber handler for {event_name}: {e}")

        # Call global handlers subscribing to BaseEvent
        for handler in list(self._subscribers["BaseEvent"]):
            try:
                handler(event)
            except Exception as e:
                print(f"Error in global subscriber handler for {event_name}: {e}")


# =====================================================================
# Institutional Metrics Calculator
# =====================================================================

class InstitutionalMetricsCalculator:
    """Computes high-fidelity institutional health and scientific success metrics from events."""

    def __init__(self, event_bus: EventBus) -> None:
        self.bus = event_bus
        self.reset()
        self._register_subscriptions()

    def reset(self) -> None:
        self.reproducibility_runs: int = 0
        self.reproducibility_successes: int = 0
        self.citations_checked: int = 0
        self.citations_accurate: int = 0
        self.total_hypotheses: int = 0
        self.falsified_hypotheses: int = 0
        self.experiments_run: int = 0
        self.experiments_succeeded: int = 0
        self.total_publications: int = 0
        self.total_cost: float = 0.0
        self.creation_times: Dict[UUID, float] = {}
        self.validated_times: List[float] = []
        self.node_counts_by_type: Dict[str, int] = collections.defaultdict(int)
        self.governance_vetoes: int = 0
        self.publication_ratings: List[float] = []

    def _register_subscriptions(self) -> None:
        self.bus.subscribe(WorkflowStarted, self.on_workflow_started)
        self.bus.subscribe(ArtifactCreated, self.on_artifact_created)
        self.bus.subscribe(ExperimentCompleted, self.on_experiment_completed)
        self.bus.subscribe(ReviewFailed, self.on_review_failed)
        self.bus.subscribe(GovernanceRejected, self.on_governance_rejected)
        self.bus.subscribe(PublicationAccepted, self.on_publication_accepted)
        self.bus.subscribe(HypothesisFalsified, self.on_hypothesis_falsified)

    def on_workflow_started(self, event: WorkflowStarted) -> None:
        self.creation_times[event.project_uuid] = event.timestamp

    def on_artifact_created(self, event: ArtifactCreated) -> None:
        self.node_counts_by_type[event.artifact_type] += 1
        if event.artifact_type == "Hypothesis":
            self.total_hypotheses += 1
        elif event.artifact_type == "ReproducibilityReport":
            self.reproducibility_runs += 1

    def on_experiment_completed(self, event: ExperimentCompleted) -> None:
        self.experiments_run += 1
        self.total_cost += event.cost
        if event.success:
            self.experiments_succeeded += 1

    def on_review_failed(self, event: ReviewFailed) -> None:
        # Peer reviews failed
        pass

    def on_governance_rejected(self, event: GovernanceRejected) -> None:
        self.governance_vetoes += 1

    def on_publication_accepted(self, event: PublicationAccepted) -> None:
        self.total_publications += 1
        duration = event.timestamp - event.timestamp_started
        self.validated_times.append(duration)

    def on_hypothesis_falsified(self, event: HypothesisFalsified) -> None:
        self.falsified_hypotheses += 1

    def calculate_metrics(self) -> Dict[str, Any]:
        reproducibility_rate = (
            self.reproducibility_successes / self.reproducibility_runs
            if self.reproducibility_runs > 0
            else 1.0
        )
        experiment_success_rate = (
            self.experiments_succeeded / self.experiments_run
            if self.experiments_run > 0
            else 0.0
        )
        false_discovery_rate = (
            self.falsified_hypotheses / self.total_hypotheses
            if self.total_hypotheses > 0
            else 0.0
        )
        avg_time_to_validated_knowledge = (
            sum(self.validated_times) / len(self.validated_times)
            if self.validated_times
            else 0.0
        )
        knowledge_graph_growth = sum(self.node_counts_by_type.values())
        cost_per_validated_discovery = (
            self.total_cost / self.total_publications
            if self.total_publications > 0
            else self.total_cost
        )

        return {
            "reproducibility_rate": reproducibility_rate,
            "experiment_success_rate": experiment_success_rate,
            "false_discovery_rate": false_discovery_rate,
            "time_to_validated_knowledge": avg_time_to_validated_knowledge,
            "knowledge_graph_growth": knowledge_graph_growth,
            "research_throughput": self.total_publications,
            "cost_per_validated_discovery": cost_per_validated_discovery,
            "governance_vetoes": self.governance_vetoes,
        }
