# -*- coding: utf-8 -*-
"""
test_cognitive_os_subsystems.py: Cross-layer integration test suite validating
joint interactions across Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind,
and APODEX WorldModel.
"""

import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel


def test_research_to_system_bridge_integration():
    """Validates end-to-end active inference state handoffs across all 5 cognitive OS subsystems."""
    # 1. Initialize Subsystems
    ros = ResearchOS()
    eios = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=100)
    wm = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=eios,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    # 2. Register and validate hypothesis in Layer 1 Research OS
    hyp = ros.register_hypothesis(
        title="Active Inference Expected Free Energy GTM Optimization",
        description="Active inference EFE routing reduces customer acquisition CAC by 25%.",
        null_hypothesis="EFE routing has no effect on CAC.",
        target_metric="cac_reduction"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status in ["validated", "registered", "refuted"]

    # 3. Handoff hypothesis to Layer 2 EOS Engine and EIOS Kernel
    handoff_res = bridge.hand_off_hypothesis_to_eios_and_eos(hyp.hypothesis_id)
    assert handoff_res["hypothesis_id"] == str(hyp.hypothesis_id)
    assert handoff_res.get("eos_ingested") is True
    assert handoff_res.get("eios_ingested") is True

    # 4. Handoff insight to Layer 3 AEAN HiveMind token bidding
    insight_res = bridge.hand_off_insight_to_aean(
        insight_task="Scale EFE Ads Campaign",
        priority=0.9,
        expected_value=0.85,
        token_cost=20
    )
    assert insight_res["task"] == "Scale EFE Ads Campaign"
    assert insight_res["granted"] is True

    # 5. Handoff causal state to Layer 4 APODEX WorldModel
    wm_res = bridge.hand_off_causal_state_to_world_model(
        entity_id="efe_gtm_experiment_v1",
        node_type="empirical_hypothesis",
        properties={"confidence": 0.95, "cac_reduction": 0.28}
    )
    assert wm_res["world_model_updated"] is True
    assert "efe_gtm_experiment_v1" in wm.beliefs
    assert wm.beliefs["efe_gtm_experiment_v1"]["confidence"] == 0.95


@pytest.mark.asyncio
async def test_eios_dag_execution_with_compiler():
    """Validates EIOS Entrepreneurial Compiler DAG generation and execution."""
    compiler = EntrepreneurialCompiler()
    kernel = EIOSKernel()

    dag = compiler.compile_goal_to_dag(
        goal="Achieve 10k MRR with Autonomous AI Agents",
        target_budget_usd=1000
    )
    assert len(dag.nodes) == 4

    success = await kernel.execute_dag(dag)
    assert success is True
    assert all(node.status == "COMPLETED" for node in dag.nodes.values())
