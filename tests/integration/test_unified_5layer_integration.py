"""
Unified 5-Layer Cross-Subsystem Integration Test Suite.
Validates end-to-end active inference workflows across:
1. Layer 1: Research OS
2. Layer 2: EIOS Kernel & EOS Engine
3. Layer 3: AEAN HiveMind
4. Layer 4: APODEX WorldModel & Cognitive Brain
5. ResearchToSystemBridge Orchestration
"""

import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler, ExecutionDAG
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge
from apodex.ai_eos.research.integration import ResearchToSystemBridge


@pytest.mark.asyncio
async def test_research_os_hypothesis_registration_and_validation():
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="GRPO Optimization in Micro-VMs",
        description="Applying GRPO RL policy updates reduces convergence time by 25%",
        null_hypothesis="H0: GRPO optimization yield <= 0",
        target_metric="convergence_speedup"
    )
    assert hyp.status == "registered"

    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    validated_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.0)

    assert validated_exp.is_statistically_significant is True
    assert hyp.status == "validated"
    assert validated_exp.p_value < 0.05


@pytest.mark.asyncio
async def test_eios_kernel_compilation_and_execution():
    kernel = EIOSKernel()
    compiler = EntrepreneurialCompiler()

    dag = compiler.compile_goal_to_dag("Scale AI Agent Infrastructure", target_budget_usd=50000)
    assert len(dag.nodes) == 4

    success = await kernel.execute_dag(dag)
    assert success is True
    assert all(node.status == "COMPLETED" for node in dag.nodes.values())


@pytest.mark.asyncio
async def test_eos_engine_opportunity_scoring_and_promotion():
    ros = ResearchOS()
    eos = EOSEngine()

    hyp = ros.register_hypothesis(
        title="SaaS Churn Reduction via Active Inference",
        description="Predictive churn sensing reduces customer cancellation by 18%",
        null_hypothesis="H0: Churn reduction <= 0",
        target_metric="churn_rate"
    )

    res = ros.promote_hypothesis_to_eos(hyp.hypothesis_id, eos)
    assert res is not None
    assert len(eos.active_hypotheses) == 1


@pytest.mark.asyncio
async def test_aean_hive_mind_token_arbitration():
    hive_mind = HiveMind(token_budget=30)

    bids = [
        TaskBid(task="Sense Customer Demand", priority=0.95, expected_value=0.90, token_cost=10),
        TaskBid(task="Run Funnel Optimization", priority=0.85, expected_value=0.80, token_cost=15),
        TaskBid(task="Rebalance Capital Reserves", priority=0.70, expected_value=0.60, token_cost=15),
    ]

    grants = hive_mind.arbitrate(bids)
    assert len(grants) == 3

    granted_tasks = hive_mind.granted_tasks(grants)
    # The top 2 bids (cost 10 + 15 = 25 <= budget 30) should be granted
    assert granted_tasks["Sense Customer Demand"] is True
    assert granted_tasks["Run Funnel Optimization"] is True
    assert granted_tasks["Rebalance Capital Reserves"] is False


@pytest.mark.asyncio
async def test_apodex_world_model_causal_and_belief_updates():
    wm = WorldModel()

    node1 = CausalNode(node_id="n_research_01", node_type="hypothesis", properties={"title": "Micro-VM Scaling"})
    node2 = CausalNode(node_id="n_exec_01", node_type="deployment", properties={"status": "active"})

    wm.add_node(node1)
    wm.add_node(node2)

    edge = RelationEdge(source_id="n_research_01", target_id="n_exec_01", relation_type="triggers", weight=0.9)
    wm.add_edge(edge)

    wm.beliefs["n_research_01"] = {"validated": True, "p_value": 0.001}

    assert wm.contains_node("n_research_01")
    assert wm.contains_node("n_exec_01")
    assert len(wm.beliefs) == 1


@pytest.mark.asyncio
async def test_research_to_system_bridge_end_to_end_handoff():
    ros = ResearchOS()
    kernel = EIOSKernel()
    compiler = EntrepreneurialCompiler()
    eos = EOSEngine()
    hive_mind = HiveMind(token_budget=100)
    wm = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        kernel=kernel,
        compiler=compiler,
        eos_engine=eos,
        hive_mind=hive_mind,
        world_model=wm
    )

    report = await bridge.execute_full_research_pipeline_handoff(
        title="Autonomous Agent Token Arbitration",
        description="Second-price token auction optimizes multi-agent resource efficiency by 30%",
        null_hypothesis="H0: Token arbitration efficiency <= 0",
        target_metric="compute_efficiency",
        ground_truth_yield=2.5
    )

    assert report["hypothesis_status"] == "validated"
    assert report["experiment_statistically_significant"] is True
    assert report["kernel_execution_success"] is True
    assert report["hive_mind_grants"] >= 1
    assert report["world_model_node_id"].startswith("hyp_node_")
    assert len(wm.beliefs) == 1
    assert len(eos.active_hypotheses) == 1
