"""Tests for First-Principles Entrepreneurial Operating System (EOS) Engines."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    LoopTimescale,
    FeedbackLoop,
    MasterLoopNode,
    MasterLoopOrchestrator,
    RiskType,
    Anomaly,
    FalsifiableHypothesis,
    CognitiveDecisionEngine,
    MentalModel,
    BusinessLoopType,
    ExternalBusinessLoopsEngine,
    LifecycleStage,
    CustomerLifecycleEngine,
    GTMMotion,
    GTMSystemEngine,
    CompanyStage,
    CompanyGrowthStateMachine,
    StrategicInitiative,
    StrategicCapitalAllocator,
    FailureModeMonitor,
    AISystemState,
    EOSOpportunityDecisionTree,
    EntrepreneurialOperatingSystemFirstPrinciples,
)


def test_master_loop_orchestrator():
    orchestrator = MasterLoopOrchestrator()
    assert orchestrator.current_node == MasterLoopNode.SENSING

    # Test standard transition
    next_node = orchestrator.transition(MasterLoopNode.SIGNAL_COLLECTION)
    assert next_node == MasterLoopNode.SIGNAL_COLLECTION

    # Test kill signal transition
    orchestrator.transition(MasterLoopNode.VALIDATION)
    reentrant_node = orchestrator.transition(MasterLoopNode.BUSINESS_MODEL, kill_signal="customer_validation_failed")
    assert reentrant_node == MasterLoopNode.OPPORTUNITY_DISCOVERY
    assert len(orchestrator.kill_signals_triggered) == 1


def test_feedback_loop_timescales():
    loop = FeedbackLoop(
        loop_id="loop_1",
        name="Ad experiment loop",
        timescale=LoopTimescale.FAST,
        cycle_time_days=3.0,
        signal_fidelity=0.9
    )
    fidelity = loop.execute_cycle(feedback_quality=0.8)
    assert fidelity > 0.8
    assert loop.is_compounding is True

    # Low feedback quality breaks compounding
    for _ in range(5):
        loop.execute_cycle(feedback_quality=0.1)
    assert loop.is_compounding is False


def test_cognitive_decision_engine():
    engine = CognitiveDecisionEngine()

    # 1. Anomaly detection
    anomaly = engine.detect_anomaly("CUDA general compute demand spike", observed=100.0, expected=10.0)
    assert anomaly.surprise_score > 2.0
    assert anomaly.is_structural_shift is True

    # 2. Hypothesis formation
    hyp = engine.form_hypothesis(
        claim="Streaming becomes viable if broadband > 50%",
        falsification_condition="CAC > $100 or buffering > 5%",
        kill_threshold=50.0,
        prior_belief=0.5,
        risk_type=RiskType.TYPE_II,
        cheap_test_cost_usd=500.0
    )
    assert hyp.risk_type == RiskType.TYPE_II

    # 3. Test result update
    updated_hyp = engine.update_belief_with_test_result(hyp.hypothesis_id, observed_metric=80.0)
    assert updated_hyp.posterior_belief > 0.5
    assert updated_hyp.is_falsified is False

    # 4. Falsification trigger
    falsified_hyp = engine.update_belief_with_test_result(hyp.hypothesis_id, observed_metric=20.0)
    assert falsified_hyp.is_falsified is True
    assert falsified_hyp.posterior_belief == 0.0


def test_mental_model_evolution():
    model = MentalModel(
        model_name="SaaS direct sales model",
        structure_version=1,
        parameters={"conversion_rate": 0.05}
    )

    # Parameter update
    model.update_parameters({"conversion_rate": 0.08})
    assert model.parameters["conversion_rate"] == 0.08

    # Ossification check
    assert model.check_ossification(consecutive_contradictions=3) is True

    # Structural update resets ossification
    model.update_structure(new_version=2, structural_reason="Transition to PLG self-serve")
    assert model.structure_version == 2
    assert model.is_ossified is False


def test_external_business_loops_engine():
    engine = ExternalBusinessLoopsEngine()
    assert len(engine.loops) == 13

    # Verify Product and Financial loop specs exist
    assert BusinessLoopType.PRODUCT in engine.loops
    assert BusinessLoopType.FINANCIAL in engine.loops

    # Simulate stock and flow coupling
    initial_cash = engine.stocks["cash_usd"]
    new_stocks = engine.simulate_coupled_step(arpu_usd=100.0, monthly_burn_usd=20000.0, new_hires=1)
    assert "cash_usd" in new_stocks
    assert new_stocks["talent_count"] == 11.0


def test_customer_lifecycle_engine():
    engine = CustomerLifecycleEngine()
    conversions = {
        LifecycleStage.AWARENESS: 0.8,
        LifecycleStage.INTEREST: 0.5,
        LifecycleStage.CONSIDERATION: 0.7,
        LifecycleStage.EVALUATION: 0.6,
        LifecycleStage.PURCHASE: 0.4,
        LifecycleStage.ONBOARDING: 0.9,
        LifecycleStage.ACTIVATION: 0.5,  # Big dropoff
        LifecycleStage.ENGAGEMENT: 0.8,
        LifecycleStage.HABIT_FORMATION: 0.8,
        LifecycleStage.RETENTION: 0.8,
        LifecycleStage.LOYALTY: 0.9,
        LifecycleStage.ADVOCACY: 0.7,
        LifecycleStage.REFERRAL: 0.6,
        LifecycleStage.EXPANSION: 0.7,
        LifecycleStage.REPURCHASE: 0.9,
    }

    results = engine.analyze_cohort_conversion(initial_cohort_size=10000, stage_conversions=conversions)
    assert "stage_counts" in results
    assert results["primary_bottleneck_stage"] == LifecycleStage.PURCHASE.value or results["primary_bottleneck_stage"] == LifecycleStage.ACTIVATION.value


def test_gtm_system_engine():
    engine = GTMSystemEngine()

    # Self-serve low complexity
    plg_result = engine.evaluate_gtm_fit(complexity="low", price_point_annual_usd=1200.0, network_effects=True)
    assert GTMMotion.PLG.value in plg_result["recommended_motions"]
    assert GTMMotion.CLG.value in plg_result["recommended_motions"]

    # High complexity enterprise
    enterprise_result = engine.evaluate_gtm_fit(complexity="high", price_point_annual_usd=100000.0, network_effects=False)
    assert GTMMotion.SLG.value in enterprise_result["recommended_motions"]


def test_company_growth_state_machine():
    sm = CompanyGrowthStateMachine()
    assert sm.current_stage == CompanyStage.IDEA

    # Premature scaling check
    is_premature, msg = sm.check_premature_scaling(retention_curve_flattens=False, cac_payback_months=24.0, stage=CompanyStage.GROWTH)
    assert is_premature is True
    assert "PREMATURE SCALING WARNING" in msg

    # Transition with healthy metrics succeeds
    next_stage = sm.transition_stage(target_stage=CompanyStage.VALIDATION, retention_flattens=True, cac_payback=6.0)
    assert next_stage == CompanyStage.VALIDATION


def test_strategic_capital_allocator():
    allocator = StrategicCapitalAllocator()
    initiatives = [
        StrategicInitiative("init_1", "High ROI PLG motion", expected_return_usd=500000.0, required_capital_usd=100000.0, confidence_score=0.9),
        StrategicInitiative("init_2", "Low ROI initiative", expected_return_usd=200000.0, required_capital_usd=100000.0, confidence_score=0.4),
        StrategicInitiative("init_3", "Huge ROI platform bet", expected_return_usd=1000000.0, required_capital_usd=150000.0, confidence_score=0.8),
    ]

    allocation = allocator.rank_initiatives(initiatives, budget_usd=250000.0)
    assert len(allocation["funded_initiatives"]) == 2
    assert "High ROI PLG motion" in allocation["funded_initiatives"]
    assert "Huge ROI platform bet" in allocation["funded_initiatives"]


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()
    alerts = monitor.audit_metrics(
        retention_flattens=False,
        cac_to_ltv_ratio=0.8,
        decision_latency_days=20.0,
        build_vs_demand_ratio=4.0
    )
    assert len(alerts) >= 3
    failure_names = [a["failure_mode"] for a in alerts]
    assert "Lack of product-market fit" in failure_names
    assert "Organizational bottlenecks" in failure_names


def test_eos_opportunity_decision_tree():
    tree = EOSOpportunityDecisionTree()

    # Noise discarded at Q1
    res1 = tree.evaluate(
        is_structural_anomaly=False,
        is_reversible_decision=True,
        high_confidence_multi_source_signal=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        structural_advantage_possible=True
    )
    assert res1["pursue"] is False
    assert "Q1" in res1["reason"]

    # Successful pursuit
    res2 = tree.evaluate(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        high_confidence_multi_source_signal=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        structural_advantage_possible=True
    )
    assert res2["pursue"] is True


def test_unified_first_principles_system():
    system = EntrepreneurialOperatingSystemFirstPrinciples()

    output = system.process_opportunity(
        description="AWS elastic cloud compute anomaly",
        observed_metric=1000.0,
        expected_metric=10.0,
        cheap_test_cost_usd=1000.0,
        test_result=95.0,
        kill_threshold=50.0,
        structural_advantage=True
    )

    assert output["ai_state"] == AISystemState.SCALE.value
    assert output["decision"]["pursue"] is True
