"""Cross-layer integration tests for Cognitive OS subsystems:
Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, and APODEX CognitiveBrain.
"""

from __future__ import annotations

import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.cognition.brain import CognitiveBrain
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_research_os_export_and_promote():
    """Verify Research OS export to EIOS Kernel and promotion to EOS Engine."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()

    hyp = ros.register_hypothesis(
        title="Active Inference Market Sensing",
        description="Active inference reduces market uncertainty in SaaS GTM loops",
        null_hypothesis="Active inference has no effect on uncertainty",
        target_metric="uncertainty_reduction",
        significance_alpha=0.05
    )

    # Validate hypothesis via sandbox simulation
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)

    assert hyp.status == "validated"

    # Export to EIOS Kernel
    exported_payload = ros.export_validated_hypothesis_to_kernel(hyp.hypothesis_id, kernel)
    assert exported_payload["title"] == "Active Inference Market Sensing"
    assert len(kernel.research_hypotheses) == 1

    # Sense anomalies in EIOS Kernel
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) >= 1
    assert anomalies[0]["source"] == "research_os"

    # Promote to EOS Engine
    promoted_hyp = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert promoted_hyp is not None
    assert promoted_hyp.status == "active"
    assert len(eos.active_hypotheses) == 1


def test_aean_hive_mind_research_insight():
    """Verify AEAN HiveMind token bidding for research insights."""
    hive_mind = HiveMind(token_budget=50)

    bid = hive_mind.register_research_insight(
        insight={"title": "Causal Do-Calculus Optimization", "statement": "Pruning parent links reduces EFE variance"},
        priority=0.9,
        expected_value=0.85,
        token_cost=20
    )

    assert isinstance(bid, TaskBid)
    assert "Causal Do-Calculus Optimization" in bid.task

    grants = hive_mind.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].granted is True
    assert grants[0].tokens == 20


def test_research_to_system_bridge_propagation():
    """Verify end-to-end multi-layer active inference state propagation via ResearchToSystemBridge."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive_mind = HiveMind(token_budget=100)
    brain = CognitiveBrain()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind,
        brain=brain
    )

    hyp = ros.register_hypothesis(
        title="Deep Reinforcement Learning with EFE Bounding",
        description="EFE bounding prevents runaway exploration in swarm agents",
        null_hypothesis="EFE bounding does not alter exploration rate",
        target_metric="exploration_rate",
        significance_alpha=0.05
    )

    propagation_res = bridge.propagate_validated_hypothesis(hyp.hypothesis_id, ground_truth_yield=3.5)

    assert propagation_res["is_significant"] is True
    assert propagation_res["kernel_exported"] is True
    assert propagation_res["kernel_anomalies_sensed"] >= 1
    assert propagation_res["eos_promoted"] is True
    assert propagation_res["hive_mind_bid_granted"] is True
    assert "brain_fact_id" in propagation_res

    # Check that brain memory asserted the semantic fact
    assert len(brain.memory.semantic_memory) >= 1
