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


def test_layer1_reality_macro() -> None:
    opt = RealityOptimizer(human_risk_aversion=3.0, cognitive_energy_weight=2.0)
    u_ent = opt.calculate_global_objective(
        expected_revenue=1000.0,
        value_at_risk=100.0,
        cognitive_energy_expended=5.0,
        capital_cost=10.0,
        regulatory_tariff_shocks=0.1
    )
    assert math.isclose(u_ent, 18.6)


def test_layer1_reality() -> None:
    opt = RealityOptimizer(human_risk_aversion=3.0, cognitive_energy_weight=2.0)
    u_ent = opt.calculate_global_objective(
        expected_revenue=1000.0,
        value_at_risk=100.0,
        cognitive_energy_expended=5.0,
        capital_cost=10.0
    )
    assert math.isclose(u_ent, 22.6)

    # Test automation boundaries
    is_auto, reason = opt.map_automation_boundaries("dynamic_pricing_optimization", 0.3)
    assert is_auto
    assert reason == "AUTOMATABLE_DETERMINISTIC"

    is_auto_emp, reason_emp = opt.map_automation_boundaries("empathy_customer_interview", 0.9)
    assert not is_auto_emp
    assert reason_emp == "HUMAN_PSYCHOLOGY_BOUND"


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

    # Test prediction arrival
    t_arr = engine.predict_market_arrival_time([0.2, 0.3, 0.4], 100.0)
    assert t_arr == pytest.approx(math.log(100.0) / 0.3)


def test_layer3_problem_discovery() -> None:
    engine = ProblemDiscoveryEngine()
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

    # Ignore checks
    assert engine.should_ignore_problem(0.05, 100.0, 500.0)
    assert engine.should_ignore_problem(0.5, 600.0, 500.0)
    assert not engine.should_ignore_problem(0.4, 100.0, 500.0)


def test_layer4_decision_making_fatigue() -> None:
    engine = DecisionMakingEngine(min_confidence_threshold=0.3)
    should_kill_normal = engine.should_kill_idea(10.0, 10.0, 6, cognitive_exhaustion_score=0.0)
    assert not should_kill_normal

    assert not engine.should_kill_idea(3.5, 6.5, 6, cognitive_exhaustion_score=0.0)
    assert engine.should_kill_idea(3.5, 6.5, 6, cognitive_exhaustion_score=1.0)

    # Attention ratio
    assert engine.allocate_attention_ratio(10.0, 5.0, 2.0) == 25.0


def test_layer4_decision_making() -> None:
    engine = DecisionMakingEngine(min_confidence_threshold=0.3)
    a, b = engine.compute_confirmation_bias_adjusted_priors(
        alpha_prior=5.0, beta_prior=5.0, positive_evidence=12, negative_evidence=4, bias_factor=1.2
    )
    assert math.isclose(a, 15.0)
    assert math.isclose(b, 9.8)

    assert engine.should_kill_idea(1.0, 9.0, 10)
    assert not engine.should_kill_idea(8.0, 2.0, 10)


def test_layer5_evaluation() -> None:
    engine = OpportunityEvaluationEngine()
    ev = engine.calculate_expected_value(market_size=100000.0, success_probability=0.7, launch_cost=20000.0)
    assert ev == 50000.0

    var = engine.estimate_value_at_risk(ev, 5000.0)
    assert var == 0.0

    # Timing windows
    t_early = engine.evaluate_timing_score(1.0, 5.0, 10.0)
    assert t_early < 1.0
    t_opt = engine.evaluate_timing_score(7.0, 5.0, 10.0)
    assert t_opt == 1.0

    # Abandonment
    assert engine.should_abandon_opportunity(100.0, 200.0, 1.0)
    assert not engine.should_abandon_opportunity(250.0, 200.0, 1.0)


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine(max_complexity_budget=50.0)
    features, total = engine.enforce_complexity_cap([10.0, 15.0, 20.0, 30.0])
    assert features == [10.0, 15.0, 20.0]
    assert total == 45.0

    jtbd_score = engine.compute_jtbd_alignment({"f1": 0.8, "f2": 0.4})
    assert jtbd_score == pytest.approx(0.6)

    # Epistemic info gain
    assert engine.calculate_epistemic_information_gain(2.5, 1.5) == 1.0


def test_layer7_customer_understanding_reputation() -> None:
    engine = CustomerUnderstandingEngine()
    prob_rep = engine.evaluate_switching_probability(
        current_product_utility=5.0,
        proposed_product_utility=5.0,
        switching_costs=1.0,
        push_forces=0.0,
        pull_forces=0.0,
        reputation_score=3.0,
        trust_decay_coefficient=0.0
    )
    assert prob_rep > 0.52

    prob_decay = engine.evaluate_switching_probability(
        current_product_utility=5.0,
        proposed_product_utility=5.0,
        switching_costs=1.0,
        push_forces=0.0,
        pull_forces=0.0,
        reputation_score=3.0,
        trust_decay_coefficient=0.5
    )
    assert prob_decay < prob_rep

    # Evangelism score
    assert engine.compute_evangelism_score(10.0, 5.0) == pytest.approx(1.0 / (1.0 + math.exp(-5.0)))


