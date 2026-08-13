"""Comprehensive unit and integration test suite for EOS First-Principles Reconstruction."""

import pytest
from apodex.ai_eos.intelligence import (
    MasterLoopNode,
    MasterLoop,
    WeakSignal,
    SignalFilter,
    Hypothesis,
    CheapTest,
    BeliefState,
    BeliefUpdater,
    DecisionRiskType,
    RiskEvaluator,
    OpportunityCostLens,
    MentalModel,
    BusinessLoop,
    BusinessLoopCoupler,
    CustomerJourneyStageType,
    CustomerJourneyStage,
    CustomerJourney,
    ChannelType,
    GTMSystem,
    GrowthStageType,
    GrowthStage,
    CompanyGrowthTracker,
    CostCurveTracker,
    MoatAuditor,
    FailureModeType,
    FailureModeMonitor,
    SensingAgent,
    HypothesisEngine,
    ValidationAgent,
    GTMSimulator,
    CapitalAllocator,
    GovernanceSafetyLayer,
    IntegratedEOSEngine
)
from apodex.arcs.kernel.kernel import EIOSKernel


def test_master_loop_transitions_and_re_entry():
    """Verify state transitions and specialized re-entry loops for kill signals."""
    loop = MasterLoop()
    assert loop.current_node == MasterLoopNode.ENVIRONMENTAL_SENSING

    # Transition sequentially
    loop.process_signal("none", 0.0)
    assert loop.current_node == MasterLoopNode.SIGNAL_COLLECTION

    # Manually position to CUSTOMER_VALIDATION (F) and trigger kill signal
    loop.current_node = MasterLoopNode.CUSTOMER_VALIDATION
    loop.process_signal("kill_signal", 0.8)
    assert loop.current_node == MasterLoopNode.OPPORTUNITY_DISCOVERY

    # MVP_EXPERIMENTATION (H) to OPPORTUNITY_DISCOVERY (D) kill signal
    loop.current_node = MasterLoopNode.MVP_EXPERIMENTATION
    loop.process_signal("kill_signal", 0.9)
    assert loop.current_node == MasterLoopNode.OPPORTUNITY_DISCOVERY

    # CUSTOMER_ACQUISITION (K) to GTM_SYSTEM (J) weak GTM signal
    loop.current_node = MasterLoopNode.CUSTOMER_ACQUISITION
    loop.process_signal("weak_gtm", 0.15)
    assert loop.current_node == MasterLoopNode.GTM_SYSTEM

    # REVENUE_OPTIMIZATION (M) to BUSINESS_MODEL_DESIGN (G) bad economics signal
    loop.current_node = MasterLoopNode.REVENUE_OPTIMIZATION
    loop.process_signal("bad_economics", 0.75)
    assert loop.current_node == MasterLoopNode.BUSINESS_MODEL_DESIGN

    # CONTINUOUS_REINVENTION (S) to ENVIRONMENTAL_SENSING (A) loop
    loop.current_node = MasterLoopNode.CONTINUOUS_REINVENTION
    loop.process_signal("reinvent", 1.0)
    assert loop.current_node == MasterLoopNode.ENVIRONMENTAL_SENSING


def test_cognitive_signal_to_idea_pipeline():
    """Verify weak signal filtering, hypothesis generation, and cheap test execution."""
    filter_agent = SignalFilter(anomaly_threshold=0.5)

    # Low amplitude -> Discarded
    sig_noise = WeakSignal(signal_id="sig_001", description="Noise", amplitude=0.3, is_structural_shift_symptom=True)
    assert filter_agent.process_signal(sig_noise) is None

    # Structural shift above threshold -> Hypothesis formed
    sig_structural = WeakSignal(signal_id="sig_002", description="Internet traffic curve spike", amplitude=0.7, is_structural_shift_symptom=True)
    hyp = filter_agent.process_signal(sig_structural)
    assert hyp is not None
    assert hyp.hypothesis_id == "hyp_sig_002"

    # Execute cheap test
    test = CheapTest(test_id="test_001", hypothesis_id=hyp.hypothesis_id, cost_cents=50_00)
    is_falsified, info_gain = test.execute(external_metric_outcome=0.4)
    assert not is_falsified
    assert info_gain > 0.0

    # Falsified test
    is_falsified_2, _ = test.execute(external_metric_outcome=0.05)
    assert is_falsified_2


