from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from apodex.evolution.common.models import MultiObjectiveMetric


class EvaluationReport(BaseModel):
    """Verbose report returned by the EvolutionVerifier."""
    is_valid: bool
    score: float
    metrics: MultiObjectiveMetric
    justification: str
    details: Dict[str, Any] = Field(default_factory=dict)


class EvolutionVerifier:
    """
    LLM-as-a-Verifier node designed to score agent completions/prompt parameters
    for evolutionary optimization. Considers correctness, cost, and latency.
    """

    def __init__(self, judge_name: str = "evo-judge-01"):
        self.judge_name = judge_name

    async def evaluate_output(
        self, prompt: str, completion: str, expected_keywords: Optional[List[str]] = None
    ) -> EvaluationReport:
        """
        Evaluates a completion's quality, cost, and latency.
        - quality: based on keyword matching, formatting, and structural constraints.
        - cost: simulated based on length of prompt + completion.
        - latency: simulated based on completion complexity.
        """
        # Determine raw quality score [0.0, 1.0]
        quality = 0.5  # baseline

        # Rule 1: Structural format
        if completion.strip().startswith("{") and completion.strip().endswith("}"):
            quality += 0.2
        elif completion.strip().startswith("[") and completion.strip().endswith("]"):
            quality += 0.1

        # Rule 2: Keyword overlap
        if expected_keywords:
            matched = sum(1 for kw in expected_keywords if kw.lower() in completion.lower())
            quality += (matched / len(expected_keywords)) * 0.3

        quality = min(1.0, max(0.0, quality))

        # Rule 3: Simulated cost (scaled [0.0, 1.0])
        total_length = len(prompt) + len(completion)
        cost = min(1.0, total_length / 2000.0)

        # Rule 4: Simulated latency (scaled [0.0, 1.0])
        latency = min(1.0, len(completion) / 1000.0)

        metrics = MultiObjectiveMetric(quality=quality, cost=cost, latency=latency)
        is_valid = quality >= 0.6

        justification = (
            f"Quality scored at {quality:.2f} based on structural constraints and overlaps. "
            f"Simulated cost={cost:.2f}, latency={latency:.2f}."
        )

        return EvaluationReport(
            is_valid=is_valid,
            score=quality,
            metrics=metrics,
            justification=justification,
            details={"judge": self.judge_name, "total_length": total_length}
        )
