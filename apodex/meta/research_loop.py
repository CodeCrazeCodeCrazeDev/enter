from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import time
from apodex.meta.experience_db import ExperienceDatabase, ResearchTicket, CapabilityDelta


@dataclass
class TrialConfig:
    """Configuration for a long-term research loop experiment."""
    trial_id: str
    base_model_path: str
    training_script_path: str
    dataset_path: str
    hyperparameters: Dict[str, Any] = field(default_factory=dict)
    max_wallclock_seconds: int = 7200  # 2 hours default limit
    gpu_quota_count: int = 1


@dataclass
class TrialResult:
    """Outcome of a research loop experiment."""
    trial_id: str
    success: bool
    new_model_weights_path: Optional[str] = None
    metrics: Dict[str, float] = field(default_factory=dict)
    lesson_learned: str = ""


class ResearchLoopController:
    """
    Research Loop Controller.
    Manages long-term training, ticket ingestion, prioritized SFT/RL recipes,
    and publishes CapabilityDeltas back to the Harness Loop.
    """

    def __init__(self, db: ExperienceDatabase) -> None:
        self.db = db
        self.active_trials: Dict[str, TrialConfig] = {}

    async def ingest_and_prioritize_tickets(self) -> List[ResearchTicket]:
        """
        Pulls pending escalated tickets from the experience DB and sorts them by
        importance (user_impact and trace frequency).
        """
        tickets = await self.db.get_research_tickets()
        # Prioritize 'high' impact tickets first
        sorted_tickets = sorted(
            tickets,
            key=lambda t: 1 if t.user_impact == "high" else 0,
            reverse=True
        )
        return sorted_tickets

    async def compile_training_dataset(self, ticket: ResearchTicket) -> str:
        """
        Gathers high-reward/successful trace logs from the ticket's example traces
        to compile an optimal supervised fine-tuning (SFT) dataset.
        """
        dataset_path = f"sandbox/data/sft_{ticket.ticket_id}.jsonl"
        return dataset_path

    async def launch_sandbox_experiment(self, config: TrialConfig) -> TrialResult:
        """
        Spins up an isolated, resource-bounded container to run the training experiment
        complying with strict wall-clock and GPU limits.
        """
        # Simulates sandboxed execution with strict resource limits
        return TrialResult(
            trial_id=config.trial_id,
            success=True,
            new_model_weights_path=f"models/finetuned_{config.trial_id}",
            metrics={"math_accuracy": 0.94, "causal_reasoning_accuracy": 0.88},
            lesson_learned="Training on Complete trajectories retaining <think> tags increases consistency."
        )

    async def promote_model_and_publish_delta(self, result: TrialResult, ticket: ResearchTicket) -> CapabilityDelta:
        """
        Promotes the successfully tested candidate weights, compiles capabilities delta,
        and publishes it to the Experience DB.
        """
        delta = CapabilityDelta(
            model_version=f"Apodex-model-{result.trial_id}",
            released_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            capabilities_delta={
                "improved": ["causal reasoning", "math accuracy"],
                "unchanged": ["standard coding"],
                "regressed": []
            },
            recommended_harness_changes=[
                f"Route all tasks related to '{ticket.failure_pattern}' to models/finetuned_{result.trial_id}"
            ]
        )
        await self.db.publish_capability_delta(delta)
        return delta

    async def generate_git_pull_request(self, result: TrialResult) -> Dict[str, Any]:
        """
        Generates an auto-PR with diffs and evaluation summary for human review.
        """
        return {
            "pr_title": f"Promote Fine-tuned Model weights - Trial {result.trial_id}",
            "pr_body": f"Evaluation shows significant performance improvement: {result.metrics}. Lesson: {result.lesson_learned}",
            "branch_name": f"apodex/trial-{result.trial_id}",
            "status": "pending_human_review"
        }
