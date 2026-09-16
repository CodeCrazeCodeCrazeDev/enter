"""Cross-layer integration test suite validating active inference state handoffs,
compiler DAG generation, multi-agent dispatching, and belief network updates
across Layer 1 Research OS, Layer 2 EIOS Kernel & EOS Engine, Layer 3 AEAN,
and Layer 4 APODEX.
"""

from __future__ import annotations
import pytest
import asyncio
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler, HierarchicalActiveInference
from apodex.ai_eos.intelligence.eos_engine import EOSEngine, VentureCell
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import (
    ResearchToSystemBridge,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
)


@pytest.mark.asyncio
async def test_unified_4layer_active_inference_and_execution_pipeline():
    # Layer 1: Research OS literature synthesis and hypothesis validation
    ros = ResearchOS()
    lit_review = ros.conduct_literature_review("Multi-Agent Active Inference")
    assert "Active Inference with Expected Free Energy approximation" in lit_review["synthesized_trends"]

    hyp = ros.register_hypothesis(
        title="Multi-Agent Free Energy Minimization",
        description="Active inference hierarchy reduces cross-layer strategy divergence",
        null_hypothesis="Free energy minimization has no impact on divergence",
        target_metric="strategy_divergence"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.5)
    assert completed_exp.is_statistically_significant is True

    # Layer 2: EIOS Compiler & Kernel execution DAG
    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag(
        goal="Deploy Multi-Agent Free Energy Minimization in production",
        target_budget_usd=15000
    )
    assert len(dag.nodes) == 4

    kernel = EIOSKernel()
    success = await kernel.execute_dag(dag)
    assert success is True

    # Layer 2: EOS Engine continuous sensing and venture allocation
    eos = EOSEngine()
    vcell = VentureCell(
        cell_id=uuid4(),
        name="Cognitive OS Venture",
        namespace="cognitive_os_ns",
        allocated_capital_cents=50000_00,
        expected_free_energy=0.85
    )
    sensing_res = eos.run_continuous_sensing_cycle([vcell], total_budget_cents=100000_00)
    assert sensing_res["world_state"]["market_demand_index"] > 0
    assert vcell.cell_id in sensing_res["allocated_budgets"]

    # Layer 3: AEAN Learnable Routing Gates & HiveMind Token Arbitration
    hive = HiveMind(token_budget=100)
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=100.0)
    agent = SpecializedAgentProfile(
        agent_id="agent_cognitive_aean",
        domain_specialty="Cognitive Execution",
        cost_per_token=0.002,
        historical_success_rate=0.92
    )
    dispatcher.register_subagent(agent)
    routed_agent_id = dispatcher.route_task(task_complexity=100, domain="Cognitive Execution")
    assert routed_agent_id == "agent_cognitive_aean"

    # Layer 4: APODEX WorldModel
    wm = WorldModel()

    # Bridge Handoff across all 4 layers
    bridge = ResearchToSystemBridge()
    record = bridge.handoff_validated_hypothesis(
        hypothesis=hyp,
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    # Verify complete 4-layer integration handoff
    assert record["hypothesis_id"] == str(hyp.hypothesis_id)
    assert record["layer1_research_os"] == "VALIDATED"
    assert record["layer2_eios"] == "ACTIVE_INFERENCE_READY"
    assert record["layer2_eos"] == "PROMOTED_TO_EOS_ENGINE"
    assert "HIVEMIND_BID_ARBITRATED_GRANTED" in record["layer3_aean"]
    assert record["layer4_world_model"] == "CAUSAL_NODE_AND_BELIEF_UPDATED"
