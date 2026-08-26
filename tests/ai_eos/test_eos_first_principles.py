"""Comprehensive test suite for the First-Principles EOS Engine and EIOSKernel integrations."""

import pytest
from apodex.ai_eos.intelligence.eos_first_principles import (
    Timescale,
    DecisionType,
    CustomerJourneyStage,
    GrowthStage,
    SystemState,
    MarketSignal,
    FalsifiableHypothesis,
    BayesianBeliefUpdater,
    BusinessLoopEngine,
    CustomerJourneyTracker,
    GTMConfiguration,
    CompanyGrowthClassifier,
    FailureModeDetector,
    SensingAgent,
    HypothesisEngineModule,
    ValidationAgent,
    GTMSimulator,
    MoatAnalyzerModule,
    CapitalAllocator,
    ReinventionTrigger,
    GovernanceSafetyLayer,
    DecisionTreeEngine,
    EOSFirstPrinciplesEngine,
)
from apodex.arcs.kernel.kernel import EIOSKernel


def test_market_signal_and_bayesian_updater():
    sig = MarketSignal(
        description="Exponential compute elasticity adoption",
        observed_value=150.0,
        expected_value=100.0,
        is_structural=True,
    )
    assert sig.anomaly_magnitude == 0.5

    alpha, beta, mean = BayesianBeliefUpdater.update(prior_alpha=5.0, prior_beta=5.0, success_count=3, failure_count=1)
    assert alpha == 8.0
    assert beta == 6.0
    assert abs(mean - (8.0 / 14.0)) < 1e-5


def test_13_external_business_loops():
    ble = BusinessLoopEngine()

    s_prod = ble.evaluate_product_loop(retention_slope=0.1, nps=60, feature_adoption_rate=0.5)
    assert not s_prod.failure_mode_detected
    assert s_prod.loop_name == "Product"

    s_mkt = ble.evaluate_marketing_loop(cac_usd=1200.0, brand_recall=0.2, conversion_rate=0.005)
    assert s_mkt.failure_mode_detected

    s_sales = ble.evaluate_sales_loop(win_rate=0.30, sales_cycle_days=45, acv_usd=25000)
    assert not s_sales.failure_mode_detected

    s_cs = ble.evaluate_customer_success_loop(nrr=1.15, churn_rate=0.02, ttv_days=10)
    assert not s_cs.failure_mode_detected

    s_brand = ble.evaluate_brand_loop(share_of_voice=0.30, price_elasticity=-0.5)
    assert not s_brand.failure_mode_detected

    s_price = ble.evaluate_pricing_loop(arpu_usd=150.0, price_realization=0.90, elasticity=-0.8)
    assert not s_price.failure_mode_detected

    s_ref = ble.evaluate_referral_loop(viral_coefficient_k=1.2, referral_cac_usd=50.0)
    assert not s_ref.failure_mode_detected

    s_data = ble.evaluate_data_loop(data_latency_sec=1.5, decision_cycle_days=3.0)
    assert not s_data.failure_mode_detected

    s_fin = ble.evaluate_financial_loop(gross_margin=0.85, burn_multiple=1.2, runway_months=24.0)
    assert not s_fin.failure_mode_detected

    s_hire = ble.evaluate_hiring_loop(time_to_fill_days=30, quality_of_hire=0.85, retention_90d=0.95)
    assert not s_hire.failure_mode_detected

    s_cult = ble.evaluate_culture_loop(enps=50, decision_latency_days=3.0)
    assert not s_cult.failure_mode_detected

    s_innov = ble.evaluate_innovation_loop(num_experiments=12, hit_rate=0.25, time_to_signal_days=7.0)
    assert not s_innov.failure_mode_detected

    s_comp = ble.evaluate_competitive_intelligence_loop(relative_share_trend=0.05, feature_parity_gap=0.10)
    assert not s_comp.failure_mode_detected

    assert len(ble.loops) == 13


def test_customer_journey_tracker():
    tracker = CustomerJourneyTracker()
    tracker.update_stage(CustomerJourneyStage.AWARENESS, conversion_rate=0.10, dropoff_rate=0.90, time_days=1.0, metric_val=10000)
    tracker.update_stage(CustomerJourneyStage.ACTIVATION, conversion_rate=0.50, dropoff_rate=0.50, time_days=0.5, metric_val=500)
    assert tracker.calculate_overall_funnel_health() == 0.30


def test_gtm_channel_fit():
    gtm_plg = GTMConfiguration(
        positioning_statement="Self-serve developer tool",
        target_segment="Developers",
        price_usd=49.0,
        product_complexity="LOW",
        primary_channel="PLG",
    )
    assert gtm_plg.validate_channel_fit()

    gtm_ent = GTMConfiguration(
        positioning_statement="Enterprise AI Operating System",
        target_segment="Global 2000",
        price_usd=150000.0,
        product_complexity="HIGH",
        primary_channel="PLG",
    )
    assert not gtm_ent.validate_channel_fit()


def test_growth_stage_classifier():
    stage, constraint = CompanyGrowthClassifier.classify_stage(
        paying_customers=50,
        mrr_usd=15000.0,
        retention_flattened=True,
        growth_rate_mom=0.10,
        developer_ecosystem_active=False,
        market_share_percent=2.0,
    )
    assert stage == GrowthStage.PMF
    assert "Team bandwidth" in constraint


def test_failure_mode_detector():
    alerts = FailureModeDetector.audit_system(
        engagement_score=0.10,  # wrong problem
        build_velocity=0.90,
        demand_signal=0.10,     # building before validating
        cac_usd=600.0,
        win_rate=0.05,
        gross_margin=0.30,      # poor pricing
        retention_flattened=False,
        decision_latency_days=20.0, # org bottleneck
        disconfirming_data_ignored=True, # founder bias
        ltv_to_cac=1.5,
        underperforming_bets_count=4, # capital misallocation
    )
    assert len(alerts) >= 5


