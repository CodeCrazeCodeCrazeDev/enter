from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    ProblemDefinition,
    CustomerProfile,
    RealityInvariantsEngine,
    OpportunityDiscoveryEngine,
    AdvancedCausalEngine,
    ProblemDiscoveryEngine,
    DecisionEngine,
    ActiveInferencePlanner,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitionEngine,
    OrganizationalEngine,
    MetaLearningEngine,
    EntrepreneurialIntelligenceOrchestrator
)


def test_layer1_reality_invariants() -> None:
    engine = RealityInvariantsEngine()

    # Sustainable value exchange
    result_viable = engine.evaluate_invariant_value_exchange(
        perceived_value_cents=10000,
        price_cents=5000,
        cost_cents=2000
    )
    assert result_viable["is_viable"] is True
    assert result_viable["customer_surplus_cents"] == 5000
    assert result_viable["producer_margin_cents"] == 3000
    assert result_viable["gross_margin_pct"] == 60.0

    # Non-viable value exchange
    result_non_viable = engine.evaluate_invariant_value_exchange(
        perceived_value_cents=4000,
        price_cents=5000,
        cost_cents=2000
    )
    assert result_non_viable["is_viable"] is False

    # Automation boundary partitioning
    assert engine.partition_automation_boundary("math_opt", False, True, False) == "CAN_BE_AUTOMATED"
    assert engine.partition_automation_boundary("founder_judgment", False, True, True) == "REQUIRES_HUMAN_JUDGMENT"


def test_layer2_opportunity_discovery() -> None:
    engine = OpportunityDiscoveryEngine()

    raw_obs = [
        {"id": 1, "signal_variance": 0.1},
        {"id": 2, "signal_variance": 0.45},
        {"id": 3, "signal_variance": 0.8}
    ]
    weak_signals = engine.detect_weak_signals(raw_obs, threshold=0.3)
    assert len(weak_signals) == 2
    assert weak_signals[0]["id"] == 2

    combinations = engine.cross_combine_domains(["AI_Agents"], ["Biotech", "Fintech"])
    assert len(combinations) == 2
    assert combinations[0]["title"] == "AI_Agents x Biotech"


def test_layer3_problem_discovery_and_causal() -> None:
    engine = ProblemDiscoveryEngine()
    prob = engine.decompose_problem(
        statement="Users churning due to latency",
        symptoms=["high_dropoff", "negative_reviews"],
        causes=["database_bottleneck"]
    )
    assert prob.is_root_cause is True
    assert prob.severity_score > 0.5
    assert prob.ignore_recommendation is False


def test_layer4_decision_making_under_uncertainty() -> None:
    engine = DecisionEngine()

    # Optimal stopping 37% rule
    samples = [10, 20, 30, 40, 15, 25, 35, 50]
    result_early = engine.optimal_stopping_decision(samples[:2], budget_limit=10)
    assert result_early["action"] == "CONTINUE_SAMPLING"

    result_commit = engine.optimal_stopping_decision(samples, budget_limit=10)
    assert result_commit["action"] == "STOP_AND_COMMIT"

    # Data & intuition blending
    blended = engine.blend_data_and_intuition(data_confidence=0.9, intuition_score=0.4, data_volume=25)
    assert 0.4 < blended < 0.9

    # Fast idea killing
    kill_eval = engine.evaluate_idea_kill_threshold(milestones_failed=2, max_allowed_failures=2)
    assert kill_eval["should_kill"] is True


