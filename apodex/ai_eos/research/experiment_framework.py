# -*- coding: utf-8 -*-
"""
experiment_framework.py: Authoritative candidate and baseline experiment tracker,
recording complete metadata, metrics, raw outcomes, effect sizes, and decisions.
"""
from __future__ import annotations
import math
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime


class ExperimentRecord:
    """Represents a fully documented scientific candidate experiment."""

    def __init__(
        self,
        hypothesis: str,
        baseline_version: str,
        candidate_version: str,
        task_distribution: str,
        metrics: List[str]
    ) -> None:
        self.experiment_id = uuid4()
        self.hypothesis = hypothesis
        self.baseline_version = baseline_version
        self.candidate_version = candidate_version
        self.task_distribution = task_distribution
        self.metrics = metrics
        self.sample_size = 0

        self.raw_baseline_results: List[float] = []
        self.raw_candidate_results: List[float] = []

        self.mean_baseline = 0.0
        self.mean_candidate = 0.0
        self.variance_baseline = 0.0
        self.variance_candidate = 0.0

        self.effect_size = 0.0
        self.t_statistic = 0.0
        self.p_value = 1.0
        self.decision = "INCONCLUSIVE"

    def log_trial_outcomes(self, baseline_outcomes: List[float], candidate_outcomes: List[float]) -> None:
        """Add outcomes, compute means, sample variances, t-statistics, and p-values."""
        self.raw_baseline_results = list(baseline_outcomes)
        self.raw_candidate_results = list(candidate_outcomes)
        self.sample_size = len(baseline_outcomes)

        if self.sample_size <= 1:
            self.p_value = 1.0
            return

        self.mean_baseline = sum(self.raw_baseline_results) / self.sample_size
        self.mean_candidate = sum(self.raw_candidate_results) / self.sample_size

        self.variance_baseline = sum((x - self.mean_baseline) ** 2 for x in self.raw_baseline_results) / (self.sample_size - 1)
        self.variance_candidate = sum((x - self.mean_candidate) ** 2 for x in self.raw_candidate_results) / (self.sample_size - 1)

        # Effect size (mean difference)
        self.effect_size = self.mean_candidate - self.mean_baseline

        # Two-sample independent t-statistic assuming unequal variances (Welch's t-test)
        se = math.sqrt((self.variance_baseline + self.variance_candidate) / self.sample_size)
        if se == 0:
            se = 1e-5

        self.t_statistic = self.effect_size / se
        # Gaussian approximation of p-value (two-tailed)
        self.p_value = 1.0 - math.erf(abs(self.t_statistic) / math.sqrt(2.0))

    def make_decision(self, alpha: float = 0.05) -> str:
        """Enforce strict statistical decision boundary to promote, reject, or revise candidates."""
        if self.p_value < alpha and self.effect_size > 0:
            self.decision = "PROMOTE"
        elif self.p_value < alpha and self.effect_size <= 0:
            self.decision = "REJECT"
        else:
            self.decision = "REVISE"
        return self.decision

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to a serializable dictionary for provenance trace inclusion."""
        return {
            "experiment_id": str(self.experiment_id),
            "hypothesis": self.hypothesis,
            "baseline_version": self.baseline_version,
            "candidate_version": self.candidate_version,
            "task_distribution": self.task_distribution,
            "metrics": self.metrics,
            "sample_size": self.sample_size,
            "mean_baseline": self.mean_baseline,
            "mean_candidate": self.mean_candidate,
            "effect_size": self.effect_size,
            "t_statistic": self.t_statistic,
            "p_value": self.p_value,
            "decision": self.decision
        }
