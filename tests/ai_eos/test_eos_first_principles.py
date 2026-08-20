"""
Comprehensive unit and integration test suite for the EOS First-Principles Reconstruction module.
"""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    Timescale,
    RiskType,
    Anomaly,
    Hypothesis,
    MentalModel,
    SignalPipeline,
    BusinessLoopName,
    BusinessLoopRegistry,
    CustomerJourneyStageName,
    CustomerLifecycle,
    GTMSystem,
    ChannelType,
    GrowthStageEnum,
    GrowthClassifier,
    MoatType,
    StrategicMoatAnalyzer,
    FailureModeEnum,
    FailureModeMonitor,
    EOSState,
    EOSStateMachine,
    OpportunityDecisionTree,
    SensingAgent,
    HypothesisEngine,
    ValidationAgent,
    GTMSimulator,
    GrowthStageClassifier,
    MoatAnalyzer,
    FailureModeMonitorAgent,
    CapitalAllocator,
    ReinventionTrigger,
    GovernanceSafetyLayer,
    KPIStack,
)


def test_internal_cognitive_loops():
    model = MentalModel(
        name="Market Model V1",
        parameters={"internet_growth": 0.8},
        structural_assumptions=["broadband_adoption_is_linear"]
    )
    pipeline = SignalPipeline(mental_model=model)

    # Anomaly filtering
    noise_anomaly = Anomaly(
        id="a1",
        description="Minor noise in website visits",
        is_structural_shift=False,
        observed_signal_strength=0.1,
        source="Analytics"
    )
    structural_anomaly = Anomaly(
        id="a2",
        description="Exponential GPU compute demand spike in LLM inference",
        is_structural_shift=True,
        observed_signal_strength=0.95,
        source="Market Trends"
    )

    assert not pipeline.filter_anomaly(noise_anomaly)
    assert pipeline.filter_anomaly(structural_anomaly)

    # Hypothesis formation
    hyp = pipeline.form_hypothesis(
        anomaly_id="a2",
        claim="Demand for specialized inference chips will cross $10B by Q4",
        falsifiable_condition="Inference chip sales revenue",
        kill_threshold_metric="Quarterly chip revenue",
        kill_threshold_value=1000.0,
        estimated_cost=50000.0,
        risk_type=RiskType.TYPE_II
    )

    assert hyp.id == "hyp_1"
    assert hyp.risk_type == RiskType.TYPE_II

    # Falsification test
    strengthened = pipeline.evaluate_test_result("hyp_1", measured_value=1500.0)
    assert strengthened is True

    # Mental model updating
    model.update_parameters("inference_demand", 0.95)
    model.update_structure("inference_demand_is_exponential")
    assert model.parameters["inference_demand"] == 0.95
    assert "inference_demand_is_exponential" in model.structural_assumptions


def test_business_loop_registry():
    registry = BusinessLoopRegistry()
    assert len(registry.loops) == 13

    product_loop = registry.get_loop(BusinessLoopName.PRODUCT)
    assert product_loop.timescale == Timescale.FAST
    assert "Retention curve" in product_loop.core_kpis

    registry.update_loop_kpi(BusinessLoopName.PRODUCT, "NPS", 65.0)
    assert registry.get_loop(BusinessLoopName.PRODUCT).kpi_values["NPS"] == 65.0


def test_customer_lifecycle():
    lifecycle = CustomerLifecycle()
    assert len(lifecycle.stages) == 15

    activation_stage = lifecycle.stages[CustomerJourneyStageName.ACTIVATION]
    assert activation_stage.founder_objective == "Cross the 'aha' threshold"

    lifecycle.set_metric(CustomerJourneyStageName.ACTIVATION, 0.42)
    assert lifecycle.stages[CustomerJourneyStageName.ACTIVATION].current_metric_value == 0.42


def test_gtm_system_channel_recommendation():
    # Low complexity, low price -> PLG
    plg_gtm = GTMSystem(
        positioning="Self-serve developer tool",
        messaging="Build in seconds",
        target_segment="Developers",
        price_point=49.0,
        complexity_score=0.1
    )
    assert plg_gtm.recommend_primary_channel() == ChannelType.PLG

    # High complexity, high price -> SLG
    slg_gtm = GTMSystem(
        positioning="Enterprise compliance platform",
        messaging="Bank-grade security",
        target_segment="Fortune 500 CISOs",
        price_point=100000.0,
        complexity_score=0.9
    )
    assert slg_gtm.recommend_primary_channel() == ChannelType.SLG


