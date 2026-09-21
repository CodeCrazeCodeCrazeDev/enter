"""End-to-End integration test suite for the Unified Cognitive Operating System.

Validates joint multi-layer active inference execution across:
- Layer 1: Research OS (Research & Hypothesis Generation)
- Layer 2: EIOS Kernel & EOS Engine (Active Inference Sensing, Business Engine & DAG Orchestration)
- Layer 3: AEAN HiveMind (Multi-Agent Token Bidding & Execution)
- Layer 4: APODEX WorldModel (Causal Graphs & Recursive Bayesian Belief Updates)
"""

from __future__ import annotations

import pytest
from uuid import uuid4
from datetime import datetime, timezone

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind, TaskBid
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge
from apodex.world_model.domain.beliefs import Belief


@pytest.mark.asyncio
async def test_end_to_end_unified_cognitive_os_workflow():
    # -------------------------------------------------------------------------
    # Layer 1: Research OS Hypothesis Validation & Registration
    # -------------------------------------------------------------------------
    research_os = ResearchOS()

    hyp = research_os.register_hypothesis(
        title="Active Inference Decision Acceleration",
        description="Autonomous active inference agents reduce decision latency under high uncertainty",
        null_hypothesis="Active inference does not affect decision latency",
        target_metric="market_sensing",
        significance_alpha=0.05,
    )
    assert hyp is not None
    hyp_id_str = str(hyp.hypothesis_id)

    # Simulate experiment execution to validate hypothesis
    exp = research_os.create_experiment(hyp.hypothesis_id, seed=42)
    completed_exp = research_os.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)
    assert completed_exp.status == "completed"

    # -------------------------------------------------------------------------
    # Layer 2: EIOS Kernel Sensing & EOS Engine State Ingestion
    # -------------------------------------------------------------------------
    eios_kernel = EIOSKernel()
    eios_kernel.register_research_hypothesis(
        hypothesis_id=hyp_id_str,
        domain="market_sensing",
        efe_delta=0.85,
    )

    anomalies = eios_kernel.sense_opportunity_anomalies(budget=10.0)
    assert len(anomalies) > 0
    assert anomalies[0]["hypothesis_id"] == hyp_id_str

    eos_engine = EOSEngine()
    eos_engine.ingest_validated_research(
        hypothesis_id=hyp_id_str,
        insight_summary=hyp.description,
        effect_size=0.85,
    )
    assert hyp_id_str in eos_engine.active_hypotheses

    # -------------------------------------------------------------------------
    # Layer 3: AEAN HiveMind Auction-Based Token Bidding Execution
    # -------------------------------------------------------------------------
    hive_mind = HiveMind(token_budget=100)

    bids = [
        TaskBid(task="active_inference_routing", priority=0.9, expected_value=1.5, token_cost=30),
        TaskBid(task="market_anomaly_sensing", priority=0.7, expected_value=1.1, token_cost=20),
        TaskBid(task="causal_graph_rebalancing", priority=0.8, expected_value=1.3, token_cost=25),
    ]

    grants = hive_mind.arbitrate(bids)
    assert len(grants) == 3
    assert grants[0].granted is True
    assert grants[0].task == "active_inference_routing"

    # -------------------------------------------------------------------------
    # Layer 4: APODEX WorldModel Causal Nodes & Recursive Bayesian Belief Updates
    # -------------------------------------------------------------------------
    world_model = WorldModel()

    node_cause = CausalNode(
        node_id="active_inference_agent",
        node_type="agent",
        properties={"label": "Active Inference Agent Deployment", "status": "active", "granted_task": grants[0].task},
    )
    node_effect = CausalNode(
        node_id="decision_latency",
        node_type="metric",
        properties={"label": "Decision Latency Reduction", "latency_ms": 120},
    )
    edge = RelationEdge(
        source_id="active_inference_agent",
        target_id="decision_latency",
        relation_type="reduces",
        weight=0.85,
    )

    world_model.add_node(node_cause)
    world_model.add_node(node_effect)
    world_model.add_relation(edge)

    assert "active_inference_agent" in world_model.nodes
    assert "decision_latency" in world_model.nodes
    assert len(world_model.edges) == 1

    # Perform recursive Bayesian belief update based on real-world tool observation
    belief = Belief(
        target_id=uuid4(),
        probability=0.5,
        evidence=["empirical_simulation_outcome_01"],
    )
    belief.update_confidence(likelihood=0.85, prior_probability=0.5)
    assert belief.probability > 0.5
