# -*- coding: utf-8 -*-
"""
test_unified_5layer_integration.py: Comprehensive end-to-end integration test suite
validating joint cross-layer workflows across:
- Layer 1: Research OS (hypothesis generation, power analysis, statistical validation)
- Layer 2: EIOS Kernel & EOS Engine (Active Inference sensing & First-Principles EOS engine)
- Layer 3: AEAN HiveMind (token bidding, agent routing, sycophancy-free debate)
- Layer 4: APODEX WorldModel & Cognitive Brain (causal SCM, Monte Carlo simulation, memory consolidation)
- Bridge: ResearchToSystemBridge (cross-layer state handoff orchestration)
"""

from __future__ import annotations
import pytest
from uuid import UUID

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import FirstPrinciplesEOSEngine
from apodex.ai_eos.research.integration import (
    ResearchToSystemBridge,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
)
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.cognition.brain import CognitiveBrain, DeepCausalWorldModel, SimulationEngine


def test_layer1_research_os_scientific_pipeline() -> None:
    """Validates Layer 1 Research OS hypothesis generation, power design, and statistical simulation."""
    ros = ResearchOS()

    # 1. Register hypothesis
    hyp = ros.register_hypothesis(
        title="Active Inference EFE Optimization",
        description="Minimizing EFE reduces agent response latency by >15%.",
        null_hypothesis="Latency reduction <= 0%",
        target_metric="latency_reduction_pct",
        significance_alpha=0.05
    )
    assert hyp.status == "registered"

    # 2. Formulate experiment design
    design = ros.design_experiment(hyp.hypothesis_id)
    assert design["recommended_sample_size"] > 0
    assert design["statistical_power"] == 0.80

    # 3. Create sandbox experiment & run walk-forward simulation
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    exp_res = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=3.2)

    assert exp_res.is_statistically_significant is True
    assert exp_res.p_value < 0.05
    assert exp_res.effect_size > 0.0
    assert exp_res.deflated_sharpe_ratio > 0.0

    # Refetch hypothesis and verify promotion
    hyp_updated = ros.hypotheses.get(hyp.hypothesis_id)
    assert hyp_updated.status == "validated"


def test_layer2_eos_engine_opportunity_and_research_ingestion() -> None:
    """Validates Layer 2 EOS Engine research ingestion and continuous opportunity scoring."""
    eos = FirstPrinciplesEOSEngine()

    research_payload = {
        "hypothesis_id": "hyp_99",
        "title": "Automated AST Code Mutation",
        "priority_score": 88.5,
        "status": "validated"
    }

    eos.ingest_validated_research(research_payload)
    assert len(eos.active_hypotheses) == 1
    assert eos.active_hypotheses[0]["title"] == "Automated AST Code Mutation"


def test_layer3_aean_hivemind_token_bidding() -> None:
    """Validates Layer 3 AEAN HiveMind research insight registration and token bidding registry."""
    hive = HiveMind()

    hive.register_research_insight(
        title="High-Yield Active Inference Routing",
        priority_score=92.0,
        effect_size=3.5
    )

    insights = getattr(hive, "research_insights", [])
    assert len(insights) == 1
    assert insights[0]["title"] == "High-Yield Active Inference Routing"


def test_layer4_apodex_cognitive_brain_cycle() -> None:
    """Validates Layer 4 APODEX CognitiveBrain unified cycle across planning, WorldModel, and memory."""
    brain = CognitiveBrain()

    # Run unified strategic cycle
    report = brain.run_strategic_cycle("Scale Autonomous AI Orchestration")

    assert report["plan_length"] == 4
    assert "mean" in report["sim_results"]
    assert report["consensus_score"] > 0.0
    assert report["claim_verified"] is True
    assert isinstance(report["fact_id"], str)


def test_cross_layer_research_to_system_bridge() -> None:
    """Validates full 5-layer state handoff orchestration via ResearchToSystemBridge."""
    ros = ResearchOS()
    eos = FirstPrinciplesEOSEngine()
    hive = HiveMind()
    world_model = DeepCausalWorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eos_engine=eos,
        hive_mind=hive,
        world_model=world_model
    )

    result = bridge.orchestrate_validated_hypothesis_handoff(
        title="Adaptive EFE Task Delegation",
        description="EFE-driven routing decreases sub-agent token overhead.",
        target_metric="token_efficiency",
        ground_truth_yield=2.8,
        commercial_value=150_000.0
    )

    assert result["hypothesis_status"] == "validated"
    assert result["is_significant"] is True
    assert result["priority_score"] > 0.0
    assert result["eos_promoted"] is True
    assert result["hive_registered"] is True
    assert result["world_updated"] is True

    # Verify WorldModel updated
    assert "token_efficiency" in world_model.variables
    assert "token_efficiency" in world_model.beliefs_alpha
