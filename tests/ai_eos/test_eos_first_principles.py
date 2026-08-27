"""Unit and integration tests for Entrepreneurial Operating System (EOS) First Principles."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    Timescale,
    TimescaleLoop,
    MultiTimescaleLoopEngine,
    RiskType,
    Signal,
    SignalToIdeaPipeline,
    MentalModel,
    BusinessLoopName,
    BusinessLoopNetwork,
    CustomerJourneyStage,
    CustomerJourneyEngine,
    ChannelType,
    GTMSystem,
    GrowthStage,
    CompanyGrowthEngine,
    MoatEvaluator,
    FailureMode,
    FailureModeMonitor,
    EOSState,
    EOSStateMachine,
    EOSDecisionTree,
    AIEOSModuleRegistry,
    SubsystemKPIStack,
)
from apodex.arcs.kernel.kernel import EIOSKernel


def test_multi_timescale_loops_velocity_and_kill_discipline():
    engine = MultiTimescaleLoopEngine()

    fast_loop = TimescaleLoop(loop_id="fast_1", name="Ad Test", timescale=Timescale.FAST, velocity_hz=5.0, compounding_rate=0.10)
    med_loop = TimescaleLoop(loop_id="med_1", name="Pricing Iteration", timescale=Timescale.MEDIUM, velocity_hz=1.0, compounding_rate=0.08)
    slow_loop = TimescaleLoop(loop_id="slow_1", name="Moat Building", timescale=Timescale.SLOW, velocity_hz=0.1, compounding_rate=0.005) # Failing compounding

    engine.register_loop(fast_loop)
    engine.register_loop(med_loop)
    engine.register_loop(slow_loop)

    velocities = engine.calculate_aggregate_loop_velocity()
    assert velocities[Timescale.FAST.value] == 5.0
    assert velocities[Timescale.MEDIUM.value] == 1.0
    assert velocities[Timescale.SLOW.value] == 0.1

    killed = engine.evaluate_kill_discipline(performance_threshold=0.02)
    assert "slow_1" in killed
    assert not engine.loops["slow_1"].active


def test_signal_filter_and_risk_evaluation():
    pipeline = SignalToIdeaPipeline(symptomatic_filter_threshold=0.5)

    noise_signal = Signal(signal_id="s1", source="Twitter", content="Random chatter", is_anomaly=False)
    assert not pipeline.filter_signal(noise_signal)

    structural_signal = Signal(
        signal_id="s2", source="Traffic metrics", content="Internet traffic 1000% growth", is_anomaly=True, structural_shift_probability=0.9, noise_level=0.1
    )
    assert pipeline.filter_signal(structural_signal)

    # Bezos's One-Way vs Two-Way Door Heuristic
    type2_risk = pipeline.evaluate_decision_risk(is_reversible=True, stakes_usd=5000)
    assert type2_risk.risk_type == RiskType.TYPE_2
    assert type2_risk.required_confidence_threshold == 0.40

    type1_risk = pipeline.evaluate_decision_risk(is_reversible=False, stakes_usd=500000)
    assert type1_risk.risk_type == RiskType.TYPE_1
    assert type1_risk.required_confidence_threshold == 0.85


def test_cheap_test_real_options_and_opportunity_cost():
    pipeline = SignalToIdeaPipeline()

    assert pipeline.evaluate_cheap_test(test_cost_usd=500.0, expected_information_gain=50.0)
    assert not pipeline.evaluate_cheap_test(test_cost_usd=10000.0, expected_information_gain=1.0)

    score = pipeline.calculate_opportunity_cost_score(
        expected_compounding_return=0.25,
        best_alternative_return=0.10,
        structural_win_reason=True,
        market_size_5yr_usd=100_000_000
    )
    assert pytest.approx(score, 0.01) == 0.15

    no_edge_score = pipeline.calculate_opportunity_cost_score(
        expected_compounding_return=0.25,
        best_alternative_return=0.10,
        structural_win_reason=False,
        market_size_5yr_usd=100_000_000
    )
    assert no_edge_score == 0.0


def test_mental_model_parameter_vs_structural_updates_and_ossification():
    model = MentalModel(model_id="m1", name="Growth Model", parameters={"conversion": 0.05})

    pred = model.generate_prediction("conversion", 1000)
    assert pred == 50.0

    # Small error -> parameter tuning
    update_type = model.update_model("conversion", 52.0)
    assert update_type == "PARAMETER_TUNING"
    assert model.structure_version == 1

    # Large persistent error -> structural refactor / paradigm shift
    pred2 = model.generate_prediction("conversion", 1000)
    update_type2 = model.update_model("conversion", 200.0)
    assert update_type2 == "STRUCTURAL_REFACTOR"
    assert model.structure_version == 2
    assert model.ossification_score < 1.0


def test_business_loop_network_13_loops_and_coupling():
    network = BusinessLoopNetwork()
    network.initialize_canonical_loops()

    assert len(network.loops) == 13
    assert BusinessLoopName.PRODUCT in network.loops
    assert BusinessLoopName.FINANCIAL in network.loops

    coupling = network.propagate_coupling_effects(arpu_delta=0.2, churn_delta=0.05)
    assert coupling["financial_health"] >= 0.95
    assert coupling["hiring_health"] > 0.85
    assert coupling["product_health"] > 0.75


def test_customer_journey_15_stages_and_retention_flattening():
    engine = CustomerJourneyEngine()
    engine.initialize_canonical_stages()

    assert len(engine.stages) == 15
    assert CustomerJourneyStage.AWARENESS in engine.stages
    assert CustomerJourneyStage.REPURCHASE in engine.stages

    # Retention curve flattening analysis (PMF indicator)
    retention_curve_flattening = [0.80, 0.50, 0.35, 0.30, 0.29, 0.29, 0.29]
    result = engine.analyze_cohort_retention_flattening(retention_curve_flattening)
    assert result["flattens"] is True
    assert result["terminal_retention"] == 0.29

    retention_curve_leaking = [0.80, 0.50, 0.30, 0.15, 0.08, 0.03, 0.01]
    result_leaking = engine.analyze_cohort_retention_flattening(retention_curve_leaking)
    assert result_leaking["flattens"] is False


def test_gtm_system_channel_selection_and_pricing_alignment():
    gtm = GTMSystem()

    plg_channels = gtm.select_optimal_distribution_channels(product_complexity="LOW", price_point_annual_usd=500, network_effects_present=True)
    assert ChannelType.PLG in plg_channels
    assert ChannelType.CLG in plg_channels

    enterprise_channels = gtm.select_optimal_distribution_channels(product_complexity="HIGH", price_point_annual_usd=100000, network_effects_present=False)
    assert ChannelType.ENTERPRISE in enterprise_channels

    assert gtm.evaluate_pricing_positioning_alignment(price_usd=50000, segment_tier="ENTERPRISE")
    assert not gtm.evaluate_pricing_positioning_alignment(price_usd=500, segment_tier="ENTERPRISE")


def test_company_growth_engine_9_stages_and_binding_constraints():
    growth = CompanyGrowthEngine()
    growth.initialize_canonical_stages()

    assert len(growth.stage_details) == 9

    stage_idea = growth.classify_stage(paying_customers=0, nrr=1.0, retention_flattens=False, annual_revenue_usd=0)
    assert stage_idea == GrowthStage.IDEA

    stage_pmf = growth.classify_stage(paying_customers=50, nrr=1.1, retention_flattens=True, annual_revenue_usd=500_000)
    assert stage_pmf == GrowthStage.PMF

    stage_leadership = growth.classify_stage(paying_customers=10000, nrr=1.35, retention_flattens=True, annual_revenue_usd=100_000_000)
    assert stage_leadership == GrowthStage.PLATFORM or stage_leadership == GrowthStage.MARKET_LEADERSHIP


def test_moat_evaluator_composite_score():
    evaluator = MoatEvaluator()
    score = evaluator.calculate_composite_moat_score(
        network_density=0.8,
        avg_switching_cost_usd=15000.0,
        brand_trust_score=0.9,
        cost_advantage_percent=0.3,
        ip_protection_score=0.7,
        counter_positioning_score=0.85
    )
    assert 0.0 <= score <= 1.0
    assert score >= 0.70


def test_failure_mode_monitor_detection_and_corrections():
    monitor = FailureModeMonitor()
    monitor.initialize_canonical_failures()

    assert len(monitor.canonical_failures) == 10

    failures = monitor.scan_for_failure_modes(
        retention_flattens=False,
        cac_usd=500,
        ltv_usd=400,  # Poor unit economics
        decision_latency_days=20.0,  # High decision latency
        spending_growth_rate=0.5,
        user_growth_rate=0.1
    )

    detected_modes = [f.mode for f in failures]
    assert FailureMode.LACK_OF_PMF in detected_modes
    assert FailureMode.PREMATURE_SCALING in detected_modes
    assert FailureMode.ORGANIZATIONAL_BOTTLENECKS in detected_modes


def test_eos_state_machine_and_decision_tree_pursuit():
    sm = EOSStateMachine()
    assert sm.current_state == EOSState.SENSING

    sm.transition_to(EOSState.HYPOTHESIS, reason="Anomaly detected")
    assert sm.current_state == EOSState.HYPOTHESIS

    tree = EOSDecisionTree()
    pursue, msg = tree.evaluate_opportunity(
        is_structural_anomaly=True,
        is_reversible=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_result_exceeds_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert pursue is True
    assert "COMMIT" in msg

    reject, msg_rej = tree.evaluate_opportunity(
        is_structural_anomaly=False,
        is_reversible=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_result_exceeds_threshold=True,
        expected_value_positive=True,
        has_structural_advantage=True
    )
    assert reject is False
    assert "DISCARD" in msg_rej


def test_ai_eos_module_registry_and_subsystem_kpi_stack():
    registry = AIEOSModuleRegistry()
    assert len(registry.registered_modules) == 10
    assert "Sensing Agent" in registry.registered_modules
    assert "Governance/Safety Layer" in registry.registered_modules

    kpis = SubsystemKPIStack()
    assert kpis.sensing_signal_to_noise_ratio == 0.85
    assert kpis.financial_gross_margin == 0.80


def test_eios_kernel_native_cognitive_capabilities():
    kernel = EIOSKernel()

    signals = [
        {"id": "sig_1", "content": "CUDA compute gap", "is_anomaly": True, "structural_shift_probability": 0.95, "noise_level": 0.05},
        {"id": "sig_2", "content": "Random noise tweet", "is_anomaly": False, "structural_shift_probability": 0.1, "noise_level": 0.9}
    ]
    anomalies = kernel.sense_opportunity_anomalies(signals)
    assert len(anomalies) == 1
    assert anomalies[0]["id"] == "sig_1"

    hyp = kernel.generate_falsifiable_hypothesis(anomalies[0])
    assert hyp["status"] == "PROPOSED"
    assert "CUDA compute gap" in hyp["claim"]

    val = kernel.validate_opportunity_economics(hyp, {"cost_usd": 100, "expected_info_gain": 20, "arpu_usd": 100, "cac_usd": 30})
    assert val["decision"] == "PROCEED"

    budget_alloc = kernel.allocate_capital_opportunity([{"id": "p1", "expected_return_score": 3.0}, {"id": "p2", "expected_return_score": 1.0}], 100_000)
    assert budget_alloc["p1"] == 75_000
    assert budget_alloc["p2"] == 25_000

    channels = kernel.reason_gtm_channel(product_complexity="LOW", price_point_cents=5000, network_effects=True)
    assert "PRODUCT_LED" in channels
    assert "COMMUNITY_LED" in channels

    moat_score = kernel.analyze_moat_durability({"network_density": 0.8, "avg_switching_cost_usd": 8000, "brand_trust_score": 0.85})
    assert 0.0 <= moat_score <= 1.0

    stage = kernel.evaluate_lifecycle_stage({"paying_customers": 100, "nrr": 1.15, "retention_flattens": True, "annual_revenue_usd": 2_000_000})
    assert stage in ["PRODUCT_MARKET_FIT", "GROWTH"]

    assert kernel.trigger_reinvention_review(revenue_decay=0.20, churn_rate=0.25)
    assert not kernel.trigger_reinvention_review(revenue_decay=0.02, churn_rate=0.03)