def test_layer7_customer_understanding() -> None:
    engine = CustomerUnderstandingEngine()
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
    attention_curve = engine.simulate_viral_attention_spread(
        initial_aware_cohort=0.1, viral_factor_k=1.5, exposure_rate=0.8, steps=3
    )
    assert len(attention_curve) == 4
    assert all(0.0 <= val <= 1.0 for val in attention_curve)

    # Positioning distance
    assert engine.calculate_positioning_distance([1.0, 2.0], [4.0, 6.0]) == 5.0


def test_layer9_sales() -> None:
    engine = SalesEngine()
    urgency = engine.calculate_buying_urgency(10.0, 5, 0.2)
    assert urgency == pytest.approx(10.0 * math.exp(-1.0))

    closing_prob = engine.resolve_objection_state(
        customer_objections=["price", "onboarding", "security"],
        resolved_objections={"price", "security"}
    )
    assert closing_prob == pytest.approx(2.0 / 3.0)

    # Sales automation channel mapping
    assert engine.select_sales_channel_by_acv(60000.0) == "ENTERPRISE_HUMAN_SALES"
    assert engine.select_sales_channel_by_acv(10000.0) == "INSIDE_SALES_HYBRID"
    assert engine.select_sales_channel_by_acv(100.0) == "AUTOMATED_SELF_SERVE"


def test_layer10_growth() -> None:
    engine = GrowthEngine()
    network_utility = engine.calculate_network_effects_utility(100, 0.05)
    assert network_utility == 500.0

    slowdown = engine.evaluate_intentional_slowdown_trigger(churn_rate=0.15, support_sla_latency_hours=12.0)
    assert slowdown

    # Compound growth forecasting
    assert engine.predict_compound_growth(1000, 0.9, 0.2, 2) == pytest.approx(1210.0)


def test_layer11_competition_deception() -> None:
    engine = CompetitionEngine()
    payoff_matrix = {
        ("Low", "Low"): (5.0, 5.0),
        ("Low", "High"): (0.0, 8.0),
        ("High", "Low"): (8.0, 0.0),
        ("High", "High"): (2.0, 2.0)
    }
    eq_normal = engine.compute_nash_equilibrium_payoff(
        player_a_strategies=["Low", "High"],
        player_b_strategies=["Low", "High"],
        payoff_matrix=payoff_matrix,
        deceptive_signal_factor_b=0.0
    )
    assert ("High", "High") in eq_normal

    eq_deceptive = engine.compute_nash_equilibrium_payoff(
        player_a_strategies=["Low", "High"],
        player_b_strategies=["Low", "High"],
        payoff_matrix=payoff_matrix,
        deceptive_signal_factor_b=10.0
    )
    assert len(eq_deceptive) > 0

    # Pivot check
    assert engine.should_pivot(10.0, 14.0)
    assert not engine.should_pivot(10.0, 11.0)


def test_layer11_competition() -> None:
    engine = CompetitionEngine()
    moat = engine.calculate_moat_strength(10.0, 5.0)
    assert moat == 15.0


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


def test_layer13_meta_learning() -> None:
    engine = MetaLearningEngine()
    original_instructions = "Objective: build high value ventures."
    updated = engine.run_textgrad_optimization(
        ["Failed due to severe bottleneck in support capacity."], original_instructions
    )
    assert "[TextGrad Meta Update]" in updated
    assert "Lagrange multiplier shadow price" in updated

    # Decision quality
    assert engine.calculate_decision_quality(100.0, 0.4, 0.1) == 200.0


def test_layer14_ai_entrepreneurship_kelly() -> None:
    engine = AIEntrepreneurshipEngine()
    opp1 = Opportunity(name="Opp 1", description="", expected_value=1000.0)
    opp2 = Opportunity(name="Opp 2", description="", expected_value=3000.0)

    p_overrides = {opp1.opportunity_id: 0.6, opp2.opportunity_id: 0.8}
    odds_overrides = {opp1.opportunity_id: 1.5, opp2.opportunity_id: 2.0}

    allocations = engine.allocate_capital_and_compute_kelly(
        [opp1, opp2], 10000.0, 100.0, p_overrides, odds_overrides
    )

    cap_1, comp_1 = allocations[opp1.opportunity_id]
    cap_2, comp_2 = allocations[opp2.opportunity_id]

    assert math.isclose(cap_1, 10000.0 * (0.3333333333333333 / 1.0333333333333332), rel_tol=1e-4)
    assert math.isclose(cap_2, 10000.0 * (0.7 / 1.0333333333333332), rel_tol=1e-4)


def test_orchestrator_integration() -> None:
    orchestrator = EntrepreneurialIntelligenceOrchestrator()
    signals = {"machine_learning": 0.8, "healthcare": 0.6, "bad_noise": 0.1}

    result = orchestrator.run_full_cognitive_cycle(
        raw_market_signals=signals, available_capital=50000.0, compute_hours=200.0, regulatory_tariff_shocks=0.1
    )

    assert "discovered_opportunity" in result
    assert result["novelty_score"] > 0.0
    assert "expected_value" in result
    assert result["expected_value"] > 0.0
    assert result["global_utility"] > 0.0
    assert result["cognitive_exhaustion"] == 0.05
