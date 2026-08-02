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
    # Expected Return: 1000, VaR: 100, Cognitive Energy: 5, Capital: 10
    # U_ent = (1000 - 3 * 100) / (5 + 2 * 10) = 700 / 25 = 28.0
    u_ent = opt.calculate_global_objective(
        expected_revenue=1000.0,
        value_at_risk=100.0,
        cognitive_energy_expended=5.0,
        capital_cost=10.0
    )
    assert math.isclose(u_ent, 28.0)

    # Test automation boundaries
    is_auto, reason = opt.map_automation_boundaries("dynamic_pricing_optimization", 0.3)
    assert is_auto
    assert reason == "AUTOMATABLE_DETERMINISTIC"

    is_auto_emp, reason_emp = opt.map_automation_boundaries("empathy_customer_interview", 0.9)
    assert not is_auto_emp
    assert reason_emp == "HUMAN_PSYCHOLOGY_BOUND"

    # Test invariants
    invariants = opt.get_invariant_principles()
    assert "first_principles_thinking" in invariants
    assert "asymmetric_risk_return" in invariants


def test_layer2_discovery() -> None:
    engine = OpportunityDiscoveryEngine(filter_threshold=0.4)
    signals = {"weak_1": 0.5, "noise_2": 0.2, "trend_3": 0.8}
    filtered = engine.filter_weak_signals(signals)
    assert "weak_1" in filtered
    assert "trend_3" in filtered
    assert "noise_2" not in filtered

    # Combinatorial synthesis
    opp = engine.synthesize_combinatorial_opportunity("tech_wearables", "bio_feedback", {})
    assert opp.novelty_score > 0.0
    assert "tech_wearables" in opp.weak_signals

    # State space search
    opps = engine.search_state_space(signals, {"market_trend": "active_inference"})
    assert len(opps) == 1  # exactly one combination of ("weak_1", "trend_3")
    assert opps[0].weak_signals == ["weak_1", "trend_3"]

    # Boost/detect weak signals
    boosted = engine.detect_weak_signals({"noise_2": 0.2, "trend_3": 0.8})
    assert boosted["noise_2"] == pytest.approx(0.24)  # 0.2 * 1.2
    assert boosted["trend_3"] == 0.8

    # Trend relevance
    relevance = engine.evaluate_trend_relevance("biotech_sensor", ["biotech", "sensor"])
    assert relevance > 0.5

    # Predict emerging market
    assert engine.predict_emerging_market([0.1, 0.2, 0.45])  # accelerating growth
    assert not engine.predict_emerging_market([0.5, 0.6, 0.65])  # decelerating growth

    # Invisible opportunity
    opp_invisible = Opportunity(name="Invis", description="", weak_signals=["novel_quantum"], novelty_score=0.8)
    assert engine.is_invisible_opportunity(opp_invisible, {"healthcare", "web3"})
    assert not engine.is_invisible_opportunity(opp_invisible, {"quantum", "healthcare"})


def test_layer3_problem_discovery() -> None:
    from apodex.ai_eos.intelligence.computational_architecture import ProblemDefinition
    engine = ProblemDiscoveryEngine()
    # First order check
    is_first = engine.classify_problem_order({"prob_2": ["prob_1"]}, "prob_1")
    assert is_first

    is_second = engine.classify_problem_order({"prob_2": ["prob_1"]}, "prob_2")
    assert not is_second

    # Backdoor criterion root-cause evaluation
    is_root, causal_strength = engine.evaluate_root_cause_do(
        symptom_prob=0.5, confounder_prob=0.3, symptom_given_intervention_prob=0.8
    )
    assert causal_strength == pytest.approx(0.65)
    assert is_root

    # Stated vs Real Problem
    prob_def = ProblemDefinition(
        stated_symptom="We need a CRM",
        real_underlying_pain="Sales reps are lazy",
        affected_user_segment="sales managers",
        economic_cost_of_inaction=100.0,
        frequency_per_week=5.0,
        severity_index=0.8
    )
    is_mismatch, verdict = engine.detect_stated_vs_real_problem(prob_def)
    assert is_mismatch
    assert verdict == "MISMATCH_DETECTED"

    # Problem Decomposition
    decomp = engine.decompose_problem("root", {"root": ["child1", "child2"], "child1": ["grandchild"]})
    assert decomp == ["root", "child1", "child2", "grandchild"]

    # Should Ignore
    assert not engine.should_ignore_problem(prob_def)
    insignificant_prob = ProblemDefinition(
        stated_symptom="small issue",
        real_underlying_pain="small issue",
        affected_user_segment="general",
        economic_cost_of_inaction=1.0,
        frequency_per_week=1.0,
        severity_index=0.1
    )
    assert engine.should_ignore_problem(insignificant_prob)