def test_bayesian_belief_updating():
    """Verify conjugate updating of belief state distributions."""
    belief = BeliefState(alpha=10.0, beta=10.0)
    updater = BeliefUpdater()

    # Success outcome updates alpha parameter
    new_belief_success = updater.update(belief, success=True)
    assert new_belief_success.alpha == 11.0
    assert new_belief_success.beta == 10.0
    assert new_belief_success.expected_probability > belief.expected_probability

    # Failure outcome updates beta parameter
    new_belief_fail = updater.update(belief, success=False)
    assert new_belief_fail.alpha == 10.0
    assert new_belief_fail.beta == 11.0
    assert new_belief_fail.expected_probability < belief.expected_probability


def test_risk_and_opportunity_cost_evaluation():
    """Verify risk type classification and strict opportunity cost filters."""
    evaluator = RiskEvaluator()
    # High cost, low reversibility -> Type I
    assert evaluator.evaluate(reversibility_score=0.1, financial_impact_cents=100000_00) == DecisionRiskType.TYPE_I
    # Low cost, high reversibility -> Type II
    assert evaluator.evaluate(reversibility_score=0.9, financial_impact_cents=500_00) == DecisionRiskType.TYPE_II

    lens = OpportunityCostLens(min_market_size_billions=1.5, requires_structural_advantage=True)
    # Valid elite opportunity
    assert lens.evaluate_project("SaaS Core", expected_compounding=True, has_advantage=True, market_size_billions=2.5)
    # Fails compounding filter
    assert not lens.evaluate_project("One-off Agency", expected_compounding=False, has_advantage=True, market_size_billions=5.0)
    # Fails advantage filter
    assert not lens.evaluate_project("Generic Copycat", expected_compounding=True, has_advantage=False, market_size_billions=2.5)
    # Fails market size filter
    assert not lens.evaluate_project("Micro-Niche", expected_compounding=True, has_advantage=True, market_size_billions=0.5)


def test_mental_model_evolution():
    """Verify prediction generation, parameter tuning, and structural paradigm shifts."""
    model = MentalModel(name="Cloud Adoption Model", parameters={"bandwidth_growth": 0.5, "latency_reduction": 0.3})

    inputs = {"bandwidth_growth": 1.0, "latency_reduction": 1.0}
    prediction = model.generate_prediction(inputs)
    assert prediction == pytest.approx(0.8)

    # Small error triggers parameter updates
    model.update_model(error=0.10)
    assert model.parameters["bandwidth_growth"] > 0.5
    assert model.consecutive_failed_predictions == 0

    # Large persistent errors trigger standard paradigm shift
    model.update_model(error=0.40)
    assert model.consecutive_failed_predictions == 1
    model.update_model(error=0.40)
    model.update_model(error=0.40)
    assert model.structural_complexity == 2  # Shifted structure
    assert model.consecutive_failed_predictions == 0

    # Model ossification prevents structure shift
    ossified_model = MentalModel(name="Ossified Model", parameters={"p": 0.5}, ossification_score=0.95)
    ossified_model.update_model(error=0.50)
    ossified_model.update_model(error=0.50)
    ossified_model.update_model(error=0.50)
    assert ossified_model.structural_complexity == 1  # Blocked structural shift


