"""Unit and integration tests for the 14-Layer Computational Architecture of Entrepreneurship."""

from __future__ import annotations
import math
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    RealityOptimizer,
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
    EntrepreneurialIntelligenceOrchestrator
)


def test_layer1_reality() -> None:
    opt = RealityOptimizer(human_risk_aversion=3.0, cognitive_energy_weight=2.0)
    u_ent = opt.calculate_global_objective(
        expected_revenue=1000.0,
        value_at_risk=100.0,
        cognitive_energy_expended=5.0,
        capital_cost=10.0
    )
    assert math.isclose(u_ent, 28.0)

    # Fundamental nature & invariants
    nature = opt.get_fundamental_nature()
    assert "definition" in nature
    assert "thermodynamic_analogy" in nature
    assert "mathematical_core" in nature

    invariants = opt.get_invariant_principles()
    assert len(invariants) == 4
    assert invariants[0]["name"] == "Asymmetric Risk Profile"

    psych_opt = opt.deconstruct_psychology_vs_optimization()
    assert len(psych_opt["human_psychology"]) > 0
    assert len(psych_opt["optimization_problems"]) > 0

    # Test automation boundaries
    is_auto, reason = opt.map_automation_boundaries("dynamic_pricing_optimization", 0.3)
    assert is_auto
    assert reason == "AUTOMATABLE_DETERMINISTIC"

    is_auto_emp, reason_emp = opt.map_automation_boundaries("empathy_customer_interview", 0.9)
    assert not is_auto_emp
    assert reason_emp == "HUMAN_PSYCHOLOGY_BOUND"

    auto_potential = opt.analyze_automation_potential()
    assert "automatable" in auto_potential
    assert "non_automatable" in auto_potential


def test_layer2_discovery() -> None:
    engine = OpportunityDiscoveryEngine(filter_threshold=0.4)
    signals = {"weak_1": 0.5, "noise_2": 0.2, "trend_3": 0.8}
    filtered = engine.filter_weak_signals(signals)
    assert "weak_1" in filtered
    assert "trend_3" in filtered
    assert "noise_2" not in filtered

    # Search space & signal-to-noise ratio check
    feed = [{"weak_1": 0.4}, {"weak_1": 0.6}]
    detected = engine.detect_weak_signals(feed)
    assert detected["weak_1"] == pytest.approx(0.5)

    entropy_signals = engine.filter_signals_by_entropy({"sig_1": 0.1, "noise_1": 0.5})
    assert "sig_1" in entropy_signals

    combined_obs = engine.combine_unrelated_observations("DeFi", "Medicine")
    assert "DeFi" in combined_obs
    assert "Medicine" in combined_obs

    novelty = engine.generate_novelty_score("Autonomous_Agent", "Decentralized_Ledger")
    assert novelty == 1.0

    trend_score = engine.evaluate_trend_importance(0.04, 0.5, 0.8)
    assert trend_score == pytest.approx(2.0)

    predicted_market = engine.predict_emerging_market([0.2, 0.3], 5)
    assert 0.0 <= predicted_market <= 1.0

    invisible_factors = engine.explain_invisible_opportunity_factors()
    assert len(invisible_factors) == 4

    opps = engine.search_world_state_space([
        {"name": "test_state", "signals": {"signal_a": 0.8, "signal_b": 0.9}}
    ])
    assert len(opps) == 1
    assert "signal_a" in opps[0].weak_signals


def test_layer3_problem_discovery() -> None:
    engine = ProblemDiscoveryEngine()

    # Definition and stated vs real checks
    problem = engine.define_problem("System latency is high", ["slow_dashboard", "timeout"])
    assert problem["statement"] == "System latency is high"

    stated_ok, explanation = engine.verify_stated_vs_real_problem(["latency"], {"database_contention": 0.95})
    assert not stated_ok
    assert "database_contention" in explanation

    hierarchy = engine.decompose_problem_hierarchy("root", {"root": ["child_1", "child_2"], "child_1": ["grandchild"]})
    assert "grandchild" in hierarchy
    assert "child_2" in hierarchy

    order_map = engine.classify_first_vs_second_order({"root": [], "child": ["root"]})
    assert "root" in order_map["first_order"]
    assert "child" in order_map["second_order"]

    # Backdoor criterion root-cause evaluation
    is_root, causal_strength = engine.evaluate_root_cause_do(
        symptom_prob=0.5, confounder_prob=0.3, symptom_given_intervention_prob=0.8
    )
    assert causal_strength == pytest.approx(0.65)
    assert is_root

    distinction = engine.distinguish_symptom_from_root_cause("p_1", 0.5, 0.8)
    assert distinction == "ROOT_CAUSE"

    assert engine.should_ignore_problem(1.0, 100.0, 0.5)
    assert not engine.should_ignore_problem(500.0, 10.0, 0.8)