def test_layer5_opportunity_evaluation() -> None:
    eval_engine = OpportunityEvaluationEngine()

    # Kelly Criterion position sizing
    kelly = eval_engine.calculate_kelly_fraction(win_probability=0.6, win_loss_ratio=2.0)
    # Kelly = (0.6 * 2.0 - 0.4) / 2.0 = (1.2 - 0.4) / 2 = 0.4
    assert pytest.approx(kelly) == 0.4

    # Opportunity switching tradeoff
    opp_a = Opportunity(title="Opp A", domain="A", tam_cents=10000000, success_probability=0.5)
    opp_b = Opportunity(title="Opp B", domain="B", tam_cents=30000000, success_probability=0.4)
    switching = eval_engine.evaluate_switching_tradeoff(opp_a, opp_b, switching_cost_cents=1000000)

    # Opp A EV = 5,000,000; Opp B Net EV = 12,000,000 - 1,000,000 = 11,000,000
    assert switching["should_switch"] is True


def test_layer6_product_creation_and_jtbd() -> None:
    engine = ProductCreationEngine()
    features = [
        {"name": "fast_checkout", "directly_addresses_goal": True, "learning_value_score": 0.9},
        {"name": "dark_mode_theme", "directly_addresses_goal": False, "learning_value_score": 0.2}
    ]
    analysis = engine.analyze_job_to_be_done("Buy products frictionlessly", features)
    assert "fast_checkout" in analysis["essential_mvp_features"]
    assert "dark_mode_theme" in analysis["rejected_bloat_features"]


def test_layer7_customer_understanding() -> None:
    engine = CustomerUnderstandingEngine()
    profile = CustomerProfile(
        segment="Enterprise",
        perceived_value_cents=50000,
        price_cents=10000,
        trust_level=0.8,
        churn_probability=0.1
    )
    risk = engine.predict_churn_risk(profile, usage_frequency_days=10)
    assert 0.0 < risk < 1.0

    assert engine.calculate_net_promoter_category(10) == "PROMOTER"
    assert engine.calculate_net_promoter_category(6) == "DETRACTOR"


def test_layer8_marketing_and_market_dynamics() -> None:
    engine = MarketingEngine()
    viral = engine.calculate_viral_coefficient(invites_sent_per_user=5.0, conversion_rate=0.25)
    assert viral["viral_coefficient_k"] == 1.25
    assert viral["is_compounding"] is True


def test_layer9_sales_systems() -> None:
    engine = SalesEngine()
    assert engine.evaluate_automation_readiness(monthly_deals=50, process_repeatability_score=0.9) is True
    assert engine.evaluate_automation_readiness(monthly_deals=10, process_repeatability_score=0.9) is False

    objection = engine.resolve_objection("PRICE_TOO_HIGH", price_cents=10000, ltv_cents=50000)
    assert objection["strategy"] == "DEMONSTRATE_ROI"
    assert objection["resolved"] is True


def test_layer10_growth_and_network_effects() -> None:
    engine = GrowthEngine()
    val = engine.compute_network_value(active_users=100)
    assert val == 10000.0  # Metcalfe's law N^2

    platform_eval = engine.evaluate_platform_transition(product_users=20000, third_party_developers=100)
    assert platform_eval["is_platform_ready"] is True


def test_layer11_competition_and_moats() -> None:
    engine = CompetitionEngine()
    durability = engine.calculate_moat_durability(network_effects=0.9, switching_costs=0.8, cost_advantage=0.7, brand_equity=0.6)
    assert 0.7 < durability < 0.85


def test_layer12_organizational_design() -> None:
    engine = OrganizationalEngine()
    hiring = engine.evaluate_hiring_trigger(current_utilization_pct=90.0, revenue_per_employee_cents=20000000)
    assert hiring["should_hire"] is True


def test_layer13_meta_learning() -> None:
    engine = MetaLearningEngine()
    brier = engine.calculate_brier_score([0.8, 0.2], [1, 0])
    # BS = ((0.8 - 1)^2 + (0.2 - 0)^2) / 2 = (0.04 + 0.04) / 2 = 0.04
    assert pytest.approx(brier) == 0.04

    rule = engine.convert_failure_to_reusable_rule({"root_cause": "MEMORY_LEAK", "domain": "INFRASTRUCTURE"})
    assert rule["status"] == "RULE_REGISTERED"


