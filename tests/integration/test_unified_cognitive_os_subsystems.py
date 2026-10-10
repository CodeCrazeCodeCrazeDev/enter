"""Integration tests for Unified Cognitive Operating System subsystems.

Validates closed-loop interactions across:
1. Research OS hypothesis validation and literature principle querying
2. EIOS Kernel DAG execution and EFE anomaly sensing
3. EOS Engine continuous sensing and research ingestion
4. AEAN HiveMind token arbitration and task bidding
5. APODEX WorldModel causal graph and Bayesian belief updates
6. ResearchToSystemBridge cross-layer state handoffs
"""

import pytest
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import register_300_paper_corpus_principles, ResearchToSystemBridge
from apodex.arcs.kernel.kernel import EIOSKernel, EntrepreneurialCompiler
from apodex.ai_eos.intelligence import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel


def test_research_os_corpus_principles_and_export():
    principles = register_300_paper_corpus_principles()
    assert len(principles) >= 4

    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Active Inference Optimization",
        description="Active inference minimizes expected free energy",
        null_hypothesis="Confidence <= 0.5",
        target_metric="EFE_reduction"
    )

    review = ros.conduct_literature_review("Active Inference")
    assert review["reviewed_citations_count"] >= 14
    assert len(review["relevant_corpus_principles"]) >= 1

    hyp.status = "validated"
    exported = ros.export_validated_hypotheses()
    assert len(exported) == 1
    assert exported[0].hypothesis_id == hyp.hypothesis_id


def test_eios_kernel_dag_execution_and_sensing():
    kernel = EIOSKernel()
    compiler = EntrepreneurialCompiler()

    dag = compiler.compile_goal_to_dag(goal="Validate AI Entrepreneurship Platform", target_budget_usd=10000)
    assert len(dag.nodes) == 4

    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="High Confidence Market Signal",
        description="Market demand index > 1.2",
        null_hypothesis="Demand <= 1.0",
        target_metric="demand_index"
    )
    hyp.posterior_confidence = 0.92

    kernel.register_research_hypothesis(hyp)
    anomalies = kernel.sense_opportunity_anomalies()
    assert len(anomalies) == 1
    assert anomalies[0]["anomaly_type"] == "HIGH_CONFIDENCE_PROMOTION"


def test_eos_engine_research_ingestion_and_sensing():
    eos = EOSEngine()
    ros = ResearchOS()

    hyp = ros.register_hypothesis(
        title="Unit Economics Scaling",
        description="LTV:CAC ratio exceeds 3.0",
        null_hypothesis="Ratio <= 2.0",
        target_metric="ltv_to_cac"
    )

    eos.ingest_validated_research(hyp)
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0].title == "Unit Economics Scaling"


def test_aean_hive_mind_token_bidding_and_arbitration():
    hive = HiveMind(token_budget=20)

    bid1 = hive.register_research_insight("Market Sensing Strategy", priority=0.9, expected_value=0.9, token_cost=10)
    bid2 = TaskBid(task="low_priority_task", priority=0.2, expected_value=0.3, token_cost=15)

    grants = hive.arbitrate([bid1, bid2])
    granted_map = hive.granted_tasks(grants)

    assert granted_map[bid1.task] is True
    assert granted_map[bid2.task] is False


def test_apodex_world_model_graph_and_belief_updates():
    wm = WorldModel()

    node = wm.create_node(node_id="venture_node_1", node_type="venture", properties={"name": "Apodex Venture"})
    assert node.node_id == "venture_node_1"

    edge = wm.add_edge(source_id="venture_node_1", target_id="market_node_1", relation_type="targets", weight=0.85)
    assert edge.relation_type == "targets"

    belief = wm.update_belief("venture_node_1", confidence=0.88, evidence_count=2)
    assert belief["confidence"] == 0.88
    assert belief["evidence_count"] == 2


def test_research_to_system_bridge_end_to_end_handoff():
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind(token_budget=50)
    wm = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eios_kernel=kernel,
        eos_engine=eos,
        hive_mind=hive,
        world_model=wm
    )

    hyp = ros.register_hypothesis(
        title="Cross-Layer active inference state handoff",
        description="Handoff active hypotheses to kernel, engine, hive, and world model",
        null_hypothesis="No effect",
        target_metric="handoff_rate"
    )

    handoff_results = bridge.bridge_hypothesis(hyp.hypothesis_id)
    assert len(handoff_results["transferred_subsystems"]) == 4
    assert "EOS Engine" in handoff_results["transferred_subsystems"]
    assert "EIOS Kernel" in handoff_results["transferred_subsystems"]
    assert "AEAN HiveMind" in handoff_results["transferred_subsystems"]
    assert "APODEX WorldModel" in handoff_results["transferred_subsystems"]