def test_layer4_decision_making() -> None:
    engine = DecisionMakingEngine(min_confidence_threshold=0.3)

    # Decisions under uncertainty
    decision, posterior = engine.make_decision_under_uncertainty(10.0, 5.0, 10, 2)
    assert decision == "PROCEED"
    assert posterior == pytest.approx(20.0 / 27.0)

    prioritized_qs = engine.determine_information_priority([
        {"question": "Q1", "uncertainty_score": 0.2},
        {"question": "Q2", "uncertainty_score": 0.9}
    ])
    assert prioritized_qs[0]["question"] == "Q2"

    boundary = engine.evaluate_intuition_vs_data_boundary(1, 500.0)
    assert boundary == "TRUST_INTUITION"

    attention = engine.allocate_cognitive_attention([
        {"name": "A1", "priority": 10.0},
        {"name": "A2", "priority": 30.0}
    ])
    assert attention["A2"] == pytest.approx(0.75)

    assert engine.execute_fast_kill(0.1, 5000.0)

    # Confirmation bias mitigation update
    a, b = engine.compute_confirmation_bias_adjusted_priors(
        alpha_prior=5.0, beta_prior=5.0, positive_evidence=12, negative_evidence=4, bias_factor=1.2
    )
    assert math.isclose(a, 15.0)
    assert math.isclose(b, 9.8)

    assert engine.should_kill_idea(1.0, 9.0, 10)
    assert not engine.should_kill_idea(8.0, 2.0, 10)

    discounts = engine.mitigate_confirmation_bias(15, 4)
    assert discounts["discounted_positive_evidence"] == 10.0
    assert discounts["weighted_negative_evidence"] == 6.0


def test_layer5_evaluation() -> None:
    engine = OpportunityEvaluationEngine()

    quality_vars = engine.get_opportunity_quality_variables()
    assert len(quality_vars) == 5

    ev = engine.calculate_expected_value(market_size=100000.0, success_probability=0.7, launch_cost=20000.0)
    assert ev == 50000.0

    opp = Opportunity(name="Test Opp", description="", expected_value=100000.0, novelty_score=0.5, timing_score=0.8)
    adv_ev = engine.calculate_advanced_expected_value(opp)
    assert adv_ev == pytest.approx(100000.0 * 0.8 * 1.25)

    var = engine.estimate_value_at_risk(ev, 5000.0)
    assert var == 0.0

    cvar = engine.estimate_downside_risk_cvar(10000.0, 5000.0)
    assert cvar >= 0.0

    t_early = engine.evaluate_timing_score(1.0, 5.0, 10.0)
    assert t_early < 1.0

    t_window = engine.evaluate_timing_window(0.8, 0.2)
    assert t_window == pytest.approx(0.64)

    opp_a = Opportunity(name="A", description="", expected_value=50000.0, downside_risk_var=10000.0)
    opp_b = Opportunity(name="B", description="", expected_value=80000.0, downside_risk_var=30000.0)
    assert engine.compare_opportunities(opp_a, opp_b).name == "B"

    assert engine.should_abandon_for_alternative(opp_a, opp_b, 5000.0)


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine(max_complexity_budget=50.0)

    to_prune = engine.determine_what_not_to_build([
        {"name": "F1", "impact": 10.0, "complexity": 1.0},
        {"name": "F2", "impact": 1.0, "complexity": 10.0}
    ])
    assert "F2" in to_prune

    multiplier = engine.minimize_unnecessary_complexity(4)
    assert multiplier < 1.0

    feature_val = engine.estimate_feature_value_creation(0.8, 100.0)
    assert feature_val == 80.0

    jtbd = engine.discover_core_jtbd(["Optimizing latency of pipeline execution", "Low latency is critical"])
    assert "latency" in jtbd

    learning_rate = engine.optimize_for_learning_rate(100.0, 500.0)
    assert learning_rate == 5.0

    features, total = engine.enforce_complexity_cap([10.0, 15.0, 20.0, 30.0])
    assert features == [10.0, 15.0, 20.0]
    assert total == 45.0

    jtbd_score = engine.compute_jtbd_alignment({"f1": 0.8, "f2": 0.4})
    assert jtbd_score == pytest.approx(0.6)