def test_external_coupled_business_loops():
    """Verify simulation of coupled operational feedback loops (Meadows style)."""
    coupler = BusinessLoopCoupler(stocks={"cash": 10000.0, "talent": 5.0})

    pricing = BusinessLoop(name="Pricing", feedback_signal="ARPU", core_kpis={"ARPU": 50.0}, failure_mode="cost_plus")
    sales = BusinessLoop(name="Sales", feedback_signal="conversion", core_kpis={"conversion_rate": 0.10}, failure_mode="non_icp")
    marketing = BusinessLoop(name="Marketing", feedback_signal="leads", core_kpis={"traffic": 1000.0}, failure_mode="mismatch")
    financial = BusinessLoop(name="Financial", feedback_signal="burn", core_kpis={"burn_multiple": 1.0}, failure_mode="negative_unit")
    hiring = BusinessLoop(name="Hiring", feedback_signal="talent", core_kpis={"time_to_fill_days": 10.0}, failure_mode="pedigree")
    product = BusinessLoop(name="Product", feedback_signal="velocity", failure_mode="loudest_customer")

    coupler.register_loop(pricing)
    coupler.register_loop(sales)
    coupler.register_loop(marketing)
    coupler.register_loop(financial)
    coupler.register_loop(hiring)
    coupler.register_loop(product)

    # Initial tick
    stocks = coupler.execute_tick()
    # Expected revenue inflow: 1000 (traffic) * 0.10 (conversion) * 50.0 (ARPU) = 5000.0
    # Expected cash: 10000.0 + 5000.0 = 15000.0
    assert stocks["cash"] == 15000.0

    # Hiring budget allocated: 15000.0 * 0.3 / 1.0 = 4500.0
    # Talent gained: 4500.0 / (10.0 * 100.0) = 4.5
    # Expected talent: 5.0 + 4.5 = 9.5
    assert stocks["talent"] == 9.5

    # Talent drives Product loop velocity core KPI: 9.5 * 2.0 = 19.0
    assert coupler.loops["Product"].core_kpis["velocity"] == 19.0


def test_customer_journey_stages():
    """Verify cohort transitions along the 15-stage full-lifecycle customer journey."""
    stages = {
        CustomerJourneyStageType.AWARENESS: CustomerJourneyStage(
            stage_type=CustomerJourneyStageType.AWARENESS,
            founder_objective="reach",
            customer_psychology="pattern matching",
            key_metric_name="reach",
            metric_value=10000.0,
            common_mistake="generic messaging",
            optimization_lever="category framing"
        ),
        CustomerJourneyStageType.INTEREST: CustomerJourneyStage(
            stage_type=CustomerJourneyStageType.INTEREST,
            founder_objective="earn attention",
            customer_psychology="curiosity",
            key_metric_name="ctr",
            metric_value=0.0,
            common_mistake="feature dumping",
            optimization_lever="pain first"
        )
    }
    journey = CustomerJourney(stages=stages)

    transitioned = journey.transition_cohort(
        CustomerJourneyStageType.AWARENESS,
        CustomerJourneyStageType.INTEREST,
        volume=10000.0,
        efficiency=0.05
    )
    assert transitioned == 500.0
    assert journey.stages[CustomerJourneyStageType.INTEREST].metric_value == 500.0


def test_go_to_market_system():
    """Verify strategic channel selection based on ARPU and complexity pricing signals."""
    # Low ARPU, low complexity -> PLG
    gtm_plg = GTMSystem(pricing_arpu_cents=50_00, product_complexity=0.2)
    assert gtm_plg.select_optimal_distribution_channel() == ChannelType.PLG

    # High ARPU, high complexity -> SLG
    gtm_slg = GTMSystem(pricing_arpu_cents=2500_00, product_complexity=0.8)
    assert gtm_slg.select_optimal_distribution_channel() == ChannelType.SLG

    # Network effect, moderate price -> CLG
    gtm_clg = GTMSystem(pricing_arpu_cents=150_00, product_complexity=0.5)
    assert gtm_clg.select_optimal_distribution_channel() == ChannelType.CLG


def test_company_growth_tracker():
    """Verify sequential growth tracker scoring and premature scaling mitigations."""
    tracker = CompanyGrowthTracker()
    assert tracker.current_stage == GrowthStageType.IDEA

    tracker.scores["validated_learnings"] = 6.0
    assert tracker.evaluate_transition() == GrowthStageType.VALIDATION

    tracker.scores["paying_customers"] = 12.0
    assert tracker.evaluate_transition() == GrowthStageType.STARTUP

    # Fails transition to PMF because retention_rate is low (mitigates premature scaling)
    tracker.scores["retention_rate"] = 0.25
    assert tracker.evaluate_transition() == GrowthStageType.STARTUP

    tracker.scores["retention_rate"] = 0.45
    assert tracker.evaluate_transition() == GrowthStageType.PMF


