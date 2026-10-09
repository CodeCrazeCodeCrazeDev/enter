"""End-to-End Integration Test Suite for Unified Cognitive Operating System.

Validates joint closed-loop interactions across Research OS, EIOS Kernel,
EOS Engine, AEAN HiveMind, and APODEX WorldModel via ResearchToSystemBridge.
"""

import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.ai_eos.domain.models import VentureCell


def test_research_os_hypothesis_validation_lifecycle():
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="High Beta Landing Page Personalization",
        description="Dynamic personalization increases CTR by >25%",
        null_hypothesis="Personalization has no effect on CTR",
        target_metric="CTR",
        significance_alpha=0.05
    )
    assert hyp.status == "registered"

    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert completed_exp.is_statistically_significant is True
    validated_hyps = ros.get_hypotheses_by_status(["validated"])
    assert len(validated_hyps) == 1
    assert validated_hyps[0].hypothesis_id == hyp.hypothesis_id


@pytest.mark.asyncio
async def test_e2e_cross_layer_system_bridge():
    # 1. Instantiate Layer Components
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive_mind = HiveMind(token_budget=100)
    world_model = WorldModel()

    # 2. Register and validate hypothesis in Research OS
    hyp = ros.register_hypothesis(
        title="Predictive Funnel Routing",
        description="Predictive routing reduces dropoff by 30%",
        null_hypothesis="Routing dropoff remains unchanged",
        target_metric="conversion_rate",
        significance_alpha=0.05
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=42)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)

    # 3. Perform Cross-Layer Bridge State Handoff
    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive_mind,
        world_model=world_model
    )
    bridge_results = bridge.bridge_validated_hypotheses()

    assert bridge_results["validated_count"] == 1
    assert len(bridge_results["eos_ingested_ids"]) == 1
    assert "Predictive Funnel Routing" in bridge_results["kernel_registered_titles"]
    assert len(bridge_results["hive_mind_bids"]) == 1
    assert len(bridge_results["world_model_nodes"]) == 1

    # 4. Verify EIOS Kernel active inference sensing and DAG execution
    anomalies = kernel.sense_opportunity_anomalies({"demand_index": 1.5, "volatility": 0.2})
    assert len(anomalies) == 1
    assert anomalies[0]["action_recommended"] == "deploy_gtm_experiment"

    compiler = EntrepreneurialCompiler()
    dag = compiler.compile_goal_to_dag("Deploy Predictive Funnel Routing GTM", target_budget_usd=10000)
    dag_success = await kernel.execute_dag(dag)
    assert dag_success is True

    # 5. Verify EOS Engine Continuous Sensing & Capital Allocation
    cells = [
        VentureCell(name="Funnel Venture Cell A", namespace="test_cell_a", uncertainty=0.3, risk=0.2),
        VentureCell(name="Funnel Venture Cell B", namespace="test_cell_b", uncertainty=0.6, risk=0.4),
    ]
    sensing_res = eos.run_continuous_sensing_cycle(cells, total_budget_cents=100000_00)
    assert "world_state" in sensing_res
    assert len(sensing_res["allocated_budgets"]) == 2

    # 6. Verify AEAN Hive Mind token arbitration
    additional_bid = TaskBid(task="monitor_funnel_telemetry", priority=0.9, expected_value=1.8, token_cost=20)
    insight_bid = TaskBid(task=bridge_results["hive_mind_bids"][0], priority=0.85, expected_value=1.5, token_cost=15)
    grants = hive_mind.arbitrate([additional_bid, insight_bid])

    granted_dict = hive_mind.granted_tasks(grants)
    assert granted_dict["monitor_funnel_telemetry"] is True
    assert granted_dict[bridge_results["hive_mind_bids"][0]] is True

    # 7. Verify World Model Causal Nodes and Belief state updates
    node_id = bridge_results["world_model_nodes"][0]
    assert node_id in world_model.nodes
    belief_key = f"belief_{node_id}"
    assert belief_key in world_model.beliefs
    assert world_model.beliefs[belief_key]["confidence"] == 0.85
