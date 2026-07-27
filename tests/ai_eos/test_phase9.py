"""Unit tests for Phase 9 Progressive Deployment and Automated Rollback."""

import pytest
from apodex.ai_eos.domain.models import Capability, SubsystemMaturity
from apodex.ai_eos.capability_intelligence.manager import CapabilityRegistry
from apodex.ai_eos.deployment.rollout import ProgressiveRolloutController


def test_progressive_rollout_transitions():
    """Verify capabilities step cleanly through staging transitions."""
    registry = CapabilityRegistry()
    controller = ProgressiveRolloutController(registry=registry)

    cap = Capability(
        capability_id="cap_rollout",
        name="DynamicBiddingEngine",
        description="Active feedback loops",
        source="apodex/models/bid.py",
        origin="internal",
        owner="Executive",
        rollback_trigger="error_rate > 0.05",
        retirement_policy="none"
    )

    registry.register_capability(cap)

    # Move to shadow
    success = controller.transition_rollout_stage("cap_rollout", "shadow")
    assert success is True
    assert registry.get_capability("cap_rollout").deployment_status == "shadow"

    # Move to canary
    success = controller.transition_rollout_stage("cap_rollout", "canary")
    assert success is True
    assert registry.get_capability("cap_rollout").deployment_status == "canary"


def test_automated_rollback_on_sla_breach():
    """Verify that metric threshold violations trigger immediate configuration rollback."""
    registry = CapabilityRegistry()
    controller = ProgressiveRolloutController(registry=registry)

    cap = Capability(
        capability_id="cap_sla",
        name="FragileModel",
        description="High latency model",
        source="apodex/models/fragile.py",
        origin="internal",
        owner="Executive",
        rollback_trigger="latency > 250",
        retirement_policy="none"
    )

    registry.register_capability(cap)
    controller.transition_rollout_stage("cap_sla", "production")

    # Monitor normal metrics -> no rollback
    rolled_back = controller.monitor_sla_metrics("cap_sla", current_latency_ms=120.0, error_rate=0.01)
    assert rolled_back is False
    assert registry.get_capability("cap_sla").deployment_status == "production"

    # Monitor SLA breach (latency exceeds 250ms) -> triggers automatic rollback!
    rolled_back = controller.monitor_sla_metrics("cap_sla", current_latency_ms=310.0, error_rate=0.01)
    assert rolled_back is True

    # Re-fetch capability and verify deactivated/rolled_back state
    rolled_cap = registry.get_capability("cap_sla")
    assert rolled_cap.deployment_status == "rolled_back"
    assert rolled_cap.maturity == SubsystemMaturity.DEPRECATED
