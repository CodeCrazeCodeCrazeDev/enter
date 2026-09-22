"""Comprehensive unit and integration tests for First-Principles Entrepreneurial Operating System (EOS).

Validates all 11 sections of the First-Principles EOS model, including state transitions,
decision tree evaluation, coupled loops, customer lifecycle, growth stage classification,
moat analysis, failure mode monitoring, and unified engine orchestration.
"""

from __future__ import annotations
import pytest

from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSState,
    EOSStateMachine,
    OpportunityDecisionTree,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GrowthStageClassifier,
    FirstPrinciplesMoatAnalyzer,
    FailureModeMonitor,
    FirstPrinciplesEOSEngine,
)


def test_eos_state_machine_valid_transitions():
    """Verify valid state transitions and history tracking in EOSStateMachine."""
    sm = EOSStateMachine(initial_state=EOSState.SENSING)
    assert sm.current_state == EOSState.SENSING

    # Sensing -> Hypothesis
    assert sm.transition(EOSState.HYPOTHESIS, "Anomaly detected") is True
    assert sm.current_state == EOSState.HYPOTHESIS

    # Hypothesis -> CheapTest
    assert sm.transition(EOSState.CHEAP_TEST, "Hypothesis formed") is True

    # CheapTest -> Validation
    assert sm.transition(EOSState.VALIDATION, "Cheap test passed") is True

    # Validation -> BuildGate
    assert sm.transition(EOSState.BUILD_GATE, "Economic viability confirmed") is True

    # BuildGate -> MVP
    assert sm.transition(EOSState.MVP, "Resources allocated") is True

    # MVP -> GTMTest
    assert sm.transition(EOSState.GTM_TEST, "Product shipped") is True

    # GTMTest -> KillOrScale
    assert sm.transition(EOSState.KILL_OR_SCALE, "GTM signal collected") is True

    # KillOrScale -> Scale
    assert sm.transition(EOSState.SCALE, "Metrics exceed threshold") is True

    # Scale -> Operate
    assert sm.transition(EOSState.OPERATE, "Repeatable loop confirmed") is True

    # Operate -> Reinvent
    assert sm.transition(EOSState.REINVENT, "Market leadership & reinvention requisite") is True

    # Reinvent -> Sensing
    assert sm.transition(EOSState.SENSING, "Re-entering sensing loop") is True

    assert len(sm.history) == 12


def test_eos_state_machine_invalid_transitions_and_falsification():
    """Verify invalid transitions are rejected and falsification/kill paths work."""
    sm = EOSStateMachine(initial_state=EOSState.SENSING)

    # Invalid jump from Sensing directly to Scale
    assert sm.transition(EOSState.SCALE, "Premature scaling attempt") is False
    assert sm.current_state == EOSState.SENSING

    # Sensing -> Hypothesis -> Discard
    sm.transition(EOSState.HYPOTHESIS)
    assert sm.transition(EOSState.DISCARD, "Falsified hypothesis") is True
    assert sm.current_state == EOSState.DISCARD

    # Discard -> Sensing
    assert sm.transition(EOSState.SENSING, "Back to sensing") is True
    assert sm.current_state == EOSState.SENSING


def test_opportunity_decision_tree_logic():
    """Verify decision tree branches, Type I vs Type II risk handling, and structural advantage criteria."""
    dt = OpportunityDecisionTree()

    # 1. Noise signal -> Discard
    res_noise = dt.evaluate_opportunity(anomaly_is_structural=False, is_reversible=True)
    assert res_noise["pursue"] is False
    assert "Noise signal" in res_noise["reason"]

    # 2. Type I (Irreversible) without high confidence signal -> Discard
    res_type1_fail = dt.evaluate_opportunity(
        anomaly_is_structural=True, is_reversible=False, high_confidence_signal=False
    )
    assert res_type1_fail["pursue"] is False
    assert res_type1_fail["risk_type"] == "Type I (Irreversible)"

    # 3. Type II (Reversible) cheap test fails kill threshold -> Discard
    res_cheap_fail = dt.evaluate_opportunity(
        anomaly_is_structural=True,
        is_reversible=True,
        cheap_test_available=True,
        test_exceeds_kill_threshold=False,
    )
    assert res_cheap_fail["pursue"] is False
    assert "kill threshold" in res_cheap_fail["reason"]

    # 4. No cheap test & EV not positive -> Discard
    res_no_cheap_ev_fail = dt.evaluate_opportunity(
        anomaly_is_structural=True,
        is_reversible=True,
        cheap_test_available=False,
        ev_clearly_positive=False,
    )
    assert res_no_cheap_ev_fail["pursue"] is False

    # 5. Passes all tests but lacks structural advantage -> Discard
    res_no_moat = dt.evaluate_opportunity(
        anomaly_is_structural=True,
        is_reversible=True,
        cheap_test_available=True,
        test_exceeds_kill_threshold=True,
        structural_advantage_exists=False,
    )
    assert res_no_moat["pursue"] is False
    assert "structural advantage" in res_no_moat["reason"]

    # 6. All conditions met -> Pursue
    res_commit = dt.evaluate_opportunity(
        anomaly_is_structural=True,
        is_reversible=True,
        cheap_test_available=True,
        test_exceeds_kill_threshold=True,
        structural_advantage_exists=True,
    )
    assert res_commit["pursue"] is True
    assert "commit resources" in res_commit["reason"].lower()


