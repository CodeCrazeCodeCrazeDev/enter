"""Unit tests for the EOS First-Principles Engine."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    Timescale,
    RiskType,
    EOSState,
    WeakSignal,
    Hypothesis,
    EXTERNAL_BUSINESS_LOOPS,
    CUSTOMER_JOURNEY_STAGES,
    COMPANY_GROWTH_STAGES,
    SignalToIdeaPipeline,
    DecisionTreeEvaluator,
    EOSStateMachine,
    FailureModeMonitor,
    EOSKPIDashboard
)


def test_signal_to_idea_pipeline():
    """Verify weak signals are filtered and converted into falsifiable hypotheses."""
    pipeline = SignalToIdeaPipeline()

    # Case 1: Noise (not an anomaly) -> Discard
    sig_noise = WeakSignal(
        description="Daily SaaS signups are normal",
        is_anomaly=False,
        source="Analytics",
        strength=0.5
    )
    hyp_noise = pipeline.filter_signal(sig_noise)
    assert hyp_noise is None
    assert len(pipeline.hypotheses) == 0

    # Case 2: Structural shift (anomaly) -> Promote
    sig_anomaly = WeakSignal(
        description="Generative AI search traffic growing at 300% month-over-month",
        is_anomaly=True,
        source="Google Trends",
        strength=0.9
    )
    hyp_anomaly = pipeline.filter_signal(sig_anomaly)
    assert hyp_anomaly is not None
    assert "compounding advantage" in hyp_anomaly.claim
    assert hyp_anomaly.is_falsifiable is True
    assert hyp_anomaly.prior_confidence == pytest.approx(0.27)
    assert len(pipeline.hypotheses) == 1


def test_risk_classification():
    """Verify decision risk profiling handles Type I (one-way doors) vs Type II (two-way doors)."""
    pipeline = SignalToIdeaPipeline()

    # Reversible decision -> Type II
    risk_type_ii = pipeline.evaluate_risk_profile(
        decision_name="Change landing page CTA from blue to green",
        irreversible_regulatory_safety=False
    )
    assert risk_type_ii == RiskType.TYPE_II

    # Irreversible decision -> Type I
    risk_type_i = pipeline.evaluate_risk_profile(
        decision_name="Incorporate as a Swiss AG and commit to multi-year healthcare regulatory compliance",
        irreversible_regulatory_safety=True
    )
    assert risk_type_i == RiskType.TYPE_I


def test_decision_tree_evaluator():
    """Verify 'Should We Pursue This Opportunity?' Decision Tree rules (Q1 to Q5)."""
    evaluator = DecisionTreeEvaluator()

    # Case 1: Noise (Q1 fails) -> Discard
    ok, rationale = evaluator.evaluate(
        is_structural_anomaly=False,
        is_reversible=True,
        has_high_confidence_multi_source=True,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert ok is False
    assert "noise" in rationale.lower()

    # Case 2: Irreversible and lacks multi-source confidence (Q2a fails) -> Discard
    ok, rationale = evaluator.evaluate(
        is_structural_anomaly=True,
        is_reversible=False,
        has_high_confidence_multi_source=False,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert ok is False
    assert "irreversible" in rationale.lower()

    # Case 3: Cheap test available but failed to exceed threshold (Q4 fails) -> Discard
    ok, rationale = evaluator.evaluate(
        is_structural_anomaly=True,
        is_reversible=True,
        has_high_confidence_multi_source=True,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill_threshold=False,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert ok is False
    assert "kill threshold" in rationale.lower()

    # Case 4: Cheap test unavailable and expected value is negative (Q4b fails) -> Discard
    ok, rationale = evaluator.evaluate(
        is_structural_anomaly=True,
        is_reversible=True,
        has_high_confidence_multi_source=True,
        cheap_test_available=False,
        cheap_test_result_exceeds_kill_threshold=False,
        expected_value_positive=False,
        has_structural_advantage=True
    )
    assert ok is False
    assert "unavailable" in rationale.lower()

    # Case 5: Lacks structural advantage (Q5 fails) -> Discard
    ok, rationale = evaluator.evaluate(
        is_structural_anomaly=True,
        is_reversible=True,
        has_high_confidence_multi_source=True,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=False
    )
    assert ok is False
    assert "structural advantage" in rationale.lower()

    # Case 6: Fully qualified opportunity -> Pursue
    ok, rationale = evaluator.evaluate(
        is_structural_anomaly=True,
        is_reversible=True,
        has_high_confidence_multi_source=True,
        cheap_test_available=True,
        cheap_test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert ok is True
    assert "commit resources" in rationale.lower()


def test_state_machine_transitions():
    """Verify system state transitions and validation constraints."""
    sm = EOSStateMachine()
    assert sm.state == EOSState.SENSING

    # SENSING -> HYPOTHESIS is allowed
    assert sm.transition_to(EOSState.HYPOTHESIS, "anomaly confirmed") is True
    assert sm.state == EOSState.HYPOTHESIS

    # SENSING -> SCALE is not allowed from HYPOTHESIS
    assert sm.transition_to(EOSState.SCALE, "premature scaling") is False
    assert sm.state == EOSState.HYPOTHESIS

    # HYPOTHESIS -> CHEAP_TEST is allowed
    assert sm.transition_to(EOSState.CHEAP_TEST, "launch smoke test") is True
    assert sm.state == EOSState.CHEAP_TEST

    # CHEAP_TEST -> VALIDATION is allowed
    assert sm.transition_to(EOSState.VALIDATION, "smoke test validated") is True
    assert sm.state == EOSState.VALIDATION

    # VALIDATION -> BUILD_GATE is allowed
    assert sm.transition_to(EOSState.BUILD_GATE, "unit economics positive") is True
    assert sm.state == EOSState.BUILD_GATE

    # BUILD_GATE -> MVP is allowed
    assert sm.transition_to(EOSState.MVP, "resource MVP development") is True
    assert sm.state == EOSState.MVP

    # MVP -> GTM_TEST is allowed
    assert sm.transition_to(EOSState.GTM_TEST, "ship GTM campaign") is True
    assert sm.state == EOSState.GTM_TEST

    # GTM_TEST -> KILL_OR_SCALE is allowed
    assert sm.transition_to(EOSState.KILL_OR_SCALE, "gather GTM results") is True
    assert sm.state == EOSState.KILL_OR_SCALE

    # KILL_OR_SCALE -> SCALE is allowed
    assert sm.transition_to(EOSState.SCALE, "scale marketing spend") is True
    assert sm.state == EOSState.SCALE

    # SCALE -> OPERATE is allowed
    assert sm.transition_to(EOSState.OPERATE, "operation consistency achieved") is True
    assert sm.state == EOSState.OPERATE

    # OPERATE -> REINVENT is allowed
    assert sm.transition_to(EOSState.REINVENT, "initiate self-disruption review") is True
    assert sm.state == EOSState.REINVENT

    # REINVENT -> SENSING is allowed (re-entrant loops)
    assert sm.transition_to(EOSState.SENSING, "loop back to top-level environmental sensing") is True
    assert sm.state == EOSState.SENSING

    # Discard is always allowed
    assert sm.transition_to(EOSState.DISCARDED, "sunset the opportunity") is True
    assert sm.state == EOSState.DISCARDED


def test_business_loops_and_coupling():
    """Verify all 13 external business loops are modeled and consistent."""
    assert len(EXTERNAL_BUSINESS_LOOPS) == 13

    # Product
    product_loop = EXTERNAL_BUSINESS_LOOPS["Product"]
    assert product_loop.name == "Product"
    assert "feature adoption" in product_loop.core_kpis
    assert "loudest customer" in product_loop.dominant_failure_mode

    # Pricing
    pricing_loop = EXTERNAL_BUSINESS_LOOPS["Pricing"]
    assert pricing_loop.name == "Pricing"
    assert "elasticity" in pricing_loop.core_kpis
    assert "Cost-plus" in pricing_loop.dominant_failure_mode

    # Financial
    financial_loop = EXTERNAL_BUSINESS_LOOPS["Financial"]
    assert financial_loop.name == "Financial"
    assert "burn multiple" in financial_loop.core_kpis


def test_customer_journey_stages():
    """Verify all 15 stages of the full-lifecycle Customer Journey are modeled."""
    assert len(CUSTOMER_JOURNEY_STAGES) == 15

    # Awareness
    stage_awareness = CUSTOMER_JOURNEY_STAGES["Awareness"]
    assert stage_awareness.stage_name == "Awareness"
    assert stage_awareness.founder_objective == "Enter consideration set"
    assert "Pattern-matching" in stage_awareness.customer_psychology

    # Activation
    stage_activation = CUSTOMER_JOURNEY_STAGES["Activation"]
    assert stage_activation.stage_name == "Activation"
    assert "true 'aha' moment" in stage_activation.optimization_lever

    # Referral
    stage_referral = CUSTOMER_JOURNEY_STAGES["Referral"]
    assert stage_referral.stage_name == "Referral"
    assert "Generic referral programs" in stage_referral.common_mistake


def test_company_growth_stages():
    """Verify all company growth stages are modeled accurately with objectives and constraints."""
    assert len(COMPANY_GROWTH_STAGES) == 9

    # Idea
    stage_idea = COMPANY_GROWTH_STAGES["Idea"]
    assert stage_idea.stage_name == "Idea"
    assert "sweat equity" in stage_idea.capital_allocation
    assert stage_idea.binding_constraint == "Founder time"

    # Startup
    stage_startup = COMPANY_GROWTH_STAGES["Startup"]
    assert stage_startup.stage_name == "Startup"
    assert stage_startup.binding_constraint == "Cash runway"

    # Market Leadership
    stage_ml = COMPANY_GROWTH_STAGES["Market Leadership"]
    assert stage_ml.stage_name == "Market Leadership"
    assert "Complacency" in stage_ml.key_risk


def test_failure_mode_monitor():
    """Verify pattern-matching of operating metrics against the 10 failure modes."""
    monitor = FailureModeMonitor()

    # Case 1: Solving the wrong problem
    metrics_wrong_problem = {
        "user_engagement": 0.05,
        "survey_satisfaction_score": 0.90
    }
    flags = monitor.inspect_metrics(metrics_wrong_problem)
    assert len(flags) == 1
    assert flags[0][0] == "Solving the wrong problem"
    assert "5-Whys" in flags[0][2]

    # Case 2: Weak positioning
    metrics_weak_positioning = {
        "cac_usd": 250,
        "sales_cycle_days": 120,
        "feature_comparison_objections": 8
    }
    flags = monitor.inspect_metrics(metrics_weak_positioning)
    assert len(flags) == 1
    assert flags[0][0] == "Weak positioning"

    # Case 3: Lack of product-market fit
    metrics_premature_scale = {
        "retention_curve_slope": -0.22,
        "is_scaling_budget": True
    }
    flags = monitor.inspect_metrics(metrics_premature_scale)
    assert len(flags) == 1
    assert flags[0][0] == "Lack of product-market fit"


def test_kpi_dashboard_rollup():
    """Verify rolled up KPI dashboard calculations and loop closure metric."""
    dashboard = EOSKPIDashboard()

    dashboard.update_sensing(signal_to_noise=0.85, anomaly_lead_time_days=4.0)
    dashboard.update_validation(cost_per_learning_usd=120.0, false_positive_rate=0.08)
    dashboard.update_product(activation_rate=0.65, retention_slope=-0.02)
    dashboard.update_gtm(cac=150.0, payback_months=11.0, organic_share=0.45)
    dashboard.update_financial(gross_margin=0.82, burn_multiple=1.2, runway_months=24.0)
    dashboard.update_org(decision_latency_days=2.5, attrition_rate=0.05)
    dashboard.update_strategic(market_share_pct=15.0, moat_durability=0.75)

    assert dashboard.sensing_metrics["signal_to_noise_ratio"] == 0.85
    assert dashboard.financial_metrics["runway_months"] == 24.0
    assert dashboard.strategic_metrics["moat_durability_score"] == 0.75

    # Overall loop-closure time (sensing + decision + validation_offset)
    loop_closure_time = dashboard.get_loop_closure_time_days()
    # sensing(4.0) + decision(2.5) + validation_offset(4.5) = 11.0
    assert loop_closure_time == 11.0
