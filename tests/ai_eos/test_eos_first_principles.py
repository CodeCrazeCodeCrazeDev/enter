"""Unit and integration test suite for the Entrepreneurial Operating System (EOS) First-Principles Engine.
"""

from __future__ import annotations

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    LoopTimescale,
    CoupledFeedbackLoop,
    MasterLoopNode,
    MasterLoopOrchestrator,
    RiskType,
    CognitiveSignalToIdeaPipeline,
    MentalModel,
    BusinessLoopType,
    BusinessLoopState,
    CoupledBusinessSystemEngine,
    CustomerJourneyStage,
    CustomerCohort,
    PositioningStrategy,
    PricingMotion,
    GTMIntegratedSystem,
    GrowthStage,
    CompanyGrowthTracker,
    MoatType,
    MoatEvaluator,
    CostCurveAnalysis,
    CapitalOpportunityCostAllocator,
    FailureMode,
    FailureModeDiagnostics,
    get_scientific_foundations,
    DecisionTreeResult,
    OpportunityDecisionTree,
    AIEOSSubsystemState,
    FullAIEOSSystemOrchestrator
)


def test_section_0_loop_timescales():
    loop = CoupledFeedbackLoop(
        loop_id="loop_1",
        name="Ad Test",
        timescale=LoopTimescale.FAST,
        velocity_days=7.0,
        signal_fidelity=0.9
    )
    assert loop.evaluate_compounding(retention_delta=0.05, unit_economics_ratio=3.0) is True
    assert loop.evaluate_compounding(retention_delta=-0.01, unit_economics_ratio=0.5) is False


def test_section_1_master_loop_orchestrator():
    orchestrator = MasterLoopOrchestrator()
    assert orchestrator.current_node == MasterLoopNode.A_ENVIRONMENTAL_SENSING

    # Test kill signal routing
    node = orchestrator.evaluate_kill_and_feedback_signals("validation_kill", metric_value=0.1)
    assert node == MasterLoopNode.D_OPPORTUNITY_DISCOVERY

    node_gtm = orchestrator.evaluate_kill_and_feedback_signals("weak_gtm", metric_value=0.5)
    assert node_gtm == MasterLoopNode.J_GTM_SYSTEM


def test_section_2_cognitive_pipeline_and_mental_models():
    pipeline = CognitiveSignalToIdeaPipeline(
        raw_signal="100x surge in bandwidth demand",
        is_structural_anomaly=True
    )
    assert pipeline.evaluate_anomaly(is_structural=True) is True
    claim = pipeline.form_hypothesis("Streaming becomes viable if broadband > 50%")
    assert "Streaming" in claim

    outcome = pipeline.run_cheap_test(test_cost_usd=500.0, observed_outcome_positive=True, effect_size=0.3)
    assert outcome == "strengthened"
    assert pipeline.belief_confidence > 0.5

    assert pipeline.classify_risk(is_reversible=True) == RiskType.TYPE_II
    assert pipeline.classify_risk(is_reversible=False) == RiskType.TYPE_I

    # Mental Model Ossification
    mm = MentalModel(
        model_id="mm_1",
        name="DVD Rental Model",
        parameters={"late_fee_revenue_pct": 0.3},
        structural_assumptions=["Physical distribution is required"]
    )
    assert mm.detect_ossification(contradiction_count=3) is True


def test_section_3_coupled_business_loops():
    engine = CoupledBusinessSystemEngine()
    loop_state = BusinessLoopState(
        loop_type=BusinessLoopType.PRICING,
        inputs={"wtp": 100},
        outputs={"arpu": 50},
        feedback_signal={"conversion": 0.1},
        core_kpi=50.0
    )
    engine.register_loop(BusinessLoopType.PRICING, loop_state)

    res = engine.simulate_coupled_step(arpu_usd=100.0, cac_usd=200.0, churn_rate=0.02)
    assert res["mrr"] > 0
    assert "cash_usd" in res


