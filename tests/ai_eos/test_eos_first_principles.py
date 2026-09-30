"""Unit and integration tests for EOSEngineFirstPrinciples.

Validates all 11 sections of the Entrepreneurial Operating System specification.
"""

import pytest
from apodex.ai_eos.intelligence import (
    EOSEngineFirstPrinciples,
    MasterLoopNode,
    LoopTimescale,
    DecisionRiskType,
    ExternalBusinessLoopType,
    JourneyStage,
    GTMDistributionMotion,
    GrowthStage,
    MoatType,
    CheapTestResult,
)


def test_eos_master_loop_and_velocity():
    engine = EOSEngineFirstPrinciples()
    assert engine.current_master_node == MasterLoopNode.ENVIRONMENTAL_SENSING

    # Transition with re-entry kill signal
    next_node = engine.transition_master_node(
        MasterLoopNode.CUSTOMER_VALIDATION, re_entry_signal="kill_signal"
    )
    assert next_node == MasterLoopNode.OPPORTUNITY_DISCOVERY

    # Calculate loop velocity
    velocity = engine.calculate_loop_velocity({
        LoopTimescale.FAST: 3.5,
        LoopTimescale.MEDIUM: 30.0,
        LoopTimescale.SLOW: 180.0
    })
    assert velocity["fast_loop_days"] == 3.5
    assert velocity["composite_velocity_score"] > 0.0


def test_cognitive_loops_anomaly_and_bayes():
    engine = EOSEngineFirstPrinciples()

    # Anomaly detection
    anomaly = engine.detect_anomaly("Unexpected traffic surge", 1000.0, 100.0)
    assert anomaly.structural_shift_probability > 0.5

    # Forced hypothesis generation
    hyp = engine.form_falsifiable_hypothesis(
        claim="Streaming becomes viable if broadband > 50%",
        enabling_condition="broadband_penetration",
        metric="churn_rate",
        threshold=0.2,
        prior=0.4,
        risk_type=DecisionRiskType.TYPE_II
    )
    assert hyp.id in engine.active_hypotheses

    # Bayesian update with strong confirmation test
    test_result = CheapTestResult(
        hypothesis_id=hyp.id,
        test_cost=500.0,
        evidence_score=0.9,
        sample_size=1000,
        execution_days=5.0
    )
    updated_hyp = engine.update_bayesian_belief(test_result)
    assert updated_hyp.current_belief_probability > 0.4
    assert updated_hyp.status in ("active", "strengthened")


def test_mental_model_ossification():
    engine = EOSEngineFirstPrinciples()

    # Update mental model with structural failures
    model = engine.update_mental_model("market_model", prediction_accurate=False, structural_failure=True)
    assert model.consecutive_failures == 1
    assert model.ossification_score == 0.3

    model = engine.update_mental_model("market_model", prediction_accurate=False, structural_failure=True)
    assert model.ossification_score == 0.6


def test_business_loops_and_leverage():
    engine = EOSEngineFirstPrinciples()
    assert len(engine.business_loops) == 13

    eval_results = engine.evaluate_business_loops({
        ExternalBusinessLoopType.PRICING: {"arpu": 150.0, "realization": 0.9},
        ExternalBusinessLoopType.HIRING: {"time_to_fill": 20.0, "quality": 0.85}
    })
    assert eval_results[ExternalBusinessLoopType.PRICING].is_healthy

    leverage_loops = engine.calculate_high_leverage_loops()
    assert ExternalBusinessLoopType.PRICING in leverage_loops
    assert ExternalBusinessLoopType.HIRING in leverage_loops


def test_customer_journey_lifecycle():
    engine = EOSEngineFirstPrinciples()
    journey = engine.evaluate_customer_journey({
        JourneyStage.AWARENESS: 0.8,
        JourneyStage.PURCHASE: 0.15,
        JourneyStage.RETENTION: 0.65
    })
    assert len(journey) == 15
    purchase_stage = next(s for s in journey if s.stage == JourneyStage.PURCHASE)
    assert purchase_stage.common_mistake_flagged is True
    assert purchase_stage.optimization_lever == "Remove steps"


def test_gtm_system_configuration():
    engine = EOSEngineFirstPrinciples()
    gtm_config = engine.configure_gtm_system(
        positioning="All-in-one cognitive OS for enterprises",
        comparison_axis="Automated decision vs manual analysis",
        segment="Enterprise AI teams",
        pricing_model="Usage-based + seat tier",
        primary_motion=GTMDistributionMotion.PLG,
        secondary_motions=[GTMDistributionMotion.SLG]
    )
    assert gtm_config.compounding_motion_score == 0.95


def test_growth_stage_and_premature_scaling():
    engine = EOSEngineFirstPrinciples()

    # Test premature scaling detection
    growth_status = engine.evaluate_growth_stage({
        "retention_flattening": 0.2,
        "growth_rate": 1.5,
        "cac_payback_months": 18.0
    })
    assert growth_status.premature_scaling_risk == 0.9

    # Test healthy growth transition
    healthy_status = engine.evaluate_growth_stage({
        "retention_flattening": 0.85,
        "nrr": 1.25,
        "cac_payback_months": 8.0,
        "growth_rate": 0.8
    })
    assert healthy_status.current_stage == GrowthStage.GROWTH
    assert healthy_status.premature_scaling_risk == 0.1


def test_technology_cost_curves_and_moats():
    engine = EOSEngineFirstPrinciples()

    curve = engine.track_technology_cost_curve("compute_cost", [100.0, 50.0, 20.0, 8.0], viability_threshold=10.0)
    assert curve.is_viability_crossed is True

    moat = engine.evaluate_moat_strength(MoatType.NETWORK_EFFECTS, score=0.9, durability=5.0, copy_cost=1000000.0)
    assert moat.strength_score == 0.9


def test_failure_mode_diagnostics():
    engine = EOSEngineFirstPrinciples()

    failures = engine.diagnose_failure_modes({
        "survey_satisfaction": 0.9,
        "active_usage": 0.1,  # Solving wrong problem
        "build_velocity": 0.95,
        "demand_signal": 0.05,  # Building before validating
    })
    detected_names = [f.failure_mode for f in failures]
    assert "Solving the wrong problem" in detected_names
    assert "Building before validating" in detected_names


def test_decision_tree_evaluator():
    engine = EOSEngineFirstPrinciples()

    # Test Noise -> Discard
    res = engine.evaluate_pursuit_decision_tree(
        is_structural_anomaly=False,
        is_reversible_decision=True,
        high_confidence_multi_source=False,
        cheap_test_available=True,
        test_exceeds_kill_threshold=None,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res.decision == "Discard"

    # Test Commit Resources
    res_commit = engine.evaluate_pursuit_decision_tree(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_commit.decision == "Commit Resources"
    assert res_commit.is_pursued is True


def test_kpi_stack_rollup():
    engine = EOSEngineFirstPrinciples()

    hyp1 = engine.form_falsifiable_hypothesis("Claim 1", "Condition 1", "metric", 0.2)
    engine.form_falsifiable_hypothesis("Claim 2", "Condition 2", "metric", 0.2)

    # Falsify hyp1
    hyp1.status = "falsified"

    kpis = engine.rollup_kpi_stack()
    assert kpis["sensing_signal_fidelity"] == 0.85
    assert kpis["validation_falsification_rate"] == 0.5
