"""Unified 5-Layer Integration Test Suite.

Validates end-to-end active inference state handoffs and cross-layer execution
across Layer 1 (Research OS), Layer 2 (EIOS Kernel & EOS Engine), Layer 3 (AEAN HiveMind),
Layer 4 (APODEX WorldModel), and ResearchToSystemBridge.
"""

import pytest
import asyncio
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, ExecutionDAG, ExecutionNode
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_research_os_hypothesis_registration_and_validation():
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Active Inference Multi-Agent Bidding",
        description="EFE routing optimizes token allocation efficiency by 25%",
        null_hypothesis="EFE routing has no effect on token allocation efficiency",
        target_metric="token_efficiency"
    )

    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=42)
    validated_exp = ros.execute_experiment_simulation(experiment_id=exp.experiment_id, ground_truth_yield=2.5)

    assert validated_exp.is_statistically_significant is True
    assert hyp.status == "validated"


def test_research_to_system_bridge_propagation():
    ros = ResearchOS()
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

    hyp = ros.register_hypothesis(
        title="Hawkes Process AST Recursive Rewrite",
        description="Non-Gaussian Hawkes process controls recursion stability",
        null_hypothesis="Hawkes process does not affect stability",
        target_metric="ast_safety"
    )
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(experiment_id=exp.experiment_id, ground_truth_yield=3.0)

    record = bridge.propagate_validated_hypothesis(hyp.hypothesis_id)
    assert record["status"] == "validated"

    # Check EIOS Kernel
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) >= 1
    assert anomalies[0]["hypothesis_id"] == str(hyp.hypothesis_id)

    # Check EOS Engine
    assert len(eos.active_hypotheses) == 1

    # Check AEAN HiveMind
    bid = hive.register_research_insight(insight_name=hyp.title)
    grants = hive.arbitrate([bid])
    assert grants[0].granted is True

    # Check WorldModel
    node_id = f"hyp_node_{str(hyp.hypothesis_id)[:8]}"
    assert node_id in world.nodes
    assert "belief_ast_safety" in world.beliefs
    assert world.beliefs["belief_ast_safety"]["prior"] == 0.75


@pytest.mark.asyncio
async def test_full_5layer_unified_active_inference_workflow():
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=200)
    world = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        world_model=world
    )

    # 1. Scientific Research Hypothesis Validation
    hyp = ros.register_hypothesis(
        title="Active Inference Expected Free Energy Scaling",
        description="EFE active inference minimizes total organizational entropy",
        null_hypothesis="EFE does not reduce entropy",
        target_metric="organizational_entropy"
    )
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=99)
    ros.execute_experiment_simulation(experiment_id=exp.experiment_id, ground_truth_yield=2.8)

    # 2. Bridge State Propagation
    bridge.propagate_validated_hypothesis(hyp.hypothesis_id)

    # 3. Execution DAG via EIOS Kernel
    dag = ExecutionDAG()
    node = ExecutionNode(name="Active Inference Execution Node", action_type="execution")
    dag.add_node(node)
    result = await kernel.execute_dag(dag)
    assert result is True

    # 4. EOS Continuous Sensing Loop
    sensing_result = eos.run_continuous_sensing_cycle(cells=[], total_budget_cents=100000_00)
    assert "world_state" in sensing_result

    # 5. AEAN HiveMind Token Arbitration
    bid = TaskBid(task="execute_active_inference", priority=0.95, expected_value=0.85, token_cost=50)
    grants = hive.arbitrate([bid])
    assert grants[0].granted is True

    # 6. WorldModel Belief Sanity Check
    assert world.beliefs["belief_organizational_entropy"]["prior"] == 0.75
