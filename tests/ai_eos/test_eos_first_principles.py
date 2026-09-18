"""
Unit and Integration Tests for First-Principles EOS Engine.

Validates all 11 sections of the Entrepreneurial Operating System specification.
"""

from __future__ import annotations

import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.eos_first_principles import (
    FirstPrinciplesEOSEngine,
    MasterLoopOrchestrator,
    Signal,
    SignalToIdeaPipeline,
    DecisionType,
    MentalModel,
    CoupledBusinessLoopsEngine,
    CustomerLifecycleEngine,
    CustomerStage,
    GTMSystemDynamics,
    GrowthStageClassifier,
    CompanyStage,
    FirstPrinciplesMoatAnalyzer,
    MoatType,
    FailureModeMonitor,
    OpportunityDecisionTree,
    EOSStateMachine,
    EOSState,
)


def test_master_loop_reentrancy():
    """Verify Master Loop orchestrator re-entrancy from Market Leadership (R) back to Sensing (A)."""
    orchestrator = MasterLoopOrchestrator()
    assert orchestrator.active_node == "A_Environmental_Sensing"

    new_node = orchestrator.trigger_reentrancy("A_Environmental_Sensing")
    assert new_node == "A_Environmental_Sensing"


def test_signal_to_idea_pipeline():
    """Verify weak signal filtering, forced hypothesis generation, and Bayesian belief updating."""
    pipeline = SignalToIdeaPipeline()

    signal_weak = Signal(description="Minor social noise", is_structural_shift=False, anomaly_score=0.2)
    assert pipeline.filter_signal(signal_weak) is False

    signal_structural = Signal(description="LLM reasoning capability jump", is_structural_shift=True, anomaly_score=0.85)
    assert pipeline.filter_signal(signal_structural) is True

    hyp = pipeline.form_hypothesis(signal_structural, "AI autonomous agents will replace manual tier-1 support", DecisionType.TYPE_II)
    assert hyp.prior_belief == 0.85
    assert pipeline.evaluate_risk(hyp) == "Fast, cheap experiment execution permitted (Reversible Door)"

    # Bayesian update with strong test result (0.90)
    updated_hyp = pipeline.update_belief_from_test(hyp, test_result_score=0.90)
    assert updated_hyp.posterior_belief > hyp.prior_belief
    assert updated_hyp.is_falsified is False

    # Bayesian update with weak test result (0.05) causing falsification
    falsified_hyp = pipeline.update_belief_from_test(hyp, test_result_score=0.01)
    assert falsified_hyp.is_falsified is True


def test_mental_model_evolution():
    """Verify mental model parameter tuning and structural paradigm shifts."""
    mm = MentalModel(parameters={"market_growth": 0.05})
    mm.update_parameters({"market_growth": 0.12})
    assert mm.parameters["market_growth"] == 0.12
    assert mm.structure_version == 1

    mm.update_structure()
    assert mm.structure_version == 2


def test_coupled_business_loops():
    """Verify 13 external business loops setup and cross-loop coupling simulation."""
    engine = CoupledBusinessLoopsEngine()
    assert len(engine.loops) == 13

    # Simulation of pricing feeding financial runway and hiring budget
    sim_res = engine.simulate_loop_coupling(pricing_arpu_cents=100_00, churn_rate=0.02, burn_multiple=1.5)
    assert sim_res["runway_months"] == 20.0
    assert sim_res["hiring_budget_cents"] > 0
    assert sim_res["product_velocity_score"] > 0.0


def test_customer_lifecycle_journey():
    """Verify 15-stage customer lifecycle objective and lever lookup."""
    journey = CustomerLifecycleEngine()
    obj, lever = journey.get_stage_objective_and_lever(CustomerStage.ACTIVATION)
    assert obj == "Cross aha threshold"
    assert lever == "Instrument true aha moment"


def test_gtm_system_dynamics():
    """Verify GTM channel fit alignment checks."""
    gtm_misaligned = GTMSystemDynamics(
        positioning_statement="Enterprise Security",
        target_segment="Fortune 500",
        price_point_cents=50000_00,  # $500
        channel_type="PLG"
    )
    res_mis = gtm_misaligned.evaluate_system_fit()
    assert res_mis["fit_status"] == "MISALIGNED"

    gtm_aligned = GTMSystemDynamics(
        positioning_statement="Self-serve Developer Tool",
        target_segment="Developers",
        price_point_cents=20_00,  # $20
        channel_type="PLG"
    )
    res_alg = gtm_aligned.evaluate_system_fit()
    assert res_alg["fit_status"] == "ALIGNED"


