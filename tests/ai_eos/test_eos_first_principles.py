"""
Unit & Integration tests for the first-principles Entrepreneurial Operating System (EOS) engine.
"""

import pytest
from uuid import uuid4
from apodex.ai_eos.intelligence.eos_first_principles import (
    RiskType,
    GrowthStage,
    EOSState,
    AnomalySignal,
    FalsifiableHypothesis,
    MultiTimescaleLoopEngine,
    SignalToHypothesisFilter,
    MentalModelEvolutionEngine,
    CoupledBusinessLoopsEngine,
    CustomerJourneySimulator,
    IntegratedGTMSystem,
    VentureGrowthStateMachine,
    StrategicThinkingEngine,
    FailureModeDiagnosticMonitor,
    AutonomousAIOrchestrator,
)


def test_multi_timescale_loop_engine():
    engine = MultiTimescaleLoopEngine()
    fast_res = engine.step_fast_loop(5)
    medium_res = engine.step_medium_loop(2)
    slow_res = engine.step_slow_loop(1)

    assert fast_res["velocity_score"] == 5
    assert medium_res["velocity_score"] == 2
    assert slow_res["velocity_score"] == 1
    assert engine.fast_loop_count == 5


def test_signal_filter_and_risk_type():
    filter_engine = SignalToHypothesisFilter()

    # Noise signal
    noise = AnomalySignal(description="Random spike", is_structural_shift=False)
    assert filter_engine.evaluate_signal(noise) is None

    # Structural signal - Type II reversible
    structural_type2 = AnomalySignal(
        description="Internet traffic 100% YoY",
        is_structural_shift=True,
        confidence=0.85,
        metadata={"is_irreversible": False, "cheap_test_cost_cents": 2000_00}
    )
    hyp2 = filter_engine.evaluate_signal(structural_type2)
    assert hyp2 is not None
    assert hyp2.risk_type == RiskType.TYPE_II
    assert hyp2.cheap_test_cost_cents == 2000_00

    # Structural signal - Type I irreversible
    structural_type1 = AnomalySignal(
        description="Regulatory compliance binding contract",
        is_structural_shift=True,
        confidence=0.90,
        metadata={"is_irreversible": True}
    )
    hyp1 = filter_engine.evaluate_signal(structural_type1)
    assert hyp1 is not None
    assert hyp1.risk_type == RiskType.TYPE_I


def test_mental_model_evolution_paradigm_shift():
    model = MentalModelEvolutionEngine()

    # Confirmed predictions
    res1 = model.update_model(empirical_evidence_supports=True)
    assert res1["action"] == "parameter_updated"
    assert model.parameter_tune_count == 1

    # Contradictions -> structural shift
    model.update_model(empirical_evidence_supports=False)
    model.update_model(empirical_evidence_supports=False)
    res_shift = model.update_model(empirical_evidence_supports=False)
    assert res_shift["action"] == "structural_paradigm_shift"
    assert res_shift["version"] == 2


def test_coupled_business_loops():
    loops = CoupledBusinessLoopsEngine()
    initial_cash = loops.cash_cents
    res = loops.execute_coupled_step(R_and_D_budget_cents=50000_00, marketing_spend_cents=50000_00)

    assert "cash_cents" in res
    assert "monthly_revenue_cents" in res
    assert res["kpis"]["cs_nrr"] == 1.15


def test_customer_journey_and_gtm():
    journey = CustomerJourneySimulator()
    sim_res = journey.simulate_funnel(initial_reach=10000, stage_conversions=[])

    assert "Awareness" in sim_res["stage_counts"]
    assert "Repurchase" in sim_res["stage_counts"]
    assert sim_res["stage_counts"]["Awareness"] == 10000

    gtm = IntegratedGTMSystem()
    plg_motion = gtm.evaluate_motion_fit(acv_cents=1000_00, complexity_score=0.1)
    enterprise_motion = gtm.evaluate_motion_fit(acv_cents=100000_00, complexity_score=0.9)

    assert "PLG" in plg_motion
    assert "Enterprise" in enterprise_motion


def test_growth_state_machine_and_moat_scoring():
    sm = VentureGrowthStateMachine()
    assert sm.current_stage == GrowthStage.IDEA

    assert sm.transition_stage(GrowthStage.VALIDATION, criteria_met=True) is True
    assert sm.current_stage == GrowthStage.VALIDATION

    assert sm.transition_stage(GrowthStage.GROWTH, criteria_met=False) is False
    assert sm.current_stage == GrowthStage.VALIDATION

    strategic = StrategicThinkingEngine()
    moats = strategic.evaluate_moats(
        network_density=0.8, switching_cost_cents=5000_00, economies_of_scale=0.6,
        brand_trust=0.9, regulatory_ip=0.7, counter_positioning=0.9
    )
    assert moats["durability_score"] > 0.6
    assert strategic.project_enabling_cost_curve(current_cost=100.0, annual_decay_rate=0.2, target_threshold=50.0) == 4


def test_failure_mode_diagnostics():
    monitor = FailureModeDiagnosticMonitor()
    metrics = {
        "retention_curve_flattens": False,
        "growth_spend_cents": 500000_00,
        "decision_latency_days": 20,
        "ignoring_disconfirming_data": True
    }
    warnings = monitor.diagnose_failures(metrics)
    assert "lack_of_pmf" in warnings
    assert "org_bottlenecks" in warnings
    assert "founder_bias" in warnings


def test_autonomous_ai_orchestrator():
    orchestrator = AutonomousAIOrchestrator()

    # Test Pursue Decision Tree - Discard Noise
    noise_signal = AnomalySignal(description="Market noise", is_structural_shift=False)
    res_noise = orchestrator.run_execution_cycle(noise_signal)
    assert res_noise["state"] == EOSState.DISCARD

    # Test Full Execution Cycle
    valid_signal = AnomalySignal(
        description="GenAI cost curve crossing feasibility threshold",
        is_structural_shift=True,
        confidence=0.85,
        metadata={
            "is_irreversible": False,
            "cheap_test_cost_cents": 2000_00,
            "acv_cents": 1200_00,
            "complexity_score": 0.1,
            "structural_advantage_potential": True
        }
    )
    res_valid = orchestrator.run_execution_cycle(valid_signal)
    assert res_valid["state"] == EOSState.SCALE
    assert "PLG" in res_valid["gtm_motion"]
    assert res_valid["kpis"]["moat_durability"] > 0
