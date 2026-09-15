"""Unit and Integration tests for the First-Principles Entrepreneurial Operating System (EOS) Engine."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSState,
    EOSStateMachine,
    OpportunityDecisionTree,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleStage,
    CustomerLifecycleEngine,
    GTMSystemEngine,
    GrowthStage,
    GrowthStageClassifier,
    StrategicMoatEngine,
    FailureModeMonitor,
    FirstPrinciplesEOSEngine,
)


def test_eos_state_machine_valid_transitions():
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    st = sm.transition_to(EOSState.HYPOTHESIS, "Anomaly detected")
    assert st == EOSState.HYPOTHESIS

    st = sm.transition_to(EOSState.CHEAP_TEST, "Cheap test started")
    assert st == EOSState.CHEAP_TEST

    st = sm.transition_to(EOSState.VALIDATION, "Cheap test passed")
    assert st == EOSState.VALIDATION


def test_eos_state_machine_invalid_transition():
    sm = EOSStateMachine()
    with pytest.raises(ValueError, match="Invalid transition"):
        sm.transition_to(EOSState.SCALE, "Direct to scale from sensing should fail")


def test_opportunity_decision_tree_noise_signal():
    dt = OpportunityDecisionTree()
    res = dt.evaluate(
        is_structural_anomaly=False,
        is_reversible=True,
        high_confidence_signals=False,
        cheap_test_available=True,
    )
    assert res.decision == "DISCARD"
    assert "Noise signal" in res.path[0]


def test_opportunity_decision_tree_commit_resources():
    dt = OpportunityDecisionTree()
    res = dt.evaluate(
        is_structural_anomaly=True,
        is_reversible=True,
        high_confidence_signals=True,
        cheap_test_available=True,
        cheap_test_passed=True,
        expected_value_positive=True,
        structural_advantage=True,
    )
    assert res.decision == "COMMIT_RESOURCES"
    assert res.risk_type == "Type_II"
    assert res.confidence_score == 0.9


def test_coupled_business_loops_engine():
    engine = CoupledBusinessLoopsEngine()
    metrics = {
        "retention_rate": 0.65,
        "nps": 55.0,
        "cac_cents": 4000,
        "conversion_rate": 0.04,
        "win_rate": 0.30,
        "acv_cents": 150000,
        "nrr": 1.15,
        "churn_rate": 0.015,
        "price_elasticity": -0.4,
        "arpu_cents": 12000,
        "k_factor": 0.9,
        "decision_latency_sec": 10.0,
        "burn_multiple": 1.2,
        "runway_months": 24.0,
        "gross_margin": 0.80,
        "time_to_fill_days": 25.0,
        "enps": 60.0,
        "experiments_run": 15.0,
        "experiment_hit_rate": 0.25,
        "feature_parity_gap": 0.10,
        "monthly_revenue_cents": 600000,
        "monthly_burn_cents": 350000,
        "new_data_points": 100,
    }
    loops = engine.update_loops(metrics)
    assert len(loops) == 13
    assert engine.stocks.cash_cents > 10_000_000
    assert engine.stocks.brand_trust_score > 0.50
    assert not loops["Financial"].failure_flag


def test_customer_lifecycle_engine():
    engine = CustomerLifecycleEngine()
    volumes = {
        "Awareness": 10000,
        "Interest": 2000,
        "Consideration": 1000,
        "Evaluation": 500,
        "Purchase": 200,
        "Onboarding": 180,
        "Activation": 150,
        "Engagement": 120,
        "Habit Formation": 100,
        "Retention": 90,
        "Loyalty": 80,
        "Advocacy": 60,
        "Referral": 40,
        "Expansion": 30,
        "Repurchase": 25,
    }
    convs = engine.update_lifecycle(volumes)
    assert len(convs) == 14
    assert convs["Awareness->Interest"] == 0.20
    bottleneck, rate = engine.identify_bottleneck_stage()
    assert bottleneck is not None


def test_gtm_system_engine():
    gtm = GTMSystemEngine()
    rec = gtm.evaluate_motion(acv_cents=150_000_00, complexity="high", has_community=True)
    assert rec["primary_motion"] == "Sales-Led Growth (SLG / Enterprise)"
    assert "Community-Led Growth (CLG)" in rec["secondary_motions"]


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()
    stage_info = classifier.classify({
        "paying_customers": 15,
        "retention_curve_flattened": True,
        "arr_cents": 2_500_000_00,
    })
    assert stage_info.stage == GrowthStage.GROWTH
    assert stage_info.binding_constraint == "Hiring velocity, systems"


def test_strategic_moat_engine():
    moat = StrategicMoatEngine()
    res = moat.score_moats(
        network_effects_score=0.8,
        switching_costs_cents=12000_00,
        scale_economies_score=0.7,
        brand_trust_score=0.9,
        counter_positioning_score=0.85,
        cornered_resources_score=0.8,
        process_power_score=0.8,
    )
    assert res["composite_moat_durability_score"] > 0.70
    assert res["dominant_moat_source"] in [
        "Network Effects",
        "Switching Costs",
        "Brand Trust",
        "Counter-Positioning",
        "Cornered Resources",
        "Process Power",
    ]


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()
    alerts = monitor.audit({
        "retention_curve_flattened": False,
        "growth_rate": 0.40,
        "burn_multiple": 3.5,
    })
    assert len(alerts) >= 2
    assert any(a.failure_mode == "Lack of product-market fit" for a in alerts)
    assert any(a.failure_mode == "Capital misallocation" for a in alerts)


def test_first_principles_eos_engine_master_cycle():
    master = FirstPrinciplesEOSEngine()
    opp_inputs = {
        "is_structural_anomaly": True,
        "is_reversible": True,
        "high_confidence_signals": True,
        "cheap_test_available": True,
        "cheap_test_passed": True,
        "expected_value_positive": True,
        "structural_advantage": True,
    }
    ops_metrics = {
        "paying_customers": 20,
        "retention_curve_flattened": True,
        "arr_cents": 1_500_000_00,
        "acv_cents": 120000,
        "retention_rate": 0.70,
        "nps": 45.0,
        "growth_rate": 0.15,
    }

    report = master.run_cycle(opp_inputs, ops_metrics)
    assert report["current_eos_state"] == EOSState.OPERATE.value
    assert report["decision_tree_result"]["decision"] == "COMMIT_RESOURCES"
    assert "Product" in report["business_loops_summary"]
    assert report["growth_stage"]["stage"] == GrowthStage.GROWTH.value
