from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    FeedbackLoop,
    LoopTimescale,
    SignalToIdeaEngine,
    RiskType,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleTracker,
    CustomerStage,
    GrowthStageClassifier,
    GrowthStage,
    FailureModeMonitor,
    OpportunityDecisionTree,
    EOSStateMachine,
    EOSLifecycleState,
    AIEOSAutonomousModules
)
from apodex.arcs.kernel.kernel import EIOSKernel


def test_timescale_loop_velocity():
    loop = FeedbackLoop(
        loop_id="loop_1",
        name="Ad Test Experiment",
        timescale=LoopTimescale.FAST,
        cycle_time_days=2.5,
        signal_to_noise_ratio=5.0,
        input_stock="Capital",
        output_stock="Conversion Data",
        kpi_name="CAC",
        kpi_value=45.0
    )
    assert loop.calculate_velocity() == pytest.approx(0.4)


def test_signal_to_idea_engine_anomaly_and_bayes():
    engine = SignalToIdeaEngine()

    # Anomaly detection beyond Kuhn threshold
    anomaly, is_structural = engine.detect_anomaly("Compute traffic curve mismatch", observed=300.0, expected=50.0)
    assert is_structural is True
    assert anomaly.kuhn_surprise_score == pytest.approx(5.0)

    # Hypothesis formation
    hyp = engine.form_hypothesis("Streaming on broadband is viable", RiskType.TYPE_II, test_cost=100.0, info_value=5000.0)
    assert hyp.posterior_probability == 0.5
    assert hyp.risk_type == RiskType.TYPE_II

    # Bayesian update
    hyp_updated = engine.update_bayesian_belief(hyp, likelihood_if_true=0.9, likelihood_if_false=0.1)
    assert hyp_updated.posterior_probability > 0.8
    assert hyp_updated.is_falsified is False

    # Bayesian falsification
    hyp_falsified = engine.update_bayesian_belief(hyp, likelihood_if_true=0.01, likelihood_if_false=0.99)
    assert hyp_falsified.is_falsified is True


def test_coupled_business_loops():
    engine = CoupledBusinessLoopsEngine()
    initial_state = engine.state.copy()

    updated_state = engine.run_coupled_step()
    assert "ltv_cac_ratio" in updated_state
    assert updated_state["ltv_cac_ratio"] > 0


def test_customer_lifecycle_tracker_bottleneck():
    tracker = CustomerLifecycleTracker()
    cohort_data = {
        CustomerStage.AWARENESS: 1000,
        CustomerStage.INTEREST: 800,
        CustomerStage.CONSIDERATION: 600,
        CustomerStage.EVALUATION: 500,
        CustomerStage.PURCHASE: 100,  # Large dropoff (80%)
        CustomerStage.ONBOARDING: 90,
        CustomerStage.ACTIVATION: 80,
        CustomerStage.ENGAGEMENT: 75,
        CustomerStage.HABIT_FORMATION: 70,
        CustomerStage.RETENTION: 65,
        CustomerStage.LOYALTY: 60,
        CustomerStage.ADVOCACY: 55,
        CustomerStage.REFERRAL: 50,
        CustomerStage.EXPANSION: 45,
        CustomerStage.REPURCHASE: 40,
    }
    tracker.record_cohort(cohort_data)
    bottleneck, dropoff = tracker.identify_primary_bottleneck()

    assert bottleneck == CustomerStage.PURCHASE
    assert dropoff == pytest.approx(0.8)


def test_growth_stage_classifier():
    classifier = GrowthStageClassifier()

    # Validation stage
    stage_val, const_val = classifier.classify_stage({"paying_customers": 3})
    assert stage_val == GrowthStage.VALIDATION

    # PMF stage
    stage_pmf, const_pmf = classifier.classify_stage({"paying_customers": 30, "retention_flattened": True})
    assert stage_pmf == GrowthStage.PMF
    assert const_pmf == "Team bandwidth"

    # Market Leadership stage
    stage_lead, const_lead = classifier.classify_stage({"market_share": 0.45, "third_party_devs": 1500})
    assert stage_lead == GrowthStage.MARKET_LEADERSHIP


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()
    metrics = {
        "cac_payback_months": 30,
        "growth_rate": 0.80,
        "decision_latency_days": 20
    }
    alerts = monitor.evaluate_failure_modes(metrics)
    modes = [a["mode"] for a in alerts]

    assert "Premature scaling" in modes
    assert "Organizational bottlenecks" in modes


def test_opportunity_decision_tree():
    tree = OpportunityDecisionTree()

    # Passing test
    pursue, reason = tree.evaluate(
        is_structural_anomaly=True,
        is_reversible=True,
        high_confidence_signal=False,
        cheap_test_available=True,
        test_passed=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert pursue is True

    # Failing test: Irreversible without high confidence signal
    pursue_type1_fail, reason_type1 = tree.evaluate(
        is_structural_anomaly=True,
        is_reversible=False,
        high_confidence_signal=False,
        cheap_test_available=False,
        test_passed=False,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert pursue_type1_fail is False
    assert "Type I" in reason_type1


def test_eos_state_machine():
    sm = EOSStateMachine()
    assert sm.current_state == EOSLifecycleState.SENSING

    sm.transition_to(EOSLifecycleState.HYPOTHESIS, "Anomaly flagged")
    assert sm.current_state == EOSLifecycleState.HYPOTHESIS
    assert len(sm.history) == 2


def test_ai_eos_autonomous_modules_end_to_end():
    modules = AIEOSAutonomousModules()
    telemetry = {
        "anomaly_desc": "Exponential API usage curve",
        "observed": 500.0,
        "expected": 20.0,
        "reversible": True,
        "test_cost": 25.0,
        "info_val": 1000.0,
        "moat_advantage": True,
        "metrics": {"paying_customers": 100, "retention_flattened": True}
    }
    result = modules.run_full_sensing_to_allocation_cycle(telemetry, "Deploy self-serve API plan")

    assert result["status"] == "APPROVED"
    assert result["stage"] == GrowthStage.GROWTH.value


def test_eios_kernel_integration():
    kernel = EIOSKernel()

    # Anomaly capability
    anom_res = kernel.sense_opportunity_anomalies("Unusual conversion spike", observed=80.0, expected=10.0)
    assert anom_res["is_structural"] is True

    # Hypothesis capability
    hyp_res = kernel.generate_falsifiable_hypothesis("PLG motion will halve CAC", risk_type="TYPE_II", test_cost=50.0, info_val=2000.0)
    assert hyp_res["risk_type"] == "TYPE_II"

    # GTM Channel reasoning capability
    channel_ent = kernel.reason_gtm_channel(price_usd=50000.0, complexity="high")
    assert channel_ent == "ENTERPRISE_SALES_LED"

    channel_plg = kernel.reason_gtm_channel(price_usd=500.0, complexity="low")
    assert channel_plg == "PRODUCT_LED_GROWTH_PLG"

    # Moat durability capability
    moat_score = kernel.analyze_moat_durability("NETWORK_EFFECTS")
    assert moat_score == 0.95

    # Reinvention review capability
    reinvent_triggered = kernel.trigger_reinvention_review(GrowthStage.MARKET_LEADERSHIP.value, market_share=0.42)
    assert reinvent_triggered is True
