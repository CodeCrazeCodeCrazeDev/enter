"""
Unit tests for the 14-Layer Computational Architecture Engine.
"""

from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence import (
    FourteenLayerEngine,
    WorldStateSignal,
    Layer1RealitySubstrate,
    Layer2OpportunityDiscovery,
    Layer3ProblemDiscovery,
    Layer4DecisionEngine,
    Layer5OpportunityEvaluation,
    Layer6ProductCreation,
    Layer7CustomerUnderstanding,
    Layer8Marketing,
    Layer9SalesEngine,
    Layer10GrowthEngine,
    Layer11CompetitionEngine,
    Layer12OrganizationalDesign,
    Layer13MetaLearning,
    Layer14AIEntrepreneurshipOrchestrator
)


def test_layer1_reality_substrate() -> None:
    l1 = Layer1RealitySubstrate()
    class_res = l1.classify_task("pricing_elasticity")
    assert class_res["category"] == "optimization"
    assert class_res["can_be_automated"] is True

    human_res = l1.classify_task("mission_vision")
    assert human_res["category"] == "human_judgment"
    assert human_res["can_be_automated"] is False

    inv_res = l1.evaluate_invariant_principles(capital_cents=50000_00, hypothesis_velocity=4.0)
    assert inv_res["ruin_probability"] == 0.0
    assert inv_res["survival_score"] == 1.0


def test_layer2_hawkes_intensity_and_discovery() -> None:
    l2 = Layer2OpportunityDiscovery()
    timestamps = [10.0, 10.5, 11.0, 11.2, 11.3]
    intensity = l2.calculate_hawkes_intensity(timestamps, baseline_mu=0.1)
    assert intensity > 0.1

    sig = WorldStateSignal(
        title="Autonomous Biotech Synthesis Platform",
        domain="synthetic_biology",
        entropy=1.2,
        event_timestamps=timestamps,
        tam_cents=200_000_000
    )
    opps = l2.process_signals([sig])
    assert len(opps) == 1
    assert opps[0].title == "Autonomous Biotech Synthesis Platform"
    assert opps[0].hawkes_intensity == intensity


def test_layer3_to_layer5_pipeline() -> None:
    l2 = Layer2OpportunityDiscovery()
    l3 = Layer3ProblemDiscovery()
    l4 = Layer4DecisionEngine(curiosity_weight=1.5)
    l5 = Layer5OpportunityEvaluation()

    sig = WorldStateSignal(
        title="Quantum Compute Compiler Optimization",
        domain="quantum_software",
        entropy=1.8,
        event_timestamps=[1.0, 2.0, 2.5],
        tam_cents=500_000_000  # $5M TAM
    )
    opp = l2.process_signals([sig])[0]
    problem = l3.analyze_root_cause(opp)
    evaluated = l5.evaluate_opportunity(opp, problem)
    decision = l4.make_decision(opp, evaluated)

    assert problem.root_cause_variable in opp.variables
    assert isinstance(evaluated.expected_value_cents, int)
    assert evaluated.expected_value_cents > 0
    assert decision.expected_free_energy < 0.0 or decision.should_kill is False


def test_full_14_layer_engine_execution() -> None:
    engine = FourteenLayerEngine()
    signal_data = {
        "title": "Decentralized AI Agent Infrastructure",
        "domain": "ai_agents",
        "entropy": 1.4,
        "event_timestamps": [100.0, 101.2, 101.8, 102.0],
        "variables": ["compute_cost", "latency", "user_retention"],
        "causal_edges": [("compute_cost", "latency"), ("latency", "user_retention")],
        "coefficients": {"compute_cost->latency": 0.8, "latency->user_retention": -1.5},
        "tam_cents": 500_000_000
    }

    result = engine.process_world_signal(signal_data)

    assert result["status"] == "EXECUTED"
    assert result["primary_opportunity"] == "Decentralized AI Agent Infrastructure"
    assert "expected_free_energy" in result["decision"]
    assert result["product_mvl"]["core_job_to_be_done"] != ""
    assert result["marketing_r0"] > 0.0
    assert result["sales_acv_cents"] == 12000_00
    assert result["growth_nrr"] == 1.25
    assert result["org_hiring_triggered"] is True


def test_14_layer_kill_criteria() -> None:
    l14 = Layer14AIEntrepreneurshipOrchestrator()
    # Signal with low success probability (should terminate)
    sig = WorldStateSignal(
        title="Impossible Energy Generator",
        domain="fringe_physics",
        entropy=5.0,
        event_timestamps=[1.0]
    )
    # Force low probability
    opps = l14.l2_discovery.process_signals([sig])
    opps[0].success_probability = 0.05

    prob = l14.l3_problem.analyze_root_cause(opps[0])
    eval_opp = l14.l5_evaluation.evaluate_opportunity(opps[0], prob)
    decision = l14.l4_decision.make_decision(opps[0], eval_opp)

    assert decision.should_kill is True
