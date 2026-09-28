"""Unit and integration tests for the First-Principles Entrepreneurial Operating System (EOS) engine."""

import pytest
from apodex.ai_eos.intelligence import (
    EOSEngineFirstPrinciples,
    SignalAnomalyDetector,
    MentalModelEvolutionEngine,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GTMSystemSimulator,
    CompanyGrowthStateMachine,
    StrategicMoatEngine,
    FailureModeMonitor,
    EOSOpportunityDecisionTree,
    GrowthStage,
    SystemState,
    RiskType,
    DecisionOutcome,
)


def test_signal_anomaly_detector_type_ii_cheap_test():
    detector = SignalAnomalyDetector(sensitivity=0.70)
    signal = {
        "name": "GPU cost drop 50%",
        "deviation": 0.80,
        "structural_confidence": 0.75,
        "irreversible": False,
    }
    res = detector.evaluate_signal(signal)
    assert res["is_anomaly"] is True
    assert res["is_structural"] is True
    assert res["risk_type"] == RiskType.TYPE_II.value
    assert res["recommended_action"] == DecisionOutcome.CHEAP_TEST.value


def test_signal_anomaly_detector_type_i_unverified():
    detector = SignalAnomalyDetector(sensitivity=0.70)
    signal = {
        "name": "New regulatory law proposed",
        "deviation": 0.90,
        "structural_confidence": 0.85,
        "irreversible": True,
        "multi_source_verified": False,
    }
    res = detector.evaluate_signal(signal)
    assert res["risk_type"] == RiskType.TYPE_I.value
    assert res["recommended_action"] == DecisionOutcome.DISCARD.value


def test_mental_model_evolution_paradigm_shift():
    engine = MentalModelEvolutionEngine(initial_structure={"paradigm": "web2_saas"})
    # 3 major contradictions trigger structural paradigm shift
    r1 = engine.process_feedback("market_growth_rate", expected_val=0.50, actual_val=0.05)
    assert r1 == "contradiction_recorded"
    r2 = engine.process_feedback("market_growth_rate", expected_val=0.50, actual_val=0.05)
    assert r2 == "contradiction_recorded"
    r3 = engine.process_feedback("market_growth_rate", expected_val=0.50, actual_val=0.05)
    assert r3 == "structural_paradigm_shift"
    assert engine.paradigm_shifts == 1


def test_external_business_loops_coupling():
    loops = ExternalBusinessLoopsEngine()
    initial_cash = loops.stocks["cash_cents"]
    initial_exp = loops.loop_kpis["innovation_experiments_run"]

    res = loops.execute_coupled_cycle(R_and_D_investment_cents=50000_00)
    assert res["loop_kpis"]["innovation_experiments_run"] == initial_exp + 1.0
    assert "cash_cents" in res["stocks"]


def test_customer_lifecycle_simulation_and_levers():
    lifecycle = CustomerLifecycleEngine()
    funnel = lifecycle.simulate_funnel(initial_awareness=1000)
    assert funnel["awareness"] == 1000
    assert funnel["interest"] == 100
    assert "activation" in funnel

    lever = lifecycle.optimize_lever("activation")
    assert "aha" in lever.lower()


def test_gtm_system_simulator():
    sim = GTMSystemSimulator()

    # Enterprise high-complexity
    res_ent = sim.evaluate_motion_fit(acv_cents=150000_00, complexity_score=0.85)
    assert "Sales-Led Growth" in res_ent["primary_motion"]

    # PLG low-complexity
    res_plg = sim.evaluate_motion_fit(acv_cents=3000_00, complexity_score=0.20)
    assert "Product-Led Growth" in res_plg["primary_motion"]


def test_company_growth_state_machine_transitions():
    sm = CompanyGrowthStateMachine()
    assert sm.current_stage == GrowthStage.IDEA

    # Transition to Validation
    stage, adv = sm.evaluate_stage_transition({"validated_learnings": 6})
    assert adv is True
    assert stage == GrowthStage.VALIDATION

    # Transition to Startup
    stage, adv = sm.evaluate_stage_transition({"paying_customers": 4})
    assert adv is True
    assert stage == GrowthStage.STARTUP


def test_strategic_moats_and_cost_curves():
    moat = StrategicMoatEngine()

    powers = {
        "network_effects": 0.8,
        "switching_costs": 0.9,
        "cornered_resource": 0.7,
        "scale_economies": 0.6,
        "counter_positioning": 0.8,
        "brand": 0.5,
        "process_power": 0.5,
    }
    score = moat.calculate_7_powers_score(powers)
    assert 0.65 <= score <= 0.75

    # Cost curve crossing
    years = moat.evaluate_cost_curve_crossing(
        current_unit_cost=100.0,
        cost_decline_rate_per_year=0.20,
        viability_threshold=20.0
    )
    assert 7.0 <= years <= 8.0


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()

    metrics = {
        "cac_cents": 5000_00,
        "ltv_cents": 8000_00,  # LTV/CAC = 1.6 (< 2.0)
        "growth_rate_mom": 0.35,  # scaling fast (> 0.30)
        "decision_latency_days": 20  # bottleneck
    }

    warnings = monitor.audit_operating_metrics(metrics)
    modes = [w["failure_mode"] for w in warnings]
    assert "Premature Scaling" in modes
    assert "Organizational Bottlenecks" in modes


def test_eos_opportunity_decision_tree():
    tree = EOSOpportunityDecisionTree()

    # Cheap test path
    res = tree.evaluate_opportunity({
        "is_structural_anomaly": True,
        "is_reversible": True,
        "cheap_test_available": True
    })
    assert res["outcome"] == DecisionOutcome.CHEAP_TEST.value

    # Commit resources path
    res2 = tree.evaluate_opportunity({
        "is_structural_anomaly": True,
        "is_reversible": False,
        "multi_source_verified": True,
        "structural_advantage_possible": True
    })
    assert res2["outcome"] == DecisionOutcome.COMMIT_RESOURCES.value


def test_eos_engine_first_principles_orchestrator():
    orchestrator = EOSEngineFirstPrinciples()

    # Fast loop
    fast_res = orchestrator.run_fast_loop({
        "name": "Generative AI cost crash",
        "deviation": 0.88,
        "structural_confidence": 0.90,
        "irreversible": False
    })
    assert orchestrator.current_state == SystemState.CHEAP_TEST
    assert "hypothesis" in fast_res

    # Medium loop
    med_res = orchestrator.run_medium_loop(
        gtm_input={"acv_cents": 20000_00, "complexity_score": 0.40},
        operating_metrics={"validated_learnings": 10, "decision_latency_days": 3}
    )
    assert "gtm_fit" in med_res
    assert "funnel" in med_res

    # Slow loop
    slow_res = orchestrator.run_slow_loop({
        "network_effects": 0.9,
        "switching_costs": 0.9,
        "cornered_resource": 0.8,
        "scale_economies": 0.8,
        "counter_positioning": 0.8,
        "brand": 0.7,
        "process_power": 0.7,
    })
    assert slow_res["moat_score"] > 0.75
    assert slow_res["action"] == "Defend & Extend Category"
