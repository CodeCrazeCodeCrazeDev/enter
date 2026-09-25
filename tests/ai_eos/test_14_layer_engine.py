from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence import (
    RealitySubstrateEngine,
    OpportunityDiscoveryEngine,
    ProblemDiscoveryEngine,
    DecisionMakingEngine,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitionEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    AIEntrepreneurshipEngine,
    FourteenLayerOrchestrator,
)


def test_layer1_reality_substrate() -> None:
    engine = RealitySubstrateEngine()
    arbitrage = engine.evaluate_reality_arbitrage({"true_physical_state": 0.9, "market_expectation": 0.3})
    assert arbitrage["has_arbitrage"] is True
    assert arbitrage["arbitrage_magnitude"] == pytest.approx(0.6)

    automation = engine.classify_task_automation("Unit Economics Calc", {"physical_touch": False, "legal_accountability": False})
    assert automation["can_automate"] is True

    invariants = engine.filter_invariant_principles({
        "epistemic_divergence": True,
        "asymmetric_upside": True,
        "fast_learning_cycles": False
    })
    assert invariants["is_viable"] is True


def test_layer2_opportunity_discovery() -> None:
    engine = OpportunityDiscoveryEngine()
    signals = engine.search_state_space([{"novelty_score": 0.8, "tam_dollars": 10000000}])
    assert len(signals) == 1

    weak = engine.detect_weak_signals([0.2, 0.3, 0.25, 0.4])
    assert weak["detected"] is True

    combined = engine.cross_combine_domains({"name": "AI", "core_tech": "LLMs"}, {"name": "Biotech", "target_market": "Pharma"})
    assert "LLMs applied to Pharma" in combined["title"]

    momentum = engine.compute_hawkes_trend_momentum([1.0, 2.0, 2.5], 3.0)
    assert momentum > 0.1

    stealth = engine.calculate_stealth_index(causal_complexity=2.0, market_signal=0.5, incumbent_blindspot=0.9)
    assert stealth > 3.0


def test_layer3_problem_discovery() -> None:
    engine = ProblemDiscoveryEngine()
    problem = engine.define_problem(current_state=0.2, target_state=1.0, friction_weight=2.0)
    assert problem["is_severe"] is True

    dag = engine.decompose_problem_dag("High Churn", ["Onboarding friction", "Slow support"])
    assert len(dag["sub_problems"]) == 2

    whys = engine.evaluate_5whys_root_cause(["Slow load time", "Large asset size", "Uncompressed images"])
    assert whys["root_cause"] == "Uncompressed images"

    ignore = engine.should_ignore_problem(tam=100, delta_wtp=1.0, resolution_cost=10000)
    assert ignore is True


def test_layer4_decision_making() -> None:
    engine = DecisionMakingEngine()
    efe = engine.compute_efe(pragmatic_utility=2.0, epistemic_information_gain=1.0, curiosity_weight=1.5)
    assert efe == -3.5

    evpi = engine.calculate_evpi(prior_uncertainty=10.0, experiment_cost=2.0)
    assert evpi == 18.0

    fused = engine.fuse_intuition_and_data(prior_belief=0.2, prior_weight=1.0, sample_data=[0.8, 0.9, 0.7])
    assert fused > 0.5

    sprt = engine.sprt_fast_kill([-1.0, -0.8, -0.5], lower_bound=-2.0)
    assert sprt == "KILL"

    bias = engine.counterfactual_bias_test("Always works", {"positive_proofs": 10, "negative_proofs": 0})
    assert bias["has_bias"] is True


def test_layer5_opportunity_evaluation() -> None:
    engine = OpportunityEvaluationEngine()
    unit_econ = engine.calculate_unit_economics(ltv=3000, cac=500, payback_months=6, ndr=1.2)
    assert unit_econ["is_healthy"] is True

    ev = engine.calculate_expected_value(p_success=0.7, npv_upside=1000000, capital_at_risk=100000)
    assert ev == 670000

    var = engine.estimate_downside_var([-0.5, -0.2, 0.1, 0.4, 0.8], confidence=0.99)
    assert var == 0.5

    bass = engine.evaluate_bass_diffusion_timing(time_step=2.0)
    assert bass > 0.0

    abandon = engine.evaluate_abandonment_trigger(current_roic=0.05, hurdle_rate=0.15)
    assert abandon is True


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine()
    features = [
        {"name": "f1", "utility": 10, "complexity": 2},
        {"name": "f2", "utility": 20, "complexity": 10},
        {"name": "f3", "utility": 5, "complexity": 1}
    ]
    kept = engine.filter_non_essential_features(features, max_complexity=5)
    assert len(kept) == 2

    jtbd = engine.extract_core_jtbd({"functional_goal": "Export reports", "emotional_goal": "Save time"})
    assert "Export reports" in jtbd["core_jtbd"]

    shapley = engine.attribute_feature_shapley_values({"all": 100.0, "f1": 30.0, "f2": 50.0})
    assert shapley["f1"] == 0.3

    lrate = engine.calculate_learning_rate_per_sprint(information_gained=10.0, sprint_duration_days=14.0)
    assert pytest.approx(lrate) == 10.0 / 14.0


def test_layer7_customer_understanding() -> None:
    engine = CustomerUnderstandingEngine()
    utility = engine.model_customer_prospect_utility(gain=10.0, loss=2.0, loss_aversion_coeff=2.25)
    assert utility == 5.5

    trust = engine.update_trust_stock(current_trust=0.5, decay=0.1, reliability_score=0.9)
    assert trust == 0.63

    friction = engine.calculate_switching_friction(data_lockin=100, retraining_cost=50, exit_penalty=25)
    assert friction == 175

    churn = engine.predict_cox_churn_risk(usage_velocity_decline=0.5, support_tickets=3)
    assert 0.0 <= churn <= 1.0


