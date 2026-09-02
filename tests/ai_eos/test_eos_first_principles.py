"""Unit and integration tests for first-principles EOS Engine implementation."""

from __future__ import annotations
import pytest

from apodex.ai_eos.intelligence import (
    EOSMasterLoopState,
    EOSStateMachine,
    OpportunityDecisionTree,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GrowthStageClassifier,
    MoatAnalyzer,
    FailureModeMonitor,
    FirstPrinciplesEOSEngine,
)


def test_eos_state_machine_transitions():
    sm = EOSStateMachine()
    assert sm.current_state == EOSMasterLoopState.SENSING

    # Transition sensing -> hypothesis
    s1 = sm.process_signal(anomaly_detected=True, test_passed=False, economic_viable=False, scale_signal=False)
    assert s1 == EOSMasterLoopState.HYPOTHESIS

    # Transition hypothesis -> cheap test
    s2 = sm.process_signal(anomaly_detected=False, test_passed=False, economic_viable=False, scale_signal=False)
    assert s2 == EOSMasterLoopState.CHEAP_TEST

    # Falsified cheap test -> discard
    s3 = sm.process_signal(anomaly_detected=False, test_passed=False, economic_viable=False, scale_signal=False)
    assert s3 == EOSMasterLoopState.DISCARD

    # Discard -> re-entrant sensing
    s4 = sm.process_signal(anomaly_detected=False, test_passed=False, economic_viable=False, scale_signal=False)
    assert s4 == EOSMasterLoopState.SENSING


def test_opportunity_decision_tree():
    tree = OpportunityDecisionTree()

    # Noise -> Discard
    res_noise = tree.evaluate(
        is_structural_anomaly=False,
        is_reversible_decision=True,
        high_confidence_multi_source=False,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_noise["decision"] == "Discard"

    # Type I irreversible risk without high confidence signal -> Discard
    res_irreversible = tree.evaluate(
        is_structural_anomaly=True,
        is_reversible_decision=False,
        high_confidence_multi_source=False,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_irreversible["decision"] == "Discard"

    # Valid cheap test and moat -> Commit
    res_commit = tree.evaluate(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_multi_source=False,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_commit["decision"] == "Commit resources"
    assert res_commit["commit"] is True


def test_coupled_business_loops():
    engine = CoupledBusinessLoopsEngine()
    metrics = {
        "Product": {"retention_curve_slope": 0.2, "nps": 60},
        "Pricing": {"arpu_cents": 10000, "price_realization": 0.9},
        "Financial": {"burn_multiple": 1.2, "gross_margin": 0.8},
        "Hiring": {"time_to_fill_days": 30}
    }
    res = engine.evaluate_loops(metrics)
    assert "loop_health_scores" in res
    assert len(res["loop_health_scores"]) == 13
    assert res["coupled_system_health"] > 0.0


def test_customer_lifecycle_engine():
    cle = CustomerLifecycleEngine()
    stage_conversions = {"Awareness": 0.5, "Purchase": 0.2, "Retention": 0.9}
    res = cle.evaluate_lifecycle_cohort(stage_conversions)
    assert res["primary_bottleneck_stage"] == "Purchase"
    assert res["primary_bottleneck_drop_rate"] == 0.8


def test_growth_stage_classifier():
    gsc = GrowthStageClassifier()
    res_pmf = gsc.classify_stage(
        paying_customers=100,
        retention_curve_flattened=True,
        monthly_growth_rate=0.05,
        rule_of_40=0.2,
        has_third_party_developers=False,
        ecosystem_gmv_cents=0
    )
    assert res_pmf["classified_stage"] == "Product-Market Fit"
    assert res_pmf["premature_scaling_risk"] is False

    res_premature = gsc.classify_stage(
        paying_customers=2000,
        retention_curve_flattened=False,
        monthly_growth_rate=0.20,
        rule_of_40=0.45,
        has_third_party_developers=False,
        ecosystem_gmv_cents=0
    )
    assert res_premature["premature_scaling_risk"] is True


def test_moat_analyzer():
    ma = MoatAnalyzer()
    res = ma.score_moats(
        network_effects_score=0.8,
        switching_costs_score=0.9,
        scale_economies_score=0.7,
        brand_equity_score=0.6,
        regulatory_ip_score=0.5,
        counter_positioning_score=0.9,
        cornered_resource_score=0.4
    )
    assert res["composite_moat_durability_index"] > 0.6
    assert res["dominant_moat_type"] in ["switching_costs", "counter_positioning"]


def test_failure_mode_monitor():
    fmm = FailureModeMonitor()
    warnings = fmm.audit_operating_metrics(
        survey_vs_usage_gap=0.5,
        build_velocity_high_demand_flat=True,
        sales_cycle_days=150.0,
        cac_rising_faster_than_ltv=True,
        retention_never_flattens=True,
        decision_latency_hours=72.0,
        precommitted_kill_criteria_ignored=True,
        underperforming_bets_funded=4
    )
    assert len(warnings) == 8


def test_first_principles_eos_engine_e2e():
    engine = FirstPrinciplesEOSEngine()
    telemetry = {
        "is_structural_anomaly": True,
        "is_reversible_decision": True,
        "anomaly_detected": True,
        "paying_customers": 500,
        "retention_curve_flattened": True,
        "monthly_growth_rate": 0.15
    }
    res = engine.run_cycle(telemetry)
    assert res["current_state"] == EOSMasterLoopState.HYPOTHESIS.value
    assert res["opportunity_decision"]["commit"] is True
    assert "business_loops" in res
    assert "customer_lifecycle" in res
    assert "growth_stage" in res
    assert "moat_durability" in res
