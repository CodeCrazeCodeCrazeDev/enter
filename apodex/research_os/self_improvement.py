from __future__ import annotations
import time
from uuid import UUID, uuid4
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from .models import InstitutionalPolicy, BaseArtifact
from .storage import ResearchRepository
from .events import EventBus

# =====================================================================
# Metacognitive Learning & Self-Improvement Flywheel
# =====================================================================

class WorkflowFailureTrace(BaseModel):
    run_id: UUID
    stage_id: str
    failure_reason: str
    timestamp: float = Field(default_factory=lambda: time.time())


class SelfImprovementFlywheel:
    """
    Closed-loop metacognitive self-improver. Analyzes structural bottlenecks,
    review rejections, and automatically evolves institutional policies and parameters.
    """

    def __init__(self, repository: ResearchRepository, event_bus: EventBus) -> None:
        self.repo = repository
        self.bus = event_bus
        self.failure_log: List[WorkflowFailureTrace] = []

    def log_failure(self, run_id: UUID, stage_id: str, reason: str) -> None:
        self.failure_log.append(WorkflowFailureTrace(
            run_id=run_id,
            stage_id=stage_id,
            failure_reason=reason
        ))

    def analyze_bottlenecks_and_evolve(self) -> Optional[InstitutionalPolicy]:
        """
        Analyzes logged failures and rejections. If a particular stage consistently fails
        (e.g., >= 2 failures), automatically creates a new InstitutionalPolicy enforcing
        stricter validation bounds, and saves it to the repository.
        """
        if not self.failure_log:
            return None

        # Count failures per stage
        stage_counts = {}
        for fail in self.failure_log:
            stage_counts[fail.stage_id] = stage_counts.get(fail.stage_id, 0) + 1

        # Identify bottleneck stage
        bottleneck_stage = None
        max_failures = 0
        for stage, count in stage_counts.items():
            if count > max_failures:
                max_failures = count
                bottleneck_stage = stage

        # Evolve rules if a bottleneck is significant (>= 2 failures)
        if bottleneck_stage and max_failures >= 2:
            new_policy = InstitutionalPolicy(
                policy_name=f"Stricter Quality Rule for {bottleneck_stage.capitalize()}",
                rules=[
                    f"All inputs to stage '{bottleneck_stage}' must possess a verification confidence rate of >= 0.85.",
                    "Execute 3x independent replicates before presenting conclusions to peer review.",
                    f"Mandate step-wise process verification: all sub-steps of stage '{bottleneck_stage}' must be validated against discrete process reward benchmarks before transitioning.",
                    f"Enforce Collective Intelligence Multi-Mind Consensus: a quorum of at least 3 distinct sub-agent perspectives must reach consensus on the correctness of '{bottleneck_stage}' execution outcomes."
                ],
                author="SelfImprovementFlywheel",
                confidence=1.0
            ).with_signature()

            self.repo.save_artifact(new_policy)
            return new_policy

        return None
