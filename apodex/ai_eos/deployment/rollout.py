"""Progressive Rollout and Automated Rollback Controller implementation for AI-EOS.

Manages staged rollout states (Sandbox -> Shadow -> Canary -> Production) and triggers
automatic rollbacks/kill-switches upon SLA exceptions.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..domain.models import Capability
from ..capability_intelligence.manager import CapabilityRegistry

logger = logging.getLogger("ai_eos.deployment")


class ProgressiveRolloutController:
    """Manages staged rollout transitions and automated rollback triggers for system capabilities."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self.registry = registry
        self.active_stages = ["sandbox", "shadow", "canary", "production"]

    def transition_rollout_stage(self, capability_id: str, target_status: str) -> bool:
        """Move a capability forward in the rollout pipeline if it exists."""
        cap = self.registry.get_capability(capability_id)
        if not cap:
            return False

        if target_status not in self.active_stages:
            logger.warning(f"Invalid rollout stage requested: {target_status}")
            return False

        cap.deployment_status = target_status
        self.registry.register_capability(cap)
        logger.info(f"Transitioned capability {cap.name} [id={capability_id}] to rollout stage: {target_status}")
        return True

    def monitor_sla_metrics(self, capability_id: str, current_latency_ms: float, error_rate: float) -> bool:
        """Monitor active metrics and trigger an automated rollback if any SLA is violated."""
        cap = self.registry.get_capability(capability_id)
        if not cap:
            return False

        # SLA bounds
        is_violating = current_latency_ms > 250.0 or error_rate > 0.05
        if is_violating:
            logger.warning(f"SLA REGRESSION DETECTED on {cap.name}! Latency={current_latency_ms}ms, Error={error_rate:.2%}")

            # Execute automated rollback
            rollback_success = self.registry.trigger_rollback(
                capability_id=capability_id,
                reason=f"SLA Violation: Latency={current_latency_ms}ms, Error={error_rate:.2%}"
            )
            return rollback_success

        logger.debug(f"SLA checks clean for capability: {cap.name}")
        return False
