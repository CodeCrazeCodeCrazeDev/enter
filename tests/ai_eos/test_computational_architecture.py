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


def test_layer3_problem_discovery() -> None:
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


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine(max_complexity_budget=50.0)
    features, total = engine.enforce_complexity_cap([10.0, 15.0, 20.0, 30.0])
    assert features == [10.0, 15.0, 20.0]
    assert total == 45.0

    jtbd_score = engine.compute_jtbd_alignment({"f1": 0.8, "f2": 0.4})
    assert jtbd_score == pytest.approx(0.6)


def test_layer7_customer_understanding() -> None:
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


def test_layer8_marketing() -> None:
    engine = MarketingEngine()
    attention_curve = engine.simulate_viral_attention_spread(
        initial_aware_cohort=0.1, viral_factor_k=1.5, exposure_rate=0.8, steps=3
    )
    assert len(attention_curve) == 4
    # Attention must increase or stay within bounds
    assert all(0.0 <= val <= 1.0 for val in attention_curve)


def test_layer9_sales() -> None:
    engine = SalesEngine()
    urgency = engine.calculate_buying_urgency(10.0, 5, 0.2)
    assert urgency == pytest.approx(10.0 * math.exp(-1.0))

    closing_prob = engine.resolve_objection_state(
        customer_objections=["price", "onboarding", "security"],
        resolved_objections={"price", "security"}
    )
    assert closing_prob == pytest.approx(2.0 / 3.0)


def test_layer10_growth() -> None:
    engine = GrowthEngine()
    network_utility = engine.calculate_network_effects_utility(100, 0.05)
    assert network_utility == 500.0

    slowdown = engine.evaluate_intentional_slowdown_trigger(churn_rate=0.15, support_sla_latency_hours=12.0)
    assert slowdown


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


def test_layer14_ai_entrepreneurship() -> None:
    engine = AIEntrepreneurshipEngine()
    opp1 = Opportunity(name="Opp 1", description="", expected_value=1000.0)
    opp2 = Opportunity(name="Opp 2", description="", expected_value=3000.0)

    allocations = engine.allocate_capital_and_compute([opp1, opp2], 10000.0, 100.0)

    # Opp 2 has 3x Opp 1 EV, so gets 75% of capital and compute
    cap_2, comp_2 = allocations[opp2.opportunity_id]
    assert cap_2 == 7500.0
    assert comp_2 == 75.0


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