def test_coupled_business_loops_evaluation():
    """Verify evaluation and failure mode detection across all 13 external business loops."""
    engine = CoupledBusinessLoopsEngine()

    healthy_metrics = {
        "retention_rate": 0.60,
        "nps": 50,
        "cac_cents": 50_00,
        "marketing_conversion_rate": 0.05,
        "win_rate": 0.30,
        "nrr": 1.25,
        "arpu_cents": 100_00,
        "viral_coefficient_k": 0.9,
        "decision_latency_hours": 12,
        "gross_margin": 0.80,
        "burn_multiple": 1.1,
        "runway_months": 24,
        "time_to_fill_days": 30,
        "enps": 50,
        "experiments_run_quarterly": 15,
        "relative_share_trend": 0.10,
    }

    results = engine.evaluate_all_loops(healthy_metrics)
    assert len(results) == 13
    assert all(loop_data["healthy"] for loop_data in results.values())

    # Test unhealthy / failure mode injected metrics
    unhealthy_metrics = {
        **healthy_metrics,
        "loudest_customer_feature_bias": True,
        "spend_scaled_before_message_fit": True,
        "selling_to_non_icp": True,
        "cs_reactive_only": True,
        "cost_plus_pricing": True,
        "vanity_metrics_only": True,
    }

    unhealthy_results = engine.evaluate_all_loops(unhealthy_metrics)
    assert unhealthy_results["product"]["healthy"] is False
    assert "loudest customer" in unhealthy_results["product"]["failure_mode"]
    assert unhealthy_results["marketing"]["healthy"] is False
    assert unhealthy_results["sales"]["healthy"] is False
    assert unhealthy_results["customer_success"]["healthy"] is False
    assert unhealthy_results["pricing"]["healthy"] is False
    assert unhealthy_results["data"]["healthy"] is False


def test_customer_lifecycle_engine():
    """Verify full 15-stage customer journey metrics, specifications, and optimization levers."""
    engine = CustomerLifecycleEngine()
    assert len(engine.STAGES) == 15
    assert len(engine.STAGE_SPECIFICATIONS) == 15

    metrics = {
        "awareness": 0.80,
        "onboarding": 0.40,  # Below threshold -> needs optimization
        "retention": 0.70,
    }

    journey = engine.evaluate_journey(metrics)
    assert len(journey) == 15
    assert journey["Awareness"]["needs_optimization"] is False
    assert journey["Onboarding"]["needs_optimization"] is True
    assert "job-to-be-done" in journey["Onboarding"]["actionable_lever"]


def test_growth_stage_classifier():
    """Verify company growth classification across all 9 stages and constraint identification."""
    classifier = GrowthStageClassifier()

    # Idea
    s1 = classifier.classify_stage({})
    assert s1["current_stage"] == "Idea"
    assert s1["binding_constraint"] == "Founder time"

    # Startup
    s2 = classifier.classify_stage({"paying_customers": 15})
    assert s2["current_stage"] == "Startup"
    assert s2["binding_constraint"] == "Cash runway"

    # PMF
    s3 = classifier.classify_stage({"paying_customers": 100, "retention_curve_flattened": True})
    assert s3["current_stage"] == "PMF"
    assert s3["binding_constraint"] == "Team bandwidth"

    # Scale
    s4 = classifier.classify_stage({"arr_cents": 15_000_000_00})
    assert s4["current_stage"] == "Scale"
    assert s4["binding_constraint"] == "Org coordination cost"

    # Market Leadership
    s5 = classifier.classify_stage({"category_share": 0.55})
    assert s5["current_stage"] == "Market Leadership"
    assert s5["key_risk"] == "Complacency, disruption from below"