def test_layer7_customer_understanding() -> None:
    engine = CustomerUnderstandingEngine()

    psy = engine.model_customer_psychology(0.6, 0.8)
    assert psy["friction_coefficient"] == pytest.approx(0.66)

    trust_eq = engine.calculate_trust_score(0.5, 0.4, 0.8)
    assert trust_eq == pytest.approx(0.25)

    drivers = engine.evaluate_switching_drivers(100.0, 500.0)
    assert drivers == 400.0

    triggers = engine.explain_buying_triggers(0.8, 0.9, 0.7)
    assert triggers == pytest.approx(0.8 * 0.9 * 0.7)

    churn = engine.predict_customer_churn(0.5, 3)
    assert churn == pytest.approx(0.5 * 0.6 + 0.3 * 0.4)

    loyalty = engine.measure_customer_loyalty(5.0, 3)
    assert loyalty == pytest.approx(0.5 * 1.3)

    assert engine.identify_evangelism_threshold(150.0, 80.0)

    prob = engine.evaluate_switching_probability(
        current_product_utility=2.0,
        proposed_product_utility=8.0,
        switching_costs=1.0,
        push_forces=0.5,
        pull_forces=0.5
    )
    assert prob > 0.99

    trust = engine.compute_trust_multiplier(0.8, 0.9)
    assert trust == pytest.approx(0.84)


def test_layer8_marketing() -> None:
    engine = MarketingEngine()

    market_sizes = engine.simulate_market_formation(10, 1000, 3)
    assert len(market_sizes) == 4
    assert market_sizes[-1] > 10

    spread = engine.calculate_attention_spread(50, 0.2, 3)
    assert len(spread) == 4

    viral_k = engine.evaluate_viral_coefficient(2.5, 0.5)
    assert viral_k == 1.25

    brand = engine.measure_brand_emergence(1000, 500)
    assert brand == 1500.0

    authority = engine.calculate_authority_score(50, 5.0)
    assert authority == 75.0

    pos = engine.evaluate_positioning_influence(0.8, 0.9)
    assert pos == pytest.approx(0.72)

    channel_ints = engine.model_channel_interactions(1000.0, 1.25)
    assert channel_ints == 1250.0


def test_layer9_sales() -> None:
    engine = SalesEngine()

    psy_state = engine.model_sales_psychological_state(0.9, 0.1)
    assert psy_state == "HOT_DECISION"

    urgency_fac = engine.calculate_buying_urgency_factors(0.8, 100.0)
    assert urgency_fac == 80.0

    objections = engine.diagnose_objections(["Too expensive", "We need a money back guarantee"])
    assert "PRICE_OBJECTION" in objections
    assert "TRUST_OBJECTION" in objections

    resolved, close_prob = engine.resolve_objections_algorithmically(["PRICE_OBJECTION"], 0.8)
    assert resolved
    assert close_prob == pytest.approx(0.6)

    assert engine.should_automate_sales(50.0, 500)
    assert engine.is_enterprise_sales_necessary(100000.0, 120)

    sales_system = engine.design_repeatable_sales_system([0.8, 0.5, 0.5])
    assert sales_system == pytest.approx(0.2)


def test_layer10_growth() -> None:
    engine = GrowthEngine()

    compounding = engine.calculate_compounding_growth(100.0, 0.1, 5)
    assert compounding == pytest.approx(100.0 * (1.1 ** 5))

    network_emergence = engine.simulate_network_effect_emergence(50)
    assert network_emergence == 2500.0

    ecosystem = engine.evaluate_ecosystem_formation(10, 50)
    assert ecosystem == 500.0

    assert engine.measure_platform_replacement_potential(1000.0, 400.0)

    ltv_cac = engine.predict_long_term_success_metrics(300.0, 80.0)
    assert ltv_cac == 3.75

    assert engine.evaluate_intentional_deceleration_triggers(0.08)