def test_active_inference_planner_ranking() -> None:
    planner = ActiveInferencePlanner(curiosity_weight=2.0)

    # Opportunity 1: High curiosity path (high expected entropy reduction from 2.0 to 0.4 = 1.6)
    opp_1 = Opportunity(
        title="high_exploratory_opportunity",
        domain="tech_frontier",
        prior_entropy=2.0,
        post_entropy_simulated=0.4,
        success_probability=0.4,
        target_preference=0.9
    )

    # Opportunity 2: Conservative replica (low entropy reduction from 0.6 to 0.5 = 0.1)
    opp_2 = Opportunity(
        title="conservative_replication",
        domain="traditional_retail",
        prior_entropy=0.6,
        post_entropy_simulated=0.5,
        success_probability=0.85,
        target_preference=0.9
    )

    ranked = planner.rank_opportunities([opp_1, opp_2])

    # Under curiosity_weight = 2.0, opp_1 should yield a more negative Expected Free Energy (superior)
    assert ranked[0][0].title == "high_exploratory_opportunity"
    assert ranked[0][1] < ranked[1][1]


def test_advanced_causal_engine_do_and_counterfactual() -> None:
    engine = AdvancedCausalEngine()

    # Build causal path: marketing_spend -> click_through_rate -> sales_revenue
    engine.add_causal_relationship("marketing_spend", "click_through_rate", 0.6)
    engine.add_causal_relationship("click_through_rate", "sales_revenue", 1.8)

    # 1. Verify do-calculus intervention (do(marketing_spend = 2.0))
    state = engine.execute_do_intervention("marketing_spend", 2.0)
    assert state["marketing_spend"] == 2.0
    # click_through_rate = 2.0 * 0.6 = 1.2
    assert pytest.approx(state["click_through_rate"]) == 1.2
    # sales_revenue = 1.2 * 1.8 = 2.16
    assert pytest.approx(state["sales_revenue"]) == 2.16

    # 2. Verify Counterfactual estimation (Abduction -> Action -> Prediction)
    factual_observations = {
        "marketing_spend": 1.0,
        "click_through_rate": 0.8,
        "sales_revenue": 1.44
    }
    counterfactual_revenue = engine.estimate_counterfactual(
        factual_observations=factual_observations,
        counterfactual_intervention=("marketing_spend", 2.0),
        target_outcome_var="sales_revenue"
    )
    assert pytest.approx(counterfactual_revenue) == 2.52


def test_orchestrated_pipeline_execution() -> None:
    engine = AdvancedCausalEngine()
    planner = ActiveInferencePlanner(curiosity_weight=1.5)
    orchestrator = EntrepreneurialIntelligenceOrchestrator(engine, planner)

    signal = {
        "title": "Autonomous Scientific Hardware Venture",
        "domain": "robotics",
        "variables": ["marketing_spend", "click_through_rate", "sales_revenue"],
        "causal_edges": [("marketing_spend", "click_through_rate"), ("click_through_rate", "sales_revenue")],
        "coefficients": {
            "marketing_spend->click_through_rate": 0.5,
            "click_through_rate->sales_revenue": 2.0
        },
        "prior_entropy": 1.8,
        "post_entropy_simulated": 0.5,
        "success_probability": 0.6,
        "tam_cents": 500000000,
        "cac_cents": 10000,
        "ltv_cents": 100000
    }

    orchestrator.ingest_signal(signal)
    pipeline_result = orchestrator.execute_orchestrated_pipeline()

    assert pipeline_result["status"] == "executed"
    assert pipeline_result["selected_opportunity"] == "Autonomous Scientific Hardware Venture"
    assert "best_expected_free_energy" in pipeline_result
    assert pipeline_result["propagated_state"]["marketing_spend"] == 1.5
    assert pipeline_result["layer1_invariant_exchange"]["is_viable"] is True
    assert pipeline_result["kelly_capital_fraction"] > 0.0
    assert pipeline_result["moat_durability_score"] > 0.0