def test_layer4_decision_making() -> None:
    engine = DecisionMakingEngine(min_confidence_threshold=0.3)
    # Confirmation bias mitigation update
    a, b = engine.compute_confirmation_bias_adjusted_priors(
        alpha_prior=5.0, beta_prior=5.0, positive_evidence=12, negative_evidence=4, bias_factor=1.2
    )
    # positive_adj = 12 / 1.2 = 10 -> alpha_post = 15
    # negative_adj = 4 * 1.2 = 4.8 -> beta_post = 9.8
    assert math.isclose(a, 15.0)
    assert math.isclose(b, 9.8)

    # Should kill
    assert engine.should_kill_idea(1.0, 9.0, 10)  # low success expectation
    assert not engine.should_kill_idea(8.0, 2.0, 10)

    # Decisions under uncertainty
    options_ev = {"VentureA": 1000.0, "VentureB": 1200.0}
    risk_variance = {"VentureA": 50.0, "VentureB": 200.0}
    # For risk_aversion=2.0, Util_A = 1000 - 100 = 900. Util_B = 1200 - 400 = 800.
    best = engine.make_decision_under_uncertainty(options_ev, risk_variance, 2.0)
    assert best == "VentureA"

    # Information seeking priority
    priority = engine.determine_information_seeking_priority(
        {"market_size_uncertainty": 0.8, "tech_feasibility_uncertainty": 0.9},
        {"market_size_uncertainty": 10.0, "tech_feasibility_uncertainty": 2.0}
    )
    assert priority == ["tech_feasibility_uncertainty", "market_size_uncertainty"]

    # Rely on intuition / data
    assert engine.should_rely_on_intuition(8.0, 0.4)
    assert not engine.should_rely_on_intuition(2.0, 0.4)
    assert engine.should_rely_on_data(50, 0.01)
    assert not engine.should_rely_on_data(10, 0.01)

    # Cognitive attention softmax
    attn = engine.allocate_cognitive_attention({"Task1": 1.0, "Task2": 2.0})
    assert attn["Task2"] > attn["Task1"]
    assert math.isclose(sum(attn.values()), 1.0, abs_tol=1e-3)


def test_layer5_evaluation() -> None:
    engine = OpportunityEvaluationEngine()
    ev = engine.calculate_expected_value(market_size=100000.0, success_probability=0.7, launch_cost=20000.0)
    assert ev == 50000.0

    var = engine.estimate_value_at_risk(ev, 5000.0)
    # 50000 - 1.645 * 5000 = 41775 -> -41775. VaR is max(0, -return) = 0.0
    assert var == 0.0

    # Timing windows
    t_early = engine.evaluate_timing_score(1.0, 5.0, 10.0)
    assert t_early < 1.0
    t_opt = engine.evaluate_timing_score(7.0, 5.0, 10.0)
    assert t_opt == 1.0

    # Opportunity Quality Metrics
    opp = Opportunity(name="OppQ", description="", expected_value=5000.0, downside_risk_var=1000.0, timing_score=0.9)
    quality = engine.evaluate_opportunity_quality_metrics(opp, margin=0.8, cap_efficiency=2.0)
    assert quality["quality_index"] > 0.0

    # Compare Opportunities
    opp_a = Opportunity(name="A", description="", expected_value=1000.0, downside_risk_var=100.0)
    opp_b = Opportunity(name="B", description="", expected_value=2000.0, downside_risk_var=500.0)
    better = engine.compare_opportunities(opp_a, opp_b)
    assert better.name == "A"  # 1000/100 = 10 vs 2000/500 = 4

    # Abandon for alternative
    assert engine.should_abandon_for_alternative(opp_a, opp_b, transition_cost=100.0)


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine(max_complexity_budget=50.0)
    features, total = engine.enforce_complexity_cap([10.0, 15.0, 20.0, 30.0])
    assert features == [10.0, 15.0, 20.0]
    assert total == 45.0

    jtbd_score = engine.compute_jtbd_alignment({"f1": 0.8, "f2": 0.4})
    assert jtbd_score == pytest.approx(0.6)

    # Excluded features
    excluded = engine.determine_excluded_features({"f1": 0.9, "f2": 0.2, "f3": 0.5})
    assert excluded == ["f2"]

    # Feature value creation
    val = engine.evaluate_feature_value_creation(2.0, 100.0)
    assert val == pytest.approx(100.0 / math.pow(2.0, 1.5))

    # Core JTBD
    core_job = engine.discover_core_jtbd({"reporting": 0.5, "speed_billing": 0.9})
    assert core_job == "speed_billing"

    # Optimize learning rate
    lr = engine.optimize_for_learning_rate(0.1, 2.0)
    assert lr == pytest.approx(0.05)


