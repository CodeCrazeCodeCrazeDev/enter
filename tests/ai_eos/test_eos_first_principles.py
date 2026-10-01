"""Unit and integration tests for EOS First-Principles Executable Engine."""

import pytest
from apodex.ai_eos.intelligence import (
    EOSEngineFirstPrinciples,
    AnomaliesAndSensingEngine,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GTMSystemSimulator,
    CompanyGrowthStateMachine,
    StrategicMoatEngine,
    FailureModeMonitor,
    EOSOpportunityDecisionTree,
)


def test_anomalies_and_sensing_engine():
    sensing = AnomaliesAndSensingEngine(baseline_threshold=0.3)
    signals = [
        {"id": "s1", "name": "normal_traffic", "observed_value": 0.5, "expected_value": 0.5, "is_structural_shift": False},
        {"id": "s2", "name": "cuda_mismatch", "observed_value": 0.9, "expected_value": 0.1, "is_structural_shift": True},
    ]

    anomalies = sensing.sense_signal_stream(signals)
    assert len(anomalies) == 1
    assert anomalies[0]["signal_id"] == "s2"
    assert anomalies[0]["is_structural"] is True

    # Form hypothesis
    hyp = sensing.form_hypothesis(anomalies[0], "CUDA compute shift enables non-graphics acceleration", kill_threshold=0.7)
    assert hyp["status"] == "proposed"
    assert hyp["posterior_confidence"] == 0.5

    # Run cheap test
    updated = sensing.run_cheap_test(hyp["hypothesis_id"], test_cost_cents=500_00, successes=8, trials=10)
    assert updated["status"] == "strengthened"
    assert updated["posterior_confidence"] > 0.7


def test_external_business_loops_engine():
    engine = ExternalBusinessLoopsEngine()

    # Test single loop health
    res = engine.evaluate_loop_health("financial", {"burn_multiple": 1.2, "runway_months": 18})
    assert res["status"] == "healthy"
    assert res["health_score"] >= 0.7

    res_critical = engine.evaluate_loop_health("financial", {"burn_multiple": 3.0, "runway_months": 4})
    assert res_critical["status"] == "critical"
    assert len(res_critical["alerts"]) >= 2

    # Test coupled loops
    metrics = {
        "financial": {"burn_multiple": 1.1, "runway_months": 24},
        "product": {"nps": 70},
        "pricing": {"arpu": 200},
        "hiring": {"time_to_fill": 20},
    }
    coupled = engine.evaluate_coupled_loops(metrics)
    assert "average_system_health" in coupled
    assert "high_leverage_health" in coupled


def test_customer_lifecycle_engine():
    engine = CustomerLifecycleEngine()

    # Stage performance
    onboarding_eval = engine.evaluate_stage_performance("onboarding", {"time_to_first_value_hours": 60})
    assert len(onboarding_eval["alerts"]) == 1
    assert "TTFV exceeds 48h" in onboarding_eval["alerts"][0]

    # Cohort retention analysis
    retention_series = [1.0, 0.6, 0.45, 0.35, 0.34, 0.34]
    cohort_res = engine.analyze_cohort_retention(retention_series)
    assert cohort_res["flattened"] is True
    assert cohort_res["pmf_retention_signal"] is True


def test_gtm_system_simulator():
    simulator = GTMSystemSimulator()

    # Low ACV / Low complexity -> PLG
    plg_fit = simulator.simulate_channel_fit("Developer API Tool", acv_cents=500_00, complexity="low", channel="plg")
    assert plg_fit["is_aligned"] is True

    # High ACV -> SLG
    enterprise_fit = simulator.simulate_channel_fit("Enterprise Core Banking", acv_cents=100000_00, complexity="high", channel="enterprise_sales")
    assert enterprise_fit["is_aligned"] is True

    # Compounding motions
    compounding = simulator.simulate_compounding_motions(["plg", "slg", "content"])
    assert compounding["compounding_multiplier"] >= 1.5
    assert compounding["has_land_and_expand_synergy"] is True


def test_company_growth_state_machine():
    sm = CompanyGrowthStateMachine(initial_stage="idea")
    assert sm.current_stage == "idea"

    # Transition from idea to validation
    res = sm.evaluate_stage_transition({"validated_learnings": 4})
    assert res["can_transition"] is True
    assert sm.current_stage == "validation"

    # Try transition without meeting criteria
    res2 = sm.evaluate_stage_transition({"paying_customers": 1})
    assert res2["can_transition"] is False
    assert sm.current_stage == "validation"


def test_strategic_moat_engine():
    moat = StrategicMoatEngine()

    moat_res = moat.score_moat_durability({
        "network_effects": 0.9,
        "switching_costs": 0.8,
        "economies_of_scale": 0.85,
        "brand_trust": 0.7,
        "counter_positioning": 0.9,
    })
    assert moat_res["durability_tier"] == "impregnable"
    assert moat_res["composite_moat_score"] >= 0.8

    # Cost curve viability
    cost_res = moat.evaluate_cost_curve_viability([1000.0, 500.0, 100.0, 10.0], threshold=15.0)
    assert cost_res["viable"] is True
    assert cost_res["crossing_index"] == 3

    # Reinvention trigger
    reinv = moat.check_reinvention_trigger(revenue_decay_rate=0.05, customer_attrition_rate=0.02, leading_indicator_drop=0.30)
    assert reinv["reinvention_triggered"] is True


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()

    diagnostics = monitor.diagnose_failure_modes({
        "high_build_velocity": True,
        "demand_signal": 0.05,
        "retention_curve_slope": -0.1,
        "is_scaling_spend": True,
    })

    modes = [d["failure_mode"] for d in diagnostics]
    assert "building_before_validating" in modes
    assert "scaling_prematurely" in modes


def test_eos_opportunity_decision_tree():
    tree = EOSOpportunityDecisionTree()

    # Noise -> Discard
    res_noise = tree.evaluate_opportunity({"is_structural_anomaly": False})
    assert res_noise["decision"] == "DISCARD"

    # Cheap test -> Run cheap test
    res_test = tree.evaluate_opportunity({
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": True,
        "test_result_exceeds_kill_threshold": False,
    })
    assert res_test["decision"] == "RUN_CHEAP_TEST"

    # All criteria met -> Commit
    res_commit = tree.evaluate_opportunity({
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": False,
        "expected_value_positive": True,
        "has_structural_advantage": True,
    })
    assert res_commit["decision"] == "COMMIT"


def test_eos_engine_first_principles_e2e():
    engine = EOSEngineFirstPrinciples()

    signals = [
        {"id": "sig-01", "name": "ai_llm_cost_drop", "observed_value": 0.01, "expected_value": 0.50, "is_structural_shift": True}
    ]
    opportunity = {
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": False,
        "expected_value_positive": True,
        "has_structural_advantage": True,
    }
    loop_metrics = {
        "financial": {"burn_multiple": 1.1, "runway_months": 24},
        "product": {"nps": 60},
    }
    growth_metrics = {
        "validated_learnings": 5,
    }

    full_res = engine.run_full_eos_cycle(
        signals=signals,
        opportunity=opportunity,
        loop_metrics=loop_metrics,
        growth_metrics=growth_metrics,
        capital_budget_cents=1000000_00
    )

    assert full_res["opportunity_decision"]["decision"] == "COMMIT"
    assert full_res["allocated_budget_cents"] == 800000_00
    assert len(full_res["anomalies_detected"]) == 1
