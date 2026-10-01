"""Integration test suite validating closed-loop interactions across all 5 cognitive OS subsystems:
1. Research OS
2. EIOS Kernel
3. EOS Engine
4. AEAN HiveMind
5. APODEX WorldModel & Cognitive Brain
"""

from __future__ import annotations

import pytest
import asyncio
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, VentureCell
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.cognition.brain import CognitiveBrain
from apodex.ai_eos.research.integration import ResearchToSystemBridge


@pytest.mark.asyncio
async def test_unified_5_subsystem_closed_loop():
    # 1. Instantiate all 5 subsystems
    ros = ResearchOS()
    eos = EOSEngine()
    eios = EIOSKernel()
    hive_mind = HiveMind(token_budget=100)
    world_model = WorldModel()
    brain = CognitiveBrain()

    # Create Cross-Layer System Bridge
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eos_engine=eos,
        eios_kernel=eios,
        hive_mind=hive_mind,
        world_model=world_model
    )

    # 2. Research OS: Register hypothesis & execute statistical validation
    hyp = ros.register_hypothesis(
        title="High-Frequency Active Inference Latency Reduction",
        description="Active inference state caching reduces decision latency by 35%.",
        null_hypothesis="Active inference state caching has no effect on latency.",
        target_metric="decision_latency_ms",
        significance_alpha=0.05
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=101)
    sim_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)
    assert sim_exp.is_statistically_significant is True
    assert hyp.status == "validated"

    # 3. ResearchToSystemBridge: Synchronize validated research across layers
    validated_hypotheses = ros.get_validated_hypotheses()
    assert len(validated_hypotheses) == 1

    sync_results = bridge.synchronize_all_pending_research()
    assert len(sync_results) == 1
    res = sync_results[0]
    assert res["eos_ingested"] is True
    assert res["eios_kernel_registered"] is True
    assert res["hive_mind_bidded"] is True
    assert res["world_model_updated"] is True

    # 4. EOS Engine: Verify active hypotheses and continuous sensing cycle
    assert len(eos.active_hypotheses) >= 1
    cell_a = VentureCell(cell_id=hyp.hypothesis_id, name="ActiveInferenceCell", namespace="active_inference_domain", capital_allocation_score=0.9)
    sensing_output = eos.run_continuous_sensing_cycle([cell_a], total_budget_cents=100000_00)
    assert "world_state" in sensing_output
    assert "allocated_budgets" in sensing_output

    # 5. EIOS Kernel: Verify anomaly sensing & DAG execution
    anomalies = eios.sense_opportunity_anomalies()
    assert len(anomalies) >= 1

    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag(goal="Deploy Active Inference Caching", target_budget_usd=50000)
    dag_success = await eios.execute_dag(dag)
    assert dag_success is True

    # 6. AEAN HiveMind: Arbitrate bids including registered research insight
    bids = list(hive_mind.registered_bids) + [
        TaskBid(task="gtm_funnel_optimization", priority=0.7, expected_value=0.8, token_cost=20)
    ]
    grants = hive_mind.arbitrate(bids)
    granted_map = hive_mind.granted_tasks(grants)
    assert len(grants) >= 1
    assert any("execute_research_insight" in k for k in granted_map.keys())

    # 7. APODEX WorldModel & Cognitive Brain: Verify graph nodes, beliefs & strategic cycle
    hyp_node_id = f"hyp_node_{str(hyp.hypothesis_id)[:8]}"
    assert hyp_node_id in world_model.beliefs
    assert world_model.beliefs[hyp_node_id]["mean"] > 0.8

    brain_res = brain.run_strategic_cycle("Deploy Active Inference Ecosystem")
    assert brain_res["plan_length"] > 0
    assert brain_res["claim_verified"] is True
