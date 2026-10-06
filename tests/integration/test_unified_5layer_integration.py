"""
test_unified_5layer_integration.py: Multi-layer closed-loop integration test suite validating
joint interactions across Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, and APODEX WorldModel.
"""

from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.ai_eos.domain.models import VentureCell
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_research_os_hypothesis_validation_lifecycle() -> None:
    """Verifies Research OS hypothesis registration and statistical validation simulation."""
    ros = ResearchOS()

    # 1. Register hypothesis
    hyp = ros.register_hypothesis(
        title="Active Inference Allocation Advantage",
        description="Active inference EFE scoring yields higher capital efficiency.",
        null_hypothesis="Active inference yields equal or lower capital efficiency.",
        target_metric="roi_capital_efficiency",
        significance_alpha=0.05
    )
    assert hyp.status == "registered"

    # 2. Create sandbox experiment
    exp = ros.create_experiment(hyp.hypothesis_id, seed=1234)
    assert exp.hypothesis_id == hyp.hypothesis_id

    # 3. Simulate statistical validation walk-forward
    validated_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)
    assert validated_exp.is_statistically_significant is True
    assert ros.hypotheses.get(hyp.hypothesis_id).status == "validated"


def test_eios_kernel_and_eos_engine_integration() -> None:
    """Verifies EIOS Kernel anomaly sensing and EOS Engine opportunity ingestion."""
    kernel = EIOSKernel()
    eos = EOSEngine()

    # 1. Kernel senses market signals
    market_signals = [
        {"name": "b2b_saas_demand", "variance": 0.25},
        {"name": "consumer_fintech_demand", "variance": 0.05}
    ]
    anomalies = kernel.sense_opportunity_anomalies(market_signals)
    assert len(anomalies) == 1
    assert anomalies[0]["signal_name"] == "b2b_saas_demand"
    assert anomalies[0]["efe_value"] > 0.5

    # 2. Ingest validated hypothesis into EOS
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Predictive Moat Expansion",
        description="Moat durability increases with network density.",
        null_hypothesis="No correlation.",
        target_metric="moat_durability"
    )
    eos.ingest_validated_research(hyp)

    assert len(eos.active_hypotheses) == 1
    matches = eos.opportunity_graph.find_similar_opportunities(["predictive", "moat"])
    assert len(matches) > 0


def test_aean_hive_mind_token_arbitration() -> None:
    """Verifies AEAN HiveMind research insight bidding and second-price token arbitration."""
    hive_mind = HiveMind(token_budget=50)

    # Register research insight bid
    research_bid = hive_mind.register_research_insight(
        task_name="execute_active_inference_strategy",
        priority=0.90,
        expected_value=0.95,
        token_cost=20
    )

    standard_bid = TaskBid(
        task="routine_log_cleanup",
        priority=0.20,
        expected_value=0.10,
        token_cost=10
    )

    grants = hive_mind.arbitrate([research_bid, standard_bid])
    granted_map = hive_mind.granted_tasks(grants)

    assert granted_map["execute_active_inference_strategy"] is True
    assert granted_map["routine_log_cleanup"] is True


def test_apodex_world_model_causal_nodes_and_beliefs() -> None:
    """Verifies APODEX WorldModel causal graph node creation and Bayesian belief tracking."""
    wm = WorldModel()

    node = wm.create_node(
        node_id="hyp_node_01",
        node_type="research_hypothesis",
        properties={"title": "Bayesian Belief Calibration"}
    )
    assert node.node_id == "hyp_node_01"

    belief = wm.update_belief(
        belief_key="active_inference_superiority",
        prior_prob=0.50,
        posterior_prob=0.92,
        evidence_count=5
    )
    assert belief["posterior_prob"] == 0.92
    assert wm.beliefs["active_inference_superiority"]["evidence_count"] == 5


def test_research_to_system_bridge_cross_layer_handoff() -> None:
    """Verifies complete end-to-end 5-layer active inference cross-layer handoff via ResearchToSystemBridge."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive_mind = HiveMind(token_budget=100)
    world_model = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind,
        world_model=world_model
    )

    # Layer 1: Register and validate hypothesis
    hyp = ros.register_hypothesis(
        title="Cross Layer Unified Active Inference",
        description="Integrating Layer 1 to Layer 4 yields sub-linear coordination latencies.",
        null_hypothesis="No latency reduction.",
        target_metric="coordination_latency"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=999)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)

    validated_hyp = ros.hypotheses.get(hyp.hypothesis_id)
    assert validated_hyp.status == "validated"

    # Execute Cross-Layer State Handoff
    results = bridge.execute_cross_layer_handoff(validated_hyp)

    assert results["layer1_research_status"] == "validated"
    assert results["layer2_eos_ingested"] is True
    assert results["layer2_kernel_sensed"] is True
    assert results["layer3_hive_mind_bid"] is True
    assert results["layer4_world_model_updated"] is True

    # Confirm subsystem states after handoff
    assert len(kernel.registered_hypotheses) == 1
    assert len(eos.active_hypotheses) == 1
    assert len(hive_mind.granted_history) == 0  # Bids registered, arbitration pending
    assert len(world_model.beliefs) == 1