def test_layer8_marketing() -> None:
    engine = MarketingEngine()
    r0 = engine.calculate_viral_coefficient(invites_per_user=3.0, conversion_rate=0.4)
    assert r0 == pytest.approx(1.2)

    cascade = engine.simulate_attention_hawkes_cascade(base_rate=0.1, excitation_alpha=0.5, decay_beta=0.8, timesteps=5)
    assert len(cascade) == 5

    authority = engine.calculate_brand_authority_score(citation_count=100, domain_rank=80.0)
    assert authority > 40.0

    dist = engine.compute_positioning_perceptual_distance([1.0, 2.0], [4.0, 6.0])
    assert dist == 5.0


def test_layer9_sales() -> None:
    engine = SalesEngine()
    stage = engine.evaluate_sales_funnel_state(awareness=0.9, qualification=0.8, trust=0.85)
    assert stage == "CLOSED_WON"

    inaction_cost = engine.calculate_inaction_economic_cost(daily_loss=1000.0, decision_delay_days=30)
    assert inaction_cost == 30000.0

    resolution = engine.resolve_buyer_objection("price_too_high", {"price_too_high": "Offer flexible ARR plan"})
    assert resolution["resolved"] is True

    route = engine.route_sales_channel(acv_dollars=100000, deal_complexity="high")
    assert route == "HIGH_TOUCH_ENTERPRISE_SALES"


def test_layer10_growth() -> None:
    engine = GrowthEngine()
    metcalfe = engine.calculate_metcalfe_network_value(user_count=100)
    assert metcalfe == 10000.0

    reed = engine.calculate_reed_group_network_value(group_count=10)
    assert reed == 1024.0

    r40 = engine.evaluate_rule_of_40(revenue_growth_pct=30.0, margin_pct=20.0)
    assert r40["passes_rule"] is True

    throttle = engine.should_throttle_growth(current_capacity=100, demand_growth_rate=200)
    assert throttle is True


def test_layer11_competition() -> None:
    engine = CompetitionEngine()
    nash = engine.model_nash_countermove([[0.5, 0.8], [0.2, 0.9]])
    assert "expected_countermove" in nash

    moat = engine.calculate_moat_vector(0.8, 0.7, 0.9, 0.8)
    assert moat == 0.8

    resistance = engine.calculate_copying_resistance(tech_complexity=8.0, execution_speed_delta=5.0)
    assert resistance == 6.8

    pivot = engine.detect_pivot_trigger(incumbent_feature_overlap=0.85, market_saturation=0.5)
    assert pivot is True


def test_layer12_org_design() -> None:
    engine = OrganizationalDesignEngine()
    hire = engine.evaluate_hiring_trigger(workload_hours=120, team_capacity_hours=80, bottleneck_score=0.9)
    assert hire is True

    delegation = engine.evaluate_centralization_vs_delegation(reversibility_type=2, local_context_intensity=0.8)
    assert delegation == "DELEGATED_EDGE_AGENT_DECISION"

    topo = engine.evolve_org_topology(node_count=10)
    assert topo == "POD_BASED_CROSS_FUNCTIONAL"

    latency = engine.calculate_decision_scaling_latency(node_count=50, topology="POD_BASED_CROSS_FUNCTIONAL")
    assert latency > 0.0


def test_layer13_meta_learning() -> None:
    engine = MetaLearningEngine()
    brier = engine.calculate_brier_calibration_score([0.9, 0.8, 0.2], [1, 1, 0])
    assert brier < 0.1

    priors = engine.update_mental_model_priors({"confidence_score": 0.6}, [{"outcome": "success"}])
    assert priors["confidence_score"] == 0.65

    rules = engine.compile_failure_to_negative_rules("Product launched without attribution tracking")
    assert len(rules) == 3

    hit_rate = engine.benchmark_intuition_hit_rate([(0.8, 1), (0.2, 0), (0.9, 0)])
    assert pytest.approx(hit_rate) == 2 / 3


def test_layer14_ai_entrepreneurship() -> None:
    engine = AIEntrepreneurshipEngine()
    route = engine.route_task_formalization("intervention")
    assert route == "Structural Causal Model (do-calculus)"

    opp = engine.construct_canonical_opportunity({"title": "Autonomous Venture"})
    assert "id" in opp

    ranked = engine.rank_opportunities_multi_criterion([
        {"title": "O1", "efe_score": -2.0},
        {"title": "O2", "efe_score": -0.5}
    ])
    assert ranked[0]["title"] == "O1"

    capital = engine.allocate_capital_kelly(p_win=0.6, odds_ratio=2.0, total_capital=1000000)
    assert capital > 0.0

    flywheel = engine.run_continuous_capability_self_improvement([{"log": "p1"}, {"log": "p2"}])
    assert flywheel["flywheel_active"] is True


def test_fourteen_layer_orchestrator_e2e() -> None:
    orchestrator = FourteenLayerOrchestrator()
    signal = {
        "title": "Autonomous AI Agent Venture Subsystem",
        "true_physical_state": 1.0,
        "market_expectation": 0.2,
        "novelty_score": 0.9,
        "tam_dollars": 50000000,
        "current_state": 0.1,
        "utility": 2.0
    }
    result = orchestrator.run_end_to_end_pipeline(signal)
    assert result["status"] == "COMPLETED"
    assert result["signal_title"] == "Autonomous AI Agent Venture Subsystem"
    assert result["l1_arbitrage"]["has_arbitrage"] is True
    assert result["l4_efe_score"] < 0.0
    assert result["l14_kelly_capital_allocated"] > 0.0
