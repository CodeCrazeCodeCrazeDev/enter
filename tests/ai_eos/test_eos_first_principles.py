"""Verification test suite for First-Principles Entrepreneurial Operating System (EOS)."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    Timescale,
    MasterLoopNode,
    CustomerJourneyStage,
    CompanyGrowthStage,
    FeedbackLoop,
    MultiTimescaleLoopEngine,
    MasterLoopStateMachine,
    SignalHypothesisFilter,
    BusinessLoopSet,
    CustomerJourneyLifecycle,
    GrowthStageClassifier,
    CompetitiveStrategyEngine,
    FailureModeMonitor,
    FirstPrinciplesEOSEngine,
)


def test_multi_timescale_loop_engine():
    engine = MultiTimescaleLoopEngine()
    fast_loop = FeedbackLoop(
        loop_id="ad_test",
        name="Ad Testing Loop",
        timescale=Timescale.FAST,
        feedback_signal=0.2,
        core_kpi=0.05,
        velocity=2.0,
    )
    slow_loop = FeedbackLoop(
        loop_id="moat_building",
        name="Moat Construction Loop",
        timescale=Timescale.SLOW,
        feedback_signal=0.1,
        core_kpi=0.8,
        velocity=0.1,
    )
    engine.register_loop(fast_loop)
    engine.register_loop(slow_loop)

    executed_fast = engine.execute_timescale(Timescale.FAST)
    assert "ad_test" in executed_fast
    assert "moat_building" not in executed_fast
    assert executed_fast["ad_test"]["compounding_factor"] == pytest.approx(2.4)


def test_master_loop_state_machine_reentrancy():
    sm = MasterLoopStateMachine()
    assert sm.current_node == MasterLoopNode.ENVIRONMENTAL_SENSING

    # Test sequential transition
    sm.transition_to(MasterLoopNode.CUSTOMER_VALIDATION)
    assert sm.current_node == MasterLoopNode.CUSTOMER_VALIDATION

    # Test kill signal from Node F -> Node D
    next_node = sm.evaluate_reentrant_signal(MasterLoopNode.CUSTOMER_VALIDATION, {"falsified": True})
    assert next_node == MasterLoopNode.OPPORTUNITY_DISCOVERY

    # Test weak GTM signal from Node K -> Node J
    sm.transition_to(MasterLoopNode.CUSTOMER_ACQUISITION)
    next_node = sm.evaluate_reentrant_signal(MasterLoopNode.CUSTOMER_ACQUISITION, {"weak_gtm": True})
    assert next_node == MasterLoopNode.GTM_SYSTEM

    # Test bad unit economics signal from Node M -> Node G
    sm.transition_to(MasterLoopNode.UNIT_ECONOMICS_OPTIMIZATION)
    next_node = sm.evaluate_reentrant_signal(MasterLoopNode.UNIT_ECONOMICS_OPTIMIZATION, {"bad_economics": True})
    assert next_node == MasterLoopNode.BUSINESS_MODEL_DESIGN


def test_signal_hypothesis_filter():
    filt = SignalHypothesisFilter(anomaly_threshold=0.6)

    # Structural anomaly vs noise
    anomaly_signal = {"unexpectedness": 0.8, "structural_alignment": 0.7}  # 0.6*0.8 + 0.4*0.7 = 0.76 >= 0.6
    noise_signal = {"unexpectedness": 0.2, "structural_alignment": 0.1}

    assert filt.is_structural_anomaly(anomaly_signal) is True
    assert filt.is_structural_anomaly(noise_signal) is False

    # Bayesian belief updating
    posterior = filt.update_bayesian_belief(prior_confidence=0.5, likelihood_ratio=3.0)
    assert posterior == pytest.approx(0.75)

    # Risk evaluation heuristic
    assert filt.evaluate_risk_heuristic("type_i", confidence=0.85) == "proceed_deliberate"
    assert filt.evaluate_risk_heuristic("type_i", confidence=0.5) == "defer_gather_evidence"
    assert filt.evaluate_risk_heuristic("type_ii", confidence=0.3) == "proceed_fast_cheap"


def test_business_loop_set():
    loops = BusinessLoopSet()
    initial_cash = loops.stocks["cash_cents"]

    results = loops.simulate_step(
        cac_cents=500_00,       # $500 CAC
        arpu_cents=100_00,       # $100 ARPU
        churn_rate=0.02,         # 2% churn
        hiring_budget_cents=50_000_00,
        rd_investment_cents=20_000_00
    )

    assert "mrr_cents" in results
    assert "burn_multiple" in results
    assert "runway_months" in results
    assert results["unit_economics_healthy"] is True
    assert loops.stocks["cash_cents"] != initial_cash


def test_customer_journey_lifecycle():
    journey = CustomerJourneyLifecycle()
    results = journey.compute_funnel_throughput(initial_awareness_count=100000)

    assert results["activated_customers"] > 0
    assert results["retained_customers"] > 0
    assert "viral_coefficient_k" in results


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()

    # Idea stage
    res_idea = classifier.classify_stage(
        has_validated_learnings=False, paying_customers=0, retention_flattening=False,
        growth_rate_mom=0.0, rule_of_40_score=0.0, has_ecosystem_api=False,
        ecosystem_gmv_cents=0, category_share=0.0
    )
    assert res_idea["stage"] == CompanyGrowthStage.IDEA.value
    assert res_idea["binding_constraint"] == "founder_time"

    # Growth stage
    res_growth = classifier.classify_stage(
        has_validated_learnings=True, paying_customers=50, retention_flattening=True,
        growth_rate_mom=0.20, rule_of_40_score=0.30, has_ecosystem_api=False,
        ecosystem_gmv_cents=0, category_share=0.05
    )
    assert res_growth["stage"] == CompanyGrowthStage.GROWTH.value
    assert res_growth["binding_constraint"] == "hiring_velocity_and_systems"


def test_competitive_strategy_engine():
    engine = CompetitiveStrategyEngine()

    # Technology cost curve decay
    cost, is_viable = engine.compute_cost_curve_viability(
        c0_initial_cost=100.0, decay_rate_lambda=0.5, time_t=2.0, viability_threshold=40.0
    )
    # 100 * exp(-1.0) = ~36.78 <= 40.0
    assert cost == pytest.approx(36.7879, rel=1e-3)
    assert is_viable is True

    # Composite moat score
    moat = engine.compute_moat_durability(
        network_density=0.8, switching_cost_score=0.6, brand_trust_score=0.5, cost_advantage_score=0.7
    )
    # 0.3*0.8 + 0.25*0.6 + 0.2*0.5 + 0.25*0.7 = 0.24 + 0.15 + 0.10 + 0.175 = 0.665
    assert moat == pytest.approx(0.665)


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()

    # Trigger organizational bottleneck warning
    warnings = monitor.evaluate_operating_metrics({"decision_latency_hours": 96.0})
    assert len(warnings) == 1
    assert warnings[0]["failure_mode"] == "organizational_bottleneck"


def test_first_principles_eos_engine_full_cycle():
    engine = FirstPrinciplesEOSEngine()

    signal_data = {"unexpectedness": 0.8, "structural_alignment": 0.8}
    business_params = {
        "cac_cents": 400_00,
        "arpu_cents": 150_00,
        "churn_rate": 0.03,
        "hiring_budget_cents": 30_000_00,
        "rd_investment_cents": 10_000_00,
        "paying_customers": 25,
        "retention_flattening": True,
        "network_density": 0.5,
    }

    cycle_results = engine.run_full_execution_cycle(signal_data, business_params)

    assert cycle_results["is_structural_anomaly"] is True
    assert cycle_results["master_loop_node"] == MasterLoopNode.ENVIRONMENTAL_SENSING.value
    assert cycle_results["moat_durability_score"] > 0.0
    assert "simulation" in cycle_results