def test_layer11_competition() -> None:
    engine = CompetitionEngine()

    action = engine.anticipate_competitor_actions(50.0, 100.0)
    assert action == "ANTICIPATE_PRICING_WAR"

    durability = engine.evaluate_moat_durability(3.0, 0.9)
    assert durability == pytest.approx(2.7)

    difficulty = engine.measure_copy_difficulty(500.0, 1000.0)
    assert difficulty == 1500.0

    assert engine.evaluate_pivot_triggers(0.7, 0.3)

    runway = engine.survive_market_disruption(100000.0, 10000.0)
    assert runway == 10.0


def test_layer12_organizational_design() -> None:
    engine = OrganizationalDesignEngine()

    assert engine.evaluate_hiring_triggers(0.95, 2.0)

    delegation = engine.classify_centralization_vs_delegation(0.1, 0.9)
    assert delegation == "DELEGATE_TO_EDGE"

    evolution = engine.evaluate_organizational_evolution(50)
    assert evolution == "FUNCTIONAL_STRUCTURE"

    scaling = engine.evaluate_decision_system_scaling(3)
    assert scaling == pytest.approx(1.0 / 1.3)


def test_layer13_meta_learning() -> None:
    engine = MetaLearningEngine()

    improvement = engine.evaluate_meta_entrepreneurial_improvement([0.5, 0.6, 0.85])
    assert improvement == 0.35

    bayesian_model = engine.update_mental_models_bayesian(0.8, 0.9)
    assert 0.0 <= bayesian_model <= 1.0

    quality = engine.measure_decision_quality(150.0, 100.0)
    assert quality == 0.5

    intuition = engine.build_intuition_via_pattern_matching("pricing_war", ["pricing_war_macro", "pricing_war_local"])
    assert intuition == 1.0

    diff = engine.calculate_learning_velocity_differential(0.5, 0.3)
    assert diff == pytest.approx(0.2)

    graph = engine.convert_failures_to_knowledge_graphs(["Fail A", "Fail B"])
    assert "error_0" in graph
    assert graph["error_0"]["description"] == "Fail A"


def test_layer14_ai_entrepreneurship() -> None:
    engine = AIEntrepreneurshipEngine()

    nature = engine.classify_entrepreneurial_task_nature("causal_inference_analysis")
    assert nature["type"] == "CAUSAL_INFERENCE"

    opp = Opportunity(name="Opp A", description="", novelty_score=0.8, expected_value=100.0)
    vector = engine.represent_opportunity_computational(opp)
    assert len(vector["opportunity_vector"]) == 5

    ranked = engine.rank_opportunities_by_expected_utility([
        Opportunity(name="X", description="", expected_value=10.0, timing_score=0.5),
        Opportunity(name="Y", description="", expected_value=100.0, timing_score=0.9)
    ])
    assert ranked[0].name == "Y"

    mcts_path = engine.select_optimal_experiments_mcts("node_0", 3)
    assert len(mcts_path) == 4

    portfolio = engine.allocate_multi_resource_portfolio([opp], 10000.0, 100.0)
    assert portfolio[opp.opportunity_id]["allocated_capital"] == 10000.0

    perf = engine.calculate_quantitative_performance_metric(8, 10, 50.0)
    assert perf == 40.0

    updated_weight = engine.simulate_self_improvement_loop(0.5, 0.2)
    assert updated_weight == pytest.approx(0.52)


def test_orchestrator_resolves_the_one_question_above_all_others() -> None:
    orchestrator = EntrepreneurialIntelligenceOrchestrator()
    signals = {"crypto": 0.8, "healthcare": 0.7, "noise": 0.1}

    result = orchestrator.resolve_complete_computational_architecture_of_entrepreneurship(
        raw_market_signals=signals,
        available_capital=100000.0,
        compute_hours=500.0,
        historical_decision_quality=[0.6, 0.7, 0.85]
    )

    assert result["question_above_all_others"] == "The Complete 14-Layer Computational Architecture of Entrepreneurship"
    assert "fundamental_nature" in result
    assert "invariant_principles" in result
    assert result["active_opportunity_name"] is not None
    assert "is_root_cause_identified" in result
    assert "bayesian_decision" in result
    assert result["risk_adjusted_expected_value"] > 0
    assert "allocated_portfolio" in result
    assert "updated_system_instructions" in result