def test_layer7_customer_understanding() -> None:
    from apodex.ai_eos.intelligence.computational_architecture import CustomerPsychologyModel
    engine = CustomerUnderstandingEngine()
    # High utility diff overcomes switching costs
    prob = engine.evaluate_switching_probability(
        current_product_utility=2.0,
        proposed_product_utility=8.0,
        switching_costs=1.0,
        push_forces=0.5,
        pull_forces=0.5
    )
    # Net utility = (8 - 2) - 1 + 0.5 + 0.5 = 6.0
    # sigmoid(6) should be extremely high
    assert prob > 0.99

    trust = engine.compute_trust_multiplier(0.8, 0.9)
    assert trust == pytest.approx(0.84)

    # Build customer trust
    bt = engine.build_customer_trust(0.9, 0.8)
    assert bt == pytest.approx(0.87)

    # Analyze buying motives
    motives = engine.analyze_buying_motives(10.0, 40.0)
    assert motives["logical_motive"] == 0.8
    assert motives["emotional_motive"] == 0.2

    # Analyze churn drivers
    assert engine.analyze_churn_drivers(5, 0.2) == pytest.approx(0.6)

    # Calculate loyalty index
    assert engine.calculate_loyalty_index(5, 8.0) == pytest.approx(0.65)

    # Is evangelist candidate
    assert engine.is_evangelist_candidate(0.9, 3)
    assert not engine.is_evangelist_candidate(0.7, 1)


def test_layer8_marketing() -> None:
    engine = MarketingEngine()
    attention_curve = engine.simulate_viral_attention_spread(
        initial_aware_cohort=0.1, viral_factor_k=1.5, exposure_rate=0.8, steps=3
    )
    assert len(attention_curve) == 4
    # Attention must increase or stay within bounds
    assert all(0.0 <= val <= 1.0 for val in attention_curve)

    # Simulate market formation
    assert engine.simulate_market_formation(0.5, 0.5) == pytest.approx(0.7)

    # Evaluate virality factors
    assert engine.evaluate_virality_factors(1.5, 0.8) == pytest.approx(1.2)

    # Measure brand emergence
    assert engine.measure_brand_emergence(0.8, 0.7) == pytest.approx(0.56)

    # Compute brand authority
    assert engine.compute_brand_authority(10, 0.8) == pytest.approx(0.9)

    # Calculate positioning perception shift
    assert engine.calculate_positioning_perception_shift(0.5, 0.4) == pytest.approx(0.7)

    # Model multi channel interaction
    assert engine.model_multi_channel_interaction(100.0, 200.0, 0.3) == pytest.approx(156.0)