def test_moat_analyzer():
    """Verify evaluation of 6 competitive moat sources and technology shift timing."""
    analyzer = FirstPrinciplesMoatAnalyzer()

    metrics = {
        "network_density": 0.8,
        "avg_switching_cost_cents": 8000_00,
        "cost_advantage_percent": 0.30,
        "brand_trust_score": 0.9,
        "patent_regulatory_moat_score": 0.5,
        "counter_positioning_score": 0.7,
        "cost_curve_viability_reached": True,
        "enabling_conditions_met": True,
    }

    res = analyzer.evaluate_moats(metrics)
    assert 0.5 <= res["composite_moat_durability_score"] <= 1.0
    assert len(res["breakdown"]) == 6
    assert res["technology_shift_timing"]["cost_curve_viability_reached"] is True


def test_failure_mode_monitor_diagnoses():
    """Verify pattern matching against all 10 operating failure modes."""
    monitor = FailureModeMonitor()

    failing_metrics = {
        "survey_positive": True,
        "engagement_rate": 0.02,  # Solving wrong problem
        "build_velocity_high": True,
        "demand_growth": 0.0,  # Building before validating
        "sales_cycle_days": 120,
        "feature_comparison_objections": True,  # Weak positioning
        "cost_plus_pricing": True,  # Poor pricing
        "nps": 70,
        "revenue_growth": 0.0,  # Distribution failure
        "retention_curve_flattened": False,
        "spend_scaling": True,  # Lack of PMF
        "decision_latency_hours": 96,  # Organizational bottlenecks
        "ignoring_disconfirming_data": True,  # Founder bias
        "cac_growth_rate": 0.5,
        "ltv_growth_rate": 0.1,  # Scaling prematurely
        "multiple_underperforming_bets": True,  # Capital misallocation
    }

    diagnoses = monitor.diagnose_failure_modes(failing_metrics)
    assert len(diagnoses) == 10
    failure_names = [d["failure_mode"] for d in diagnoses]
    assert "solving_wrong_problem" in failure_names
    assert "building_before_validating" in failure_names
    assert "weak_positioning" in failure_names
    assert "poor_pricing" in failure_names
    assert "distribution_failure" in failure_names
    assert "lack_of_pmf" in failure_names
    assert "organizational_bottlenecks" in failure_names
    assert "founder_bias" in failure_names
    assert "scaling_prematurely" in failure_names
    assert "capital_misallocation" in failure_names


def test_first_principles_eos_engine_e2e():
    """Verify unified FirstPrinciplesEOSEngine holistic evaluation workflow."""
    engine = FirstPrinciplesEOSEngine()

    metrics = {
        "paying_customers": 50,
        "retention_curve_flattened": True,
        "arr_cents": 2_500_000_00,
        "network_density": 0.6,
        "avg_switching_cost_cents": 5000_00,
        "brand_trust_score": 0.8,
        "retention_rate": 0.65,
        "nps": 55,
        "cac_cents": 40_00,
        "marketing_conversion_rate": 0.04,
        "win_rate": 0.35,
        "nrr": 1.20,
        "arpu_cents": 120_00,
        "viral_coefficient_k": 0.85,
        "decision_latency_hours": 16,
        "gross_margin": 0.82,
        "burn_multiple": 1.2,
        "runway_months": 20,
        "time_to_fill_days": 35,
        "enps": 45,
        "experiments_run_quarterly": 12,
        "relative_share_trend": 0.08,
    }

    evaluation = engine.evaluate_venture_state(metrics)
    assert evaluation["current_state"] == "Sensing"
    assert evaluation["growth_stage"]["current_stage"] == "Growth"
    assert evaluation["moats"]["composite_moat_durability_score"] > 0.3
    assert len(evaluation["failure_diagnoses"]) == 0
    assert evaluation["healthy"] is True