def test_growth_stage_classifier():
    stage = GrowthClassifier.classify_stage(
        paying_customers=100,
        retention_curve_flattened=True,
        annual_growth_rate=1.5,
        third_party_developers=10,
        market_share=0.05
    )
    assert stage == GrowthStageEnum.GROWTH

    platform_stage = GrowthClassifier.classify_stage(
        paying_customers=1000,
        retention_curve_flattened=True,
        annual_growth_rate=0.5,
        third_party_developers=100,
        market_share=0.15
    )
    assert platform_stage == GrowthStageEnum.PLATFORM


def test_strategic_moat_analyzer():
    analyzer = StrategicMoatAnalyzer(
        active_moats={
            MoatType.NETWORK_EFFECTS: 0.8,
            MoatType.SWITCHING_COSTS: 0.9,
            MoatType.BRAND: 0.7
        }
    )
    assert pytest.approx(analyzer.evaluate_durability(), 0.01) == 0.8


def test_failure_mode_monitor():
    monitor = FailureModeMonitor()
    alerts = monitor.scan_metrics(
        survey_vs_usage_gap=0.7,
        build_velocity_high_demand_flat=True,
        decision_latency_days=20.0
    )
    assert len(alerts) == 3
    failure_types = {a.failure_mode for a in alerts}
    assert FailureModeEnum.SOLVING_WRONG_PROBLEM in failure_types
    assert FailureModeEnum.BUILDING_BEFORE_VALIDATING in failure_types
    assert FailureModeEnum.ORGANIZATIONAL_BOTTLENECK in failure_types


def test_eos_state_machine():
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    sm.transition_to(EOSState.HYPOTHESIS)
    sm.transition_to(EOSState.CHEAP_TEST)
    sm.transition_to(EOSState.VALIDATION)

    assert sm.current_state == EOSState.VALIDATION
    assert len(sm.state_history) == 4


def test_opportunity_decision_tree():
    # Pass all checks
    pursue, msg = OpportunityDecisionTree.evaluate(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        has_high_confidence_multi_source_signal=True,
        cheap_test_available=True,
        cheap_test_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert pursue is True
    assert "Commit resources" in msg

    # Fail structural anomaly
    pursue, msg = OpportunityDecisionTree.evaluate(
        is_structural_anomaly=False,
        is_reversible_decision=True,
        has_high_confidence_multi_source_signal=True,
        cheap_test_available=True,
        cheap_test_exceeds_kill_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert pursue is False
    assert "Discard" in msg


def test_ai_modules_and_kpi_stack():
    model = MentalModel(name="Test Model")
    pipeline = SignalPipeline(mental_model=model)

    sensing = SensingAgent(signal_pipeline=pipeline)
    hyp_engine = HypothesisEngine(signal_pipeline=pipeline)
    validation = ValidationAgent(signal_pipeline=pipeline)
    gtm_sim = GTMSimulator()
    classifier = GrowthStageClassifier()
    moat_agent = MoatAnalyzer()
    fail_agent = FailureModeMonitorAgent()
    allocator = CapitalAllocator()
    reinvention = ReinventionTrigger()
    governance = GovernanceSafetyLayer()

    anomalies = [
        Anomaly(id="a1", description="Noise", is_structural_shift=False, observed_signal_strength=0.1, source="src"),
        Anomaly(id="a2", description="Shift", is_structural_shift=True, observed_signal_strength=0.9, source="src"),
    ]
    structural = sensing.scan_environment(anomalies)
    assert len(structural) == 1

    hyp = hyp_engine.convert_anomaly_to_hypothesis(
        anomaly=structural[0],
        claim="Market shift claim",
        falsifiable_condition="Revenue > 100",
        kill_threshold_metric="Revenue",
        kill_threshold_value=100.0,
        estimated_cost=1000.0,
        risk_type=RiskType.TYPE_II
    )
    test_result = validation.run_cheap_test(hyp.id, metric_result=150.0)
    assert test_result is True

    ranked = allocator.rank_initiatives([
        {"name": "A", "expected_return": 100, "cost": 10},
        {"name": "B", "expected_return": 500, "cost": 100},
        {"name": "C", "expected_return": 300, "cost": 15},
    ])
    assert ranked[0]["name"] == "C" # return/cost ratio = 20

    assert reinvention.evaluate_self_disruption(market_share=0.5, innovation_velocity=0.2) is True
    assert governance.require_approval(RiskType.TYPE_I, budget=1000.0) is True

    kpi = KPIStack(signal_to_noise_ratio=0.85, activation_rate=0.4)
    assert kpi.signal_to_noise_ratio == 0.85