def test_layer9_sales() -> None:
    from apodex.ai_eos.intelligence.computational_architecture import CustomerPsychologyModel
    engine = SalesEngine()
    urgency = engine.calculate_buying_urgency(10.0, 5, 0.2)
    assert urgency == pytest.approx(10.0 * math.exp(-1.0))

    closing_prob = engine.resolve_objection_state(
        customer_objections=["price", "onboarding", "security"],
        resolved_objections={"price", "security"}
    )
    assert closing_prob == pytest.approx(2.0 / 3.0)

    # Simulate sales psychology transition
    assert engine.simulate_sales_psychology_transition(1.0, 2.0, 3.0) > 0.9

    # Generate sales objections
    cust = CustomerPsychologyModel(price_sensitivity=0.8, risk_aversion=0.8, inertia_strength=0.8)
    objections = engine.generate_sales_objections(cust)
    assert "pricing_objection" in objections
    assert "risk_objection" in objections
    assert "switching_inertia_objection" in objections

    # Should automate sales
    assert engine.should_automate_sales(3000.0, 0.2)
    assert not engine.should_automate_sales(8000.0, 0.5)

    # Is enterprise sales necessary
    assert engine.is_enterprise_sales_necessary(60000.0, 2)
    assert not engine.is_enterprise_sales_necessary(30000.0, 2)

    # Design repeatable sales funnel
    funnel = engine.design_repeatable_sales_funnel(1000, [0.5, 0.5, 0.5, 0.5])
    assert funnel["lead_in"] == 1000
    assert funnel["qualified"] == 500
    assert funnel["demo_completed"] == 250
    assert funnel["closed_won"] == 62.5


def test_layer10_growth() -> None:
    engine = GrowthEngine()
    network_utility = engine.calculate_network_effects_utility(100, 0.05)
    assert network_utility == 500.0

    slowdown = engine.evaluate_intentional_slowdown_trigger(churn_rate=0.15, support_sla_latency_hours=12.0)
    assert slowdown

    # Detect network effects emergence
    assert engine.detect_network_effects_emergence(20, 100)
    assert not engine.detect_network_effects_emergence(5, 100)

    # Evaluate ecosystem formation
    assert engine.evaluate_ecosystem_formation(10, 50000) == pytest.approx(6.2)

    # Evaluate platform transition
    assert engine.evaluate_platform_transition(50.0, 0.1)
    assert not engine.evaluate_platform_transition(150.0, 0.3)

    # Predict long term success metrics
    predictions = engine.predict_long_term_success_metrics(4.0, 1.2)
    assert predictions["is_scalable"]
    assert predictions["ltv_to_cac_ratio"] == 4.0


def test_layer11_competition() -> None:
    engine = CompetitionEngine()
    moat = engine.calculate_moat_strength(10.0, 5.0)
    assert moat == 15.0

    # Simple Pure Strategy Nash Equilibrium check
    # Strategies: Low, High
    payoff_matrix = {
        ("Low", "Low"): (5.0, 5.0),
        ("Low", "High"): (0.0, 8.0),
        ("High", "Low"): (8.0, 0.0),
        ("High", "High"): (2.0, 2.0)
    }
    eq = engine.compute_nash_equilibrium_payoff(
        player_a_strategies=["Low", "High"],
        player_b_strategies=["Low", "High"],
        payoff_matrix=payoff_matrix
    )
    # Nash Equilibrium is (High, High) in a prisoner's dilemma matrix
    assert ("High", "High") in eq

    # Anticipate competitor moves
    assert engine.anticipate_competitor_moves("low_price") == "value_differentiation"
    assert engine.anticipate_competitor_moves("unknown") == "first_principles_innovation"

    # Evaluate barrier to imitation
    assert engine.evaluate_barrier_to_imitation(0.8, 0.6) == pytest.approx(0.7)

    # Evaluate pivot triggers
    assert engine.evaluate_pivot_triggers(500.0, 300.0, 12.0)
    assert engine.evaluate_pivot_triggers(100.0, 500.0, 2.0)
    assert not engine.evaluate_pivot_triggers(100.0, 500.0, 10.0)

    # Simulate disruption survival
    assert engine.simulate_disruption_survival(50000.0, 5000.0, 0.5)
    assert not engine.simulate_disruption_survival(20000.0, 5000.0, 0.5)


