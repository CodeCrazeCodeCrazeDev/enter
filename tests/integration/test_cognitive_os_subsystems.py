from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind


def test_research_os_to_kernel_and_eos_handoff() -> None:
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()

    # 1. Hypothesis registration
    hyp = ros.register_hypothesis(
        title="Dynamic Active Inference Price Elasticity Optimization",
        description="Testing non-linear price elasticity under active inference state handoffs.",
        null_hypothesis="price_elasticity <= 0",
        target_metric="price_elasticity",
        significance_alpha=0.05
    )

    # 2. Experiment simulation & validation
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=42)
    exp_res = ros.execute_experiment_simulation(experiment_id=exp.experiment_id, ground_truth_yield=1.5)

    assert hyp.status == "validated"
    assert exp_res.is_statistically_significant is True

    # 3. Export to EIOS Kernel
    exported = ros.export_validated_hypothesis_to_kernel(hypothesis_id=hyp.hypothesis_id, eios_kernel=kernel)
    assert exported is True
    assert len(kernel.registered_hypotheses) == 1

    # 4. EIOS Kernel anomaly sensing
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) == 1
    assert anomalies[0]["title"] == "Dynamic Active Inference Price Elasticity Optimization"
    assert anomalies[0]["efe_score"] > 1.0

    # 5. Promote to EOS Engine
    promoted = ros.promote_hypothesis_to_eos(hypothesis_id=hyp.hypothesis_id, eos_engine=eos)
    assert promoted is True
    assert hyp.hypothesis_id in eos.active_hypotheses


def test_research_to_system_bridge_end_to_end() -> None:
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive_mind = HiveMind()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind
    )

    record = bridge.execute_cross_layer_handoff(
        hypothesis_title="Autonomous Multi-Agent GTM Channel Discovery",
        hypothesis_description="Evaluating high-converting multi-agent GTM outreach channels.",
        target_metric="conversion_rate",
        ground_truth_yield=2.0,
        seed=100
    )

    assert record["status"] == "validated"
    assert record["is_statistically_significant"] is True
    assert record["eios_anomalies_sensed"] >= 1
    assert record["eos_ingested"] is True
    assert "aean_consensus_score" in record
    assert len(bridge.handoff_audit_trail) == 1


def test_data_leakage_and_statistical_guardrails() -> None:
    ros = ResearchOS()

    train_data = ["user_1", "user_2", "user_3"]
    test_data = ["user_3", "user_4", "user_5"]

    # Verify data leakage detection
    has_leakage = ros.detect_data_leakage(train_data, test_data)
    assert has_leakage is True

    clean_test_data = ["user_4", "user_5", "user_6"]
    no_leakage = ros.detect_data_leakage(train_data, clean_test_data)
    assert no_leakage is False