def test_strategic_thinking_moats_and_cost_curves():
    """Verify strategic cost-curve forecasting and Porters/Helmer competitive moat auditing."""
    # Battery technology cost-decay forecast
    tracker = CostCurveTracker(
        technology_name="Lithium Batteries",
        historical_cost_per_unit={2018: 200.0, 2022: 100.0}
    )
    # Predicts year when target cost is crossed
    predicted_year = tracker.predict_viability_year(target_economic_cost=50.0)
    assert predicted_year > 2022

    moats = MoatAuditor()
    moats.moat_scores["network_effects"] = 0.8
    moats.moat_scores["switching_costs"] = 0.6
    assert moats.calculate_total_moat_index() == pytest.approx(1.4 / 6)


def test_failure_mode_analysis_and_monitor():
    """Verify monitoring systems detect failure modes and return correction pathways."""
    monitor = FailureModeMonitor()

    # Scaling prematurely detection: high burn multiple and low LTV:CAC
    metrics = {"burn_multiple": 4.5, "ltv_cac_ratio": 1.1}
    failures = monitor.analyze_failures(metrics)
    assert len(failures) == 1
    assert failures[0][0] == FailureModeType.PREMATURE_SCALING
    assert "focus on cohort retention" in failures[0][1]


def test_integrated_ai_driven_os_engine():
    """Verify the overall orchestration layer of the Integrated EOS Operating System."""
    engine = IntegratedEOSEngine()
    engine.growth_tracker.current_stage = GrowthStageType.MARKET_LEADERSHIP

    metrics = {"burn_multiple": 5.0, "ltv_cac_ratio": 1.0}
    alerts = engine.run_strategic_audit(metrics)

    assert any("Active Failure Mode" in alert for alert in alerts)
    assert any("Continuous Reinvention" in alert for alert in alerts)
    assert engine.master_loop.current_node == MasterLoopNode.CONTINUOUS_REINVENTION


def test_eios_kernel_integration():
    """Verify programmatic strategic reasoning integration inside EIOSKernel."""
    kernel = EIOSKernel()

    # 1. Sensing Anomalies
    assert kernel.sense_opportunity_anomalies(data=[100.0, 150.0, 100.0], baseline=50.0)
    assert not kernel.sense_opportunity_anomalies(data=[50.0, 52.0, 48.0], baseline=50.0)

    # 2. Strategic Hypothesis Generation
    hyp = kernel.generate_falsifiable_hypothesis("Compute cost curve drop")
    assert hyp.hypothesis_id.startswith("hyp_")

    # 3. Validation Opportunity Economics
    test = CheapTest(test_id="test_opt", hypothesis_id=hyp.hypothesis_id, cost_cents=100_00, target_metric_observed=0.45)
    viability_score = kernel.validate_opportunity_economics(test)
    assert viability_score == pytest.approx(0.90)

    # 4. Capital Allocation under Opportunity Cost
    initiatives = [
        {"id": "init_A", "expected_return": 3.5, "required_cost_cents": 500_00},
        {"id": "init_B", "expected_return": 8.0, "required_cost_cents": 1000_00}
    ]
    allocs = kernel.allocate_capital_opportunity(initiatives, total_budget_cents=1200_00)
    # Highest ROI (init_B) is fully funded, remaining 200 cents goes to init_A
    assert allocs["init_B"] == 1000_00
    assert allocs["init_A"] == 200_00

    # 5. GTM Channel Reasoner
    channel = kernel.reason_gtm_channel(pricing_cents=50_00, complexity=0.2)
    assert channel == ChannelType.PLG

    # 6. Moat Durability Auditor
    total_moat = kernel.analyze_moat_durability({"network_effects": 0.9, "brand_trust": 0.9})
    assert total_moat == pytest.approx(1.8 / 6)

    # 7. Growth Lifecycle Evaluator
    stage = kernel.evaluate_lifecycle_stage({"validated_learnings": 10.0})
    assert stage == GrowthStageType.VALIDATION

    # 8. Reinvention Trigger
    loop_node = kernel.trigger_reinvention_review()
    assert loop_node == MasterLoopNode.CONTINUOUS_REINVENTION