def test_layer12_organizational_design() -> None:
    engine = OrganizationalDesignEngine()
    price_active = engine.calculate_lagrange_shadow_price(
        current_utilization=120.0, capacity_limit=100.0, marginal_revenue=500.0
    )
    assert price_active == 600.0

    price_inactive = engine.calculate_lagrange_shadow_price(
        current_utilization=80.0, capacity_limit=100.0, marginal_revenue=500.0
    )
    assert price_inactive == 0.0

    # Determine centralization policy
    assert engine.determine_centralization_policy(0.9, 0.1) == "CENTRALIZED_EXECUTIVE_COMMAND"
    assert engine.determine_centralization_policy(0.2, 0.8) == "DECENTRALIZED_LOCAL_AUTONOMY"
    assert engine.determine_centralization_policy(0.5, 0.5) == "HYBRID_DELEGATED_POLICY"

    # Determine delegation policy
    assert engine.determine_delegation_policy(0.8, 0.5) == "FULL_DELEGATION"
    assert engine.determine_delegation_policy(0.5, 0.7) == "SUPERVISED_DELEGATION"
    assert engine.determine_delegation_policy(0.2, 0.9) == "RETAIN_IN_CORE"

    # Evolve organizational structure
    assert engine.evolve_organizational_structure(5) == "FLAT_COHESIVE_FOUNDING_TEAM"
    assert engine.evolve_organizational_structure(25) == "FUNCTIONAL_DEPARTMENTS"
    assert engine.evolve_organizational_structure(100) == "MATRIX_OR_PRODUCT_DIVISIONS"

    # Scale decision making systems
    assert engine.scale_decision_making_systems(10, 5) == 25.0


def test_layer13_meta_learning() -> None:
    engine = MetaLearningEngine()
    original_instructions = "Objective: build high value ventures."
    updated = engine.run_textgrad_optimization(
        ["Failed due to severe bottleneck in support capacity."], original_instructions
    )
    assert "[TextGrad Meta Update]" in updated
    assert "Lagrange multiplier shadow price" in updated

    # Evaluate decision quality
    assert engine.evaluate_decision_quality(100.0, 80.0, 0.9) == pytest.approx(0.82)
    assert engine.evaluate_decision_quality(0.0, 10.0, 0.9) == 0.0

    # Train intuition feedback loop
    assert engine.train_intuition_feedback_loop(0.6, 0.8) == pytest.approx(0.62)

    # Calculate competitive learning rate
    assert engine.calculate_competitive_learning_rate(10.0, 5.0) == 2.0

    # Convert failures to rules
    assert engine.convert_failures_to_rules(["objection handling error"]) == ["PREVENT_RECURRENCE_OF_OBJECTION_HANDLING_ERROR"]


def test_layer14_ai_entrepreneurship() -> None:
    engine = AIEntrepreneurshipEngine()
    opp1 = Opportunity(name="Opp 1", description="", expected_value=1000.0, downside_risk_var=10.0)
    opp2 = Opportunity(name="Opp 2", description="", expected_value=3000.0, downside_risk_var=30.0)

    allocations = engine.allocate_capital_and_compute([opp1, opp2], 10000.0, 100.0)

    # Opp 2 has 3x Opp 1 EV, so gets 75% of capital and compute
    cap_2, comp_2 = allocations[opp2.opportunity_id]
    assert cap_2 == 7500.0
    assert comp_2 == 75.0

    # Rank opportunities
    ranked = engine.rank_opportunities([opp1, opp2])
    # opp1 EV/VaR = 1000/10 = 100. opp2 EV/VaR = 3000/30 = 100.
    # ranked can be either, but confirms it handles sorting
    assert len(ranked) == 2

    # Select experimental designs
    assert engine.select_experimental_designs(["customer_willingness"]) == ["RUN_ACTIVE_LEARNING_EXPERIMENT_ON_CUSTOMER_WILLINGNESS"]

    # Evaluate entrepreneurial performance
    assert engine.evaluate_entrepreneurial_performance(10000.0, 15000.0) > 0.0
    assert engine.evaluate_entrepreneurial_performance(0.0, 15000.0) == 0.0


def test_orchestrator_integration() -> None:
    orchestrator = EntrepreneurialIntelligenceOrchestrator()
    signals = {"machine_learning": 0.8, "healthcare": 0.6, "bad_noise": 0.1}

    result = orchestrator.run_full_cognitive_cycle(
        raw_market_signals=signals, available_capital=50000.0, compute_hours=200.0
    )

    assert "discovered_opportunity" in result
    assert result["novelty_score"] > 0.0
    assert "expected_value" in result
    assert result["expected_value"] > 0.0
    assert result["system_instructions_length"] > 0
