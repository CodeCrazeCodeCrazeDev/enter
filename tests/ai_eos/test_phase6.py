"""Unit tests for Phase 6 Frontier Capability & Model Intelligence and Capability Registry."""

import pytest
from apodex.ai_eos.domain.models import Capability, SubsystemMaturity
from apodex.ai_eos.capability_intelligence.manager import CapabilityRegistry, CapabilityIntelligenceManager


def test_capability_four_pipeline_lifecycle():
    """Verify Discovery, Distillation, Validation, and Promotion of capabilities."""
    registry = CapabilityRegistry()
    manager = CapabilityIntelligenceManager(registry=registry)

    # 1. Pipeline A: Discovery
    candidates = manager.discover_candidates(source_feed="arxiv_research")
    assert len(candidates) == 1
    assert "MonteCarloTreeSearchAdCreative" in candidates[0]["name"]

    # 2. Pipeline B: Distillation
    cap = manager.distill_capability(candidates[0])
    assert cap.maturity == SubsystemMaturity.EXPERIMENTAL
    assert cap.deployment_status == "staged"
    assert "arxiv_research" in cap.origin

    # 3. Pipeline C: Validation (Simulate successful validation)
    passed = manager.validate_capability_sandbox(cap, simulated_acc=0.88, cost_ratio=1.10)
    assert passed is True
    assert cap.maturity == SubsystemMaturity.VALIDATED
    assert cap.benchmark_results["accuracy"] == 0.88

    # 4. Pipeline D: Promotion
    success = manager.promote_to_production(cap)
    assert success is True
    assert cap.maturity == SubsystemMaturity.PRODUCTION
    assert cap.deployment_status == "production"

    # Verify registered
    registered_cap = registry.get_capability(cap.capability_id)
    assert registered_cap == cap


def test_capability_rollback_mechanics():
    """Verify that degrading performance triggers rollback and logs a negative signal."""
    registry = CapabilityRegistry()
    manager = CapabilityIntelligenceManager(registry=registry)

    cap = Capability(
        capability_id="cap_test_b",
        name="AnomalyDetector",
        description="Fuzzy logic anomaly scoring",
        source="apodex/execution/anomaly.py",
        origin="internal",
        owner="Operations",
        maturity=SubsystemMaturity.VALIDATED,
        deployment_status="canary",
        rollback_trigger="error_rate > 0.05",
        retirement_policy="unusable"
    )

    manager.promote_to_production(cap)
    assert registry.get_capability("cap_test_b").deployment_status == "production"

    # Trigger Rollback
    rollback_success = registry.trigger_rollback("cap_test_b", reason="SLA error_rate spike to 0.12")
    assert rollback_success is True

    # Check that capability is now rolled back and deprecated
    rolled_cap = registry.get_capability("cap_test_b")
    assert rolled_cap.deployment_status == "rolled_back"
    assert rolled_cap.maturity == SubsystemMaturity.DEPRECATED
    assert len(registry._rollback_history) == 1
    assert registry._rollback_history[0]["reason"] == "SLA error_rate spike to 0.12"


def test_frontier_model_routing():
    """Verify prompt routing policies compiled based on model profiles."""
    registry = CapabilityRegistry()
    manager = CapabilityIntelligenceManager(registry=registry)

    policy_cheap = manager.get_optimal_routing_policy(task_domain="coding", budget_tier="CHEAP")
    assert policy_cheap == "Qwen-2.5-Coder"

    policy_expensive = manager.get_optimal_routing_policy(task_domain="math", budget_tier="EXPENSIVE")
    assert policy_expensive == "DeepSeek-R1"
