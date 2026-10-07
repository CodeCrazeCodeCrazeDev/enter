# -*- coding: utf-8 -*-
"""
test_unified_5layer_integration.py: Integration test suite for 5-layer unified cognitive operating system.
Validates Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, APODEX WorldModel, and ResearchToSystemBridge.
"""

import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_research_os_hypothesis_export():
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Hawkes Process Yield Boost",
        description="Non-Gaussian Hawkes self-exciting point processes enhance yield.",
        null_hypothesis="H0: Hawkes point process yield <= 0",
        target_metric="sharpe_ratio"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.0)

    exported = ros.export_validated_hypotheses()
    assert len(exported) == 1
    assert exported[0].hypothesis_id == hyp.hypothesis_id
    assert exported[0].status == "validated"


def test_eios_kernel_active_inference_sensing():
    kernel = EIOSKernel()
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="MAP-Elites Diversity Expansion",
        description="Island model MAP-Elites increases prompt genome diversity.",
        null_hypothesis="H0: Diversity increase <= 0",
        target_metric="fitness_score"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=456)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.8)

    dag = kernel.register_research_hypothesis(hyp)
    assert dag.id.startswith("dag_research_")
    assert len(dag.nodes) == 2

    anomalies = kernel.sense_opportunity_anomalies([hyp])
    assert len(anomalies) == 1
    assert anomalies[0]["hypothesis_title"] == "MAP-Elites Diversity Expansion"
    assert anomalies[0]["efe_score"] > 0


def test_eos_engine_research_ingestion():
    eos = EOSEngine()
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="DPO Preference Advantage Margin",
        description="Clipped trajectory advantage margins stabilize DPO policy gradients.",
        null_hypothesis="H0: Advantage margin <= 0",
        target_metric="policy_loss"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=789)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.0)

    eos.ingest_validated_research(hyp)
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0].title == "DPO Preference Advantage Margin"


def test_aean_hive_mind_insight_bidding():
    hive_mind = HiveMind(token_budget=50)
    insight = {
        "title": "Autonomous Agent Swarm Bidding",
        "priority": 0.95,
        "expected_value": 2.5,
        "token_cost": 15
    }
    bid = hive_mind.register_research_insight(insight)
    assert isinstance(bid, TaskBid)
    assert bid.task == "research_insight:Autonomous Agent Swarm Bidding"

    grants = hive_mind.arbitrate([bid])
    assert len(grants) == 1
    assert grants[0].granted is True
    assert grants[0].tokens == 15


def test_world_model_causal_nodes_and_beliefs():
    wm = WorldModel()
    node = wm.create_node(
        node_id="hyp-node-101",
        node_type="research_hypothesis",
        properties={"title": "Active Inference Free Energy Minimization"}
    )
    assert node.node_id == "hyp-node-101"
    assert node.node_type == "research_hypothesis"

    edge = wm.add_edge(
        source_id="hyp-node-101",
        target_id="system-capability-202",
        relation_type="improves_capability",
        weight=0.9
    )
    assert edge.source_id == "hyp-node-101"
    assert edge.target_id == "system-capability-202"

    belief = wm.update_belief(
        node_id="hyp-node-101",
        posterior_probability=0.92,
        evidence_keys=["trial_run_1", "trial_run_2"]
    )
    assert belief["node_id"] == "hyp-node-101"
    assert belief["posterior_probability"] == 0.92


def test_research_to_system_bridge_full_pipeline():
    bridge = ResearchToSystemBridge()
    result = bridge.execute_full_5layer_pipeline(
        title="Unified 5-Layer Cognitive OS Integration",
        description="Validates closed-loop active inference state handoffs across Research OS, EIOS, EOS, AEAN, and WorldModel.",
        null_hypothesis="H0: Cross-layer coordination performance <= baseline",
        target_metric="system_throughput",
        ground_truth_yield=3.5
    )

    assert result["pipeline_status"] == "success"
    assert result["hypothesis_validated"] is True
    assert result["eios"]["status"] == "handed_off_to_eios"
    assert result["eos"]["status"] == "ingested_into_eos"
    assert result["aean"]["grant_status"] is True
    assert result["world_model"]["status"] == "world_model_updated"
    assert result["world_model"]["belief"]["posterior_probability"] == 0.95
