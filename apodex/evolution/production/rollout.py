from __future__ import annotations
import random
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from apodex.memory.models import CostMode, CapabilityDelta
from apodex.evolution.common.models import EvolutionChangelog


class DeploymentVariant(BaseModel):
    """Represents a deployed model/workflow configuration variant in production."""
    variant_id: str
    target_capability: str
    traffic_percentage: float = Field(0.0, ge=0.0, le=100.0)
    verifier_scores: List[float] = Field(default_factory=list)
    latencies_sec: List[float] = Field(default_factory=list)


class EvolutionObservabilityMonitor:
    """
    Monitors live SLA statistics, tracking token costs, latency spikes, and
    detecting performance degradation to automatically trigger rollback.
    """

    def __init__(self, changelog: Optional[EvolutionChangelog] = None) -> None:
        self.changelog = changelog or EvolutionChangelog()
        self.incident_log: List[Dict[str, Any]] = []

    def record_sla_metrics(self, variant: DeploymentVariant, latency: float, score: float) -> bool:
        """
        Records live execution metrics.
        Returns True if metrics are healthy; False if a regression/SLA breach is detected
        (triggering automated rollback).
        """
        variant.latencies_sec.append(latency)
        variant.verifier_scores.append(score)

        # SLA checks
        latency_healthy = latency < 5.0  # Latency limit: 5 seconds
        score_healthy = score >= 0.5     # Quality score limit: 0.5

        if not (latency_healthy and score_healthy):
            incident = {
                "variant_id": variant.variant_id,
                "timestamp": time_only_sim(),
                "reason": "SLA_BREACH",
                "metrics": {"latency": latency, "score": score}
            }
            self.incident_log.append(incident)
            return False  # Regression!

        return True


def time_only_sim() -> float:
    return 1718000000.0


class ProductionRolloutManager:
    """
    Coordinates A/B testing variants and phased rollout percentages,
    safely auto-rolling back if the Observability Monitor flags an SLA regression.
    """

    def __init__(
        self,
        changelog: Optional[EvolutionChangelog] = None,
        monitor: Optional[EvolutionObservabilityMonitor] = None
    ) -> None:
        self.changelog = changelog or EvolutionChangelog()
        self.monitor = monitor or EvolutionObservabilityMonitor(changelog=self.changelog)
        self.active_variants: Dict[str, DeploymentVariant] = {}

    def register_variant(self, variant_id: str, target_capability: str, initial_traffic: float = 10.0) -> DeploymentVariant:
        """Deploys a new version as an A/B test or staged rollout variant."""
        var = DeploymentVariant(
            variant_id=variant_id,
            target_capability=target_capability,
            traffic_percentage=initial_traffic
        )
        self.active_variants[variant_id] = var
        return var

    def route_traffic(self) -> str:
        """Routes execution traffic based on deployment variant percentages."""
        if not self.active_variants:
            return "baseline"

        # Simple weighted selection
        r = random.uniform(0, 100)
        cumulative = 0.0
        for vid, variant in self.active_variants.items():
            cumulative += variant.traffic_percentage
            if r <= cumulative:
                return vid
        return "baseline"

    def adjust_staged_rollout(self, variant_id: str, delta_percentage: float) -> float:
        """Gradually scales up or down a rollout's traffic percentage."""
        var = self.active_variants.get(variant_id)
        if not var:
            raise ValueError("Variant not found")

        var.traffic_percentage = min(100.0, max(0.0, var.traffic_percentage + delta_percentage))
        return var.traffic_percentage

    def trigger_incident_rollback(self, variant_id: str) -> bool:
        """Rolls back an unhealthy deployment variant, setting traffic to 0."""
        var = self.active_variants.pop(variant_id, None)
        if not var:
            return False

        # Apply rollback in the evolution changelog
        self.changelog.rollback_last_change()
        return True