def test_section_4_customer_journey():
    cohort = CustomerCohort(cohort_id="c_2026", size=1000, active_count=1000)
    assert cohort.advance_stage(CustomerJourneyStage.ACTIVATION, 0.4) == CustomerJourneyStage.ACTIVATION
    assert cohort.active_count == 400

    assert cohort.evaluate_aha_activation(0.5) is True
    assert cohort.compute_viral_k_factor(invites_per_user=5.0, invite_conversion_rate=0.3) == 1.5


def test_section_5_gtm_integrated_system():
    pos = PositioningStrategy(
        category_name="Developer Security",
        target_segment="Enterprise Devs",
        comparison_axis="Automated Static Analysis",
        value_proposition="Zero-config vulnerability remediation"
    )

    gtm_plg = GTMIntegratedSystem(
        positioning=pos,
        pricing_motion=PricingMotion.SELF_SERVE_PLG,
        acv_usd=1000.0,
        cac_usd=300.0,
        sales_cycle_days=1
    )
    assert gtm_plg.validate_channel_fit() is True
    payback = gtm_plg.calculate_payback_period_months(gross_margin_percent=80.0)
    assert payback < 12.0

    gtm_invalid = GTMIntegratedSystem(
        positioning=pos,
        pricing_motion=PricingMotion.SELF_SERVE_PLG,
        acv_usd=20000.0,
        cac_usd=15000.0,
        sales_cycle_days=180
    )
    assert gtm_invalid.validate_channel_fit() is False


def test_section_6_company_growth_system():
    tracker = CompanyGrowthTracker(stage=GrowthStage.IDEA, paying_customers=10)
    assert tracker.evaluate_stage_transition() == GrowthStage.VALIDATION

    tracker.stage = GrowthStage.GROWTH
    tracker.retention_curve_flattened = False
    assert tracker.detect_premature_scaling(cac_payback_months=12.0) is True


def test_section_7_strategic_thinking_moats_and_capital():
    moat = MoatEvaluator(
        moat_type=MoatType.NETWORK_EFFECTS,
        network_density=0.8,
        switching_cost_usd=5000.0,
        relative_cost_advantage_pct=25.0,
        brand_trust_score=0.9
    )
    durability = moat.compute_durability_score()
    assert 0.0 <= durability <= 1.0

    cost_curve = CostCurveAnalysis(
        technology_domain="Batteries",
        cost_per_unit_historical=[(2020, 150.0), (2024, 100.0)],
        viability_threshold_cost=75.0
    )
    year = cost_curve.predict_viability_year()
    assert year is not None and year > 2024

    initiatives = [
        {"name": "Init A", "expected_value_usd": 100000, "success_probability": 0.5, "capital_required_usd": 10000},
        {"name": "Init B", "expected_value_usd": 500000, "success_probability": 0.8, "capital_required_usd": 20000}
    ]
    ranked = CapitalOpportunityCostAllocator.rank_initiatives(initiatives)
    assert ranked[0]["name"] == "Init B"


def test_section_8_failure_mode_diagnostics():
    metrics = {
        "engagement_rate": 0.05,
        "survey_satisfaction": 0.9,
        "retention_curve_slope": -0.8
    }
    warnings = FailureModeDiagnostics.audit_operating_metrics(metrics)
    assert len(warnings) >= 2
    failure_types = [w[0] for w in warnings]
    assert FailureMode.SOLVING_WRONG_PROBLEM in failure_types
    assert FailureMode.LACK_OF_PMF in failure_types


def test_section_9_scientific_foundations():
    foundations = get_scientific_foundations()
    assert len(foundations) >= 5
    domains = [f.domain for f in foundations]
    assert "Economics" in domains
    assert "Systems Thinking" in domains


def test_section_10_ai_eos_decision_tree_and_orchestrator():
    res = OpportunityDecisionTree.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_result_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert res == DecisionTreeResult.COMMIT_RESOURCES

    orchestrator = FullAIEOSSystemOrchestrator()
    cycle_res = orchestrator.run_full_execution_cycle(metrics={"gtm_quality": 1.5, "decision_latency_days": 2.0})
    assert "current_stage" in cycle_res
    assert cycle_res["master_loop_node"] is not None
