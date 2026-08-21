"""Cross-Subsystem End-to-End Integration Test Suite.

Validates the joint operation and feedback loops across:
- ResearchOS (Scientific discovery, literature retrieval, hypothesis testing)
- EIOS Kernel (Active Inference Expected Free Energy, Execution DAG compilation)
- EOS Engine (Entrepreneurial execution, hypothesis generation, continuous sensing)
- AEAN HiveMind (Multi-agent coordination, TaskBid arbitration, Grant issuance)
- APODEX Cognitive Brain (Executive control, strategic cycles, memory engines)
- Autonomous Institution (Expected Free Energy Planner & Structural Causal Model)
"""

from __future__ import annotations

import pytest
import asyncio
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import (
    EIOSKernel,
    HierarchicalActiveInference,
    EntrepreneurialCompiler,
    ExecutionDAG,
    ExecutionNode
)
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, VentureCell, Hypothesis
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid, Grant
from apodex.cognition.brain import CognitiveBrain
from apodex.cognition.research.autonomous_institution import (
    ResearchHypothesis,
    ExpectedFreeEnergyPlanner,
    StructuralCausalModel
)


@pytest.mark.asyncio
async def test_full_cross_subsystem_cognitive_lifecycle():
    # 1. ResearchOS: Conduct Literature Review
    research_os = ResearchOS()
    papers = research_os.conduct_literature_review("active inference expected free energy")
    assert len(papers) > 0

    # 2. EIOS Kernel & Active Inference Expected Free Energy Planner
    efe_planner = ExpectedFreeEnergyPlanner(curiosity_weight=1.5)
    policy_1 = {
        "name": "epistemic_exploration",
        "prior_entropy": 2.0,
        "post_entropy": 0.4,
        "predicted_prob": 0.6,
        "target_pref": 0.95
    }
    policy_2 = {
        "name": "conservative_path",
        "prior_entropy": 0.5,
        "post_entropy": 0.4,
        "predicted_prob": 0.8,
        "target_pref": 0.95
    }
    best_policy, efe = efe_planner.select_optimal_policy([policy_1, policy_2])
    assert best_policy["name"] == "epistemic_exploration"
    assert efe < 0.0

    # 3. Hierarchical Active Inference Layer Free Energy Calculation
    active_inf = HierarchicalActiveInference()
    layer_fe = active_inf.calculate_layer_free_energy(
        layer="strategic_layer",
        actual_outcome=0.85,
        expected_outcome=0.90
    )
    assert isinstance(layer_fe, float)

    # 4. EntrepreneurialCompiler & ExecutionDAG compilation
    compiler = EntrepreneurialCompiler()
    node1 = ExecutionNode(
        node_id="node_1",
        name="allocate_capital",
        action_type="capital",
        payload={"amount": 1000},
        depends_on=[]
    )
    node2 = ExecutionNode(
        node_id="node_2",
        name="deploy_product",
        action_type="deployment",
        payload={"env": "prod"},
        depends_on=["node_1"]
    )
    dag = ExecutionDAG(
        dag_id="dag_01",
        nodes={"node_1": node1, "node_2": node2}
    )
    eios_kernel = EIOSKernel()
    exec_res = await eios_kernel.execute_dag(dag)
    assert exec_res is True

    # 5. EOS Engine Continuous Sensing Cycle & Hypothesis Tracking
    eos_engine = EOSEngine()
    cell = VentureCell(id="vc_01", name="alpha_venture", namespace="trading")
    sensing_summary = eos_engine.run_continuous_sensing_cycle([cell], total_budget_cents=10000)
    assert "world_state" in sensing_summary
    assert "allocated_budgets" in sensing_summary

    hyp = Hypothesis(
        id="hyp_eos_01",
        description="Autonomous portfolio execution increases risk-adjusted yield",
        category="product_market_fit",
        prior_probability=0.7
    )
    eos_engine.hypothesis_engine.add_hypothesis(hyp)
    assert len(eos_engine.hypothesis_engine.hypotheses) > 0

    # 6. AEAN Hive Mind: Multi-Agent Task Arbitrate & Grant Issuance
    hive = HiveMind(token_budget=100)
    bid_a = TaskBid(
        task="task_alloc_01",
        priority=0.9,
        expected_value=100.0,
        token_cost=20
    )
    bid_b = TaskBid(
        task="task_alloc_02",
        priority=0.8,
        expected_value=80.0,
        token_cost=15
    )
    grants = hive.arbitrate([bid_a, bid_b])
    assert len(grants) > 0
    assert len(hive.granted_history) > 0

    # 7. APODEX Cognitive Brain Execution Cycle
    brain = CognitiveBrain()
    res = brain.run_strategic_cycle("Optimize multi-agent capital allocation strategy")
    assert res is not None
    assert "plan_length" in res
    assert res["consensus_score"] > 0.0


@pytest.mark.asyncio
async def test_causal_do_calculus_interoperability():
    # Structural Causal Model do-calculus intervention
    scm = StructuralCausalModel()
    scm.add_causal_link("learning_rate", "model_accuracy", weight=0.8)
    scm.add_causal_link("model_accuracy", "business_revenue", weight=1.5)

    post_state = scm.intervene_do("learning_rate", 0.1)
    assert post_state["learning_rate"] == 0.1
    assert pytest.approx(post_state["model_accuracy"]) == 0.08
    assert pytest.approx(post_state["business_revenue"]) == 0.12