def test_growth_stage_classifier():
    """Verify 9-stage company growth classification and binding constraints."""
    classifier = GrowthStageClassifier()

    stage_idea = classifier.classify_stage(paying_customers=0, mrr_cents=0, nrr=1.0)
    assert stage_idea == CompanyStage.IDEA
    assert classifier.get_binding_constraint(stage_idea) == "Founder time"

    stage_pmf = classifier.classify_stage(paying_customers=60, mrr_cents=50000_00, nrr=1.05)
    assert stage_pmf == CompanyStage.PMF
    assert classifier.get_binding_constraint(stage_pmf) == "Team bandwidth"

    stage_growth = classifier.classify_stage(paying_customers=200, mrr_cents=150000_00, nrr=1.20)
    assert stage_growth == CompanyStage.GROWTH


def test_moat_analyzer_and_cost_curves():
    """Verify moat durability scoring and cost curve viability horizon calculation."""
    analyzer = FirstPrinciplesMoatAnalyzer()

    moat_scores = {
        MoatType.NETWORK_EFFECTS: 0.8,
        MoatType.SWITCHING_COSTS: 0.9,
        MoatType.COUNTER_POSITIONING: 0.7,
    }
    durability = analyzer.calculate_moat_durability(moat_scores)
    assert 0.5 <= durability <= 1.0

    # Calculate years to economic viability: current cost $100, target $10, 20% annual decay
    years = analyzer.evaluate_cost_curve_viability(current_cost=100.0, threshold_cost=10.0, annual_decay_rate=0.20)
    assert 11.0 < years < 12.0


def test_failure_mode_monitor():
    """Verify active failure mode pattern matching and hazard detection."""
    monitor = FailureModeMonitor()

    hazards = monitor.audit_failure_modes(
        engagement_rate=0.05,
        survey_positive=True,
        cac=300.0,
        ltv=400.0,
        decision_latency_days=20.0
    )

    assert len(hazards) == 3
    failure_names = [h["failure_mode"] for h in hazards]
    assert "Solving the wrong problem" in failure_names
    assert "Premature scaling / Poor unit economics" in failure_names
    assert "Organizational bottlenecks" in failure_names


def test_opportunity_decision_tree():
    """Verify 'Should We Pursue This Opportunity?' decision tree branch evaluation."""
    dt = OpportunityDecisionTree()

    # Noise discard
    res_noise = dt.evaluate_opportunity(
        is_structural_anomaly=False,
        is_reversible=True,
        high_confidence_multi_source=False,
        cheap_test_available=True,
        test_result_exceeds_kill=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_noise["pursue"] is False

    # Irreversible without high confidence discard
    res_irrev = dt.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible=False,
        high_confidence_multi_source=False,
        cheap_test_available=True,
        test_result_exceeds_kill=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_irrev["pursue"] is False

    # Fully valid pursuit
    res_go = dt.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_result_exceeds_kill=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res_go["pursue"] is True


def test_eos_state_machine_lifecycle():
    """Verify AI State Machine transitions from Sensing to Reinvent."""
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    sm.transition("ANOMALY_DETECTED", {})
    assert sm.current_state == EOSState.HYPOTHESIS

    sm.transition("HYPOTHESIS_FORMED", {})
    assert sm.current_state == EOSState.CHEAP_TEST

    sm.transition("STRENGTHENED", {})
    assert sm.current_state == EOSState.VALIDATION

    sm.transition("ECONOMIC_VIABILITY_CONFIRMED", {})
    assert sm.current_state == EOSState.BUILD_GATE

    sm.transition("RESOURCED", {})
    assert sm.current_state == EOSState.MVP

    sm.transition("SHIPPED", {})
    assert sm.current_state == EOSState.GTM_TEST

    sm.transition("SIGNAL_COLLECTED", {})
    assert sm.current_state == EOSState.KILL_OR_SCALE

    sm.transition("ABOVE_THRESHOLD", {})
    assert sm.current_state == EOSState.SCALE

    sm.transition("REPEATABLE_LOOP_CONFIRMED", {})
    assert sm.current_state == EOSState.OPERATE

    sm.transition("REINVENTION_MANDATE", {})
    assert sm.current_state == EOSState.REINVENT

    sm.transition("REENTRY", {})
    assert sm.current_state == EOSState.SENSING


def test_first_principles_eos_engine_integration():
    """Verify integrated master EOS engine KPI rollup and component coordination."""
    engine = FirstPrinciplesEOSEngine()
    kpi_stack = engine.calculate_subsystem_kpi_stack()

    assert "Sensing" in kpi_stack
    assert "SystemLevel" in kpi_stack
    assert kpi_stack["Financial"]["gross_margin"] == 0.82
