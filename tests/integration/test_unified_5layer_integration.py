"""Integration test suite validating closed-loop active inference cross-layer interaction
across Research OS (Layer 1), EIOS Kernel & EOS Engine (Layer 2), AEAN HiveMind (Layer 3),
and APODEX WorldModel (Layer 4) via ResearchToSystemBridge.
"""

from __future__ import annotations

import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_research_os_hypothesis_registration_and_validation():
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Hawkes Non-Gaussian Active Inference Signal",
        description="Non-Gaussian Hawkes process models market anomalies with sub-linear response time.",
        null_hypothesis="Hawkes process exhibits standard Gaussian noise without shift.",
        target_metric="sharpe_ratio",
        significance_alpha=0.05
    )
    assert hyp.status == "registered"

    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert completed_exp.status.value == "completed" or completed_exp.status == "COMPLETED"
    assert hyp.status in ["validated", "refuted"]


def test_cross_layer_active_inference_handoff_bridge():
    # Initialize 4-layer cognitive stack
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Causal Graph Bayesian Strategy Ingestion",
        description="Causal DAG updates increase decision certainty.",
        null_hypothesis="DAG updates do not alter decision variance.",
        target_metric="expected_free_energy",
        significance_alpha=0.05
    )
    hyp.status = "validated"

    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=100)
    world = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        world_model=world
    )

    record = bridge.handoff_validated_hypothesis(hyp.hypothesis_id, capital_allocation=15000.0)

    # Validate Layer 1 -> Layer 2 handoff
    assert record.status == "SUCCESS"
    assert len(eos.active_hypotheses) == 1
    assert len(kernel.research_hypotheses) == 1

    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) == 1
    assert anomalies[0]["title"] == "Causal Graph Bayesian Strategy Ingestion"

    # Validate Layer 2 -> Layer 3 handoff
    assert len(hive.registered_insights) == 1
    assert hive.registered_insights[0]["tokens"] == 150

    bids = [
        TaskBid(task="Sense Demand", priority=0.8, expected_value=1.0, token_cost=30),
        TaskBid(task=f"Execute Strategy for {hyp.title}", priority=0.9, expected_value=1.5, token_cost=50),
    ]
    grants = hive.arbitrate(bids)
    granted = hive.granted_tasks(grants)
    assert granted[f"Execute Strategy for {hyp.title}"] is True

    # Validate Layer 3 -> Layer 4 handoff
    assert len(world.nodes) == 1
    assert "Causal Graph Bayesian Strategy Ingestion" in world.beliefs
    assert world.beliefs["Causal Graph Bayesian Strategy Ingestion"]["confidence"] == 0.99


@pytest.mark.asyncio
async def test_eios_kernel_compiler_and_dag_execution():
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag(
        goal="Launch Cross-Layer Autonomous Research Flywheel",
        target_budget_usd=50000
    )
    assert len(dag.nodes) == 4

    kernel = EIOSKernel()
    success = await kernel.execute_dag(dag)
    assert success is True