def test_ai_driven_agent_modules():
    sensing = SensingAgent()
    signals = [
        MarketSignal(description="Normal baseline", observed_value=10.0, expected_value=10.0),
        MarketSignal(description="API traffic spike", observed_value=500.0, expected_value=100.0, is_structural=True),
    ]
    anomalies = sensing.detect_anomalies(signals)
    assert len(anomalies) == 1

    hyp_mod = HypothesisEngineModule()
    hyp = hyp_mod.generate_hypothesis(anomalies[0])
    assert hyp.status == "PROPOSED"

    val_agent = ValidationAgent()
    res = val_agent.evaluate_test(hyp, test_cost_usd=50.0, observed_metric=150.0, kill_threshold=120.0)
    assert res.passed
    assert hyp.posterior_belief > 0.5

    gtm_sim = GTMSimulator()
    gtm_res = gtm_sim.simulate_gtm(
        GTMConfiguration(
            positioning_statement="AI DevTool",
            target_segment="SMB",
            price_usd=299.0,
            product_complexity="LOW",
            primary_channel="PLG",
        ),
        monthly_ad_spend_usd=5000.0,
    )
    assert gtm_res["channel_fit_valid"] == 1.0

    moat_score = MoatAnalyzerModule.calculate_moat_score(
        network_density=0.8, switching_cost_score=0.7, brand_trust=0.9, cost_advantage=0.6
    )
    assert moat_score > 0.70

    allocator = CapitalAllocator()
    initiatives = [
        {"id": "init_a", "cost_usd": 10000.0, "prob_success": 0.8, "expected_payoff_usd": 50000.0},
        {"id": "init_b", "cost_usd": 5000.0, "prob_success": 0.2, "expected_payoff_usd": 2000.0},
    ]
    allocs = allocator.allocate_capital(initiatives, total_budget_usd=12000.0)
    assert allocs["init_a"] == 10000.0

    reinvention = ReinventionTrigger()
    assert reinvention.evaluate_reinvention_necessity(revenue_growth_yoy=-0.05, market_share_decay=0.08, tech_shift_detected=False)

    gov = GovernanceSafetyLayer()
    assert not gov.evaluate_governance_gate(
        decision_type=DecisionType.TYPE_I, capital_requested_usd=100000.0, capital_threshold_type_i=50000.0, human_approved=False
    )


def test_decision_tree_engine():
    approved, msg = DecisionTreeEngine.evaluate_pursuit(
        is_structural_anomaly=True,
        is_reversible=True,
        high_confidence_multi_source=True,
        cheap_test_available=True,
        test_exceeds_kill_threshold=True,
        ev_clearly_positive=True,
        has_structural_advantage=True,
    )
    assert approved
    assert "Approved" in msg

    is_pursued, msg2 = DecisionTreeEngine.evaluate_pursuit(
        is_structural_anomaly=False,
        is_reversible=True,
        high_confidence_multi_source=False,
        cheap_test_available=True,
        test_exceeds_kill_threshold=True,
        ev_clearly_positive=True,
        has_structural_advantage=True,
    )
    assert not is_pursued
    assert "Discarded" in msg2


def test_master_eos_engine_cycle():
    engine = EOSFirstPrinciplesEngine()
    signals = [MarketSignal(description="Sudden cloud cost drop", observed_value=10.0, expected_value=100.0, is_structural=True)]
    initiatives = [{"id": "cloud_opt", "cost_usd": 5000.0, "prob_success": 0.9, "expected_payoff_usd": 30000.0}]
    res = engine.run_full_sensing_and_execution_cycle(signals, initiatives, total_budget_usd=10000.0)
    assert res["anomalies_detected"] == 1
    assert res["hypotheses_generated"] == 1
    assert res["capital_allocations_usd"]["cloud_opt"] == 5000.0


def test_eios_kernel_cognitive_capabilities():
    kernel = EIOSKernel()

    # 1. Sensing anomalies
    obs = [{"description": "Ad reach drop", "observed": 50.0, "expected": 100.0}]
    anomalies = kernel.sense_opportunity_anomalies(obs)
    assert len(anomalies) == 1

    # 2. Generate falsifiable hypothesis
    hyp = kernel.generate_falsifiable_hypothesis(anomalies[0])
    assert hyp["status"] == "PROPOSED"

    # 3. Validate opportunity economics
    econ = kernel.validate_opportunity_economics(arpu_usd=100.0, cac_usd=250.0, churn_rate=0.02)
    assert econ["economically_viable"]

    # 4. Allocate capital
    inits = [{"id": "p1", "score": 3.0}, {"id": "p2", "score": 1.0}]
    allocs = kernel.allocate_capital_opportunity(inits, budget_usd=10000.0)
    assert allocs["p1"] == 7500.0

    # 5. GTM channel reasoning
    gtm = kernel.reason_gtm_channel(price_usd=15000.0, complexity="HIGH")
    assert gtm == "SALES_LED"

    # 6. Analyze moat durability
    moat = kernel.analyze_moat_durability(network_density=0.9, switching_cost=0.8, brand_trust=0.9, cost_adv=0.7)
    assert moat > 0.80

    # 7. Evaluate lifecycle stage
    stage = kernel.evaluate_lifecycle_stage(customers=100, mrr=120000.0, retention_flat=True)
    assert stage == "GROWTH"

    # 8. Trigger reinvention review
    reinv = kernel.trigger_reinvention_review(growth_decay=0.20, attrition_rate=0.25)
    assert reinv
