"""Unit and integration test suite for the 14-Layer Computational Engine of AI Entrepreneurship."""

import pytest
from apodex.ai_eos.intelligence import (
    SignalVector,
    ProblemNode,
    OpportunityModel,
    FeatureCandidate,
    CustomerState,
    DecisionRecord,
    Layer1RealitySubstrateEngine,
    Layer2OpportunityDiscoveryEngine,
    Layer3ProblemDiscoveryEngine,
    Layer4DecisionMakingEngine,
    Layer5OpportunityEvaluationEngine,
    Layer6ProductCreationEngine,
    Layer7CustomerUnderstandingEngine,
    Layer8MarketingEngine,
    Layer9SalesEngine,
    Layer10GrowthEngine,
    Layer11CompetitionEngine,
    Layer12OrganizationalDesignEngine,
    Layer13MetaLearningEngine,
    Layer14AIEntrepreneurshipOrchestrator,
    FourteenLayerEntrepreneurialEngine
)


def test_layer1_reality_substrate():
    engine = Layer1RealitySubstrateEngine()
    pv = engine.evaluate_arbitrage_value(utility_captured=100.0, friction_cost=20.0, time_horizon=5.0, discount_rate=0.05)
    assert pv > 0.0
    assert engine.verify_positive_sum_exchange(buyer_utility=100.0, price=50.0, seller_cost=20.0) is True
    assert engine.verify_positive_sum_exchange(buyer_utility=40.0, price=50.0, seller_cost=20.0) is False


def test_layer2_opportunity_discovery():
    engine = Layer2OpportunityDiscoveryEngine()
    s1 = SignalVector(source="market_trends", value=3.5, historical_mean=1.0, historical_std=0.5)
    s2 = SignalVector(source="tech_breakthrough", value=10.0, historical_mean=2.0, historical_std=1.0)

    a1 = engine.compute_anomaly_index(s1)
    assert a1 == pytest.approx(5.0)

    novelty = engine.fuse_signals_and_generate_novelty(s1, s2)
    assert novelty > 0.0


def test_layer3_problem_discovery():
    engine = Layer3ProblemDiscoveryEngine()
    p1 = ProblemNode(description="Slow onboarding workflow", solution_cost=500.0, addressable_friction=5000.0, causal_leverage=0.8)
    res = engine.analyze_problem(p1, causal_intervention_delta=0.6)

    assert res["is_root_cause"] is True
    assert res["worth_solving"] is True
    assert res["action"] == "Solve"


def test_layer4_decision_making_active_inference():
    engine = Layer4DecisionMakingEngine()
    opp = OpportunityModel(title="AI Agent Platform", prior_entropy=2.0, post_entropy_simulated=0.5, success_probability=0.7, target_preference=0.9)

    efe = engine.calculate_expected_free_energy(opp)
    assert isinstance(efe, float)

    kill = engine.evaluate_kill_gate(opp, pmf_posterior_prob=0.1, kill_threshold=0.2)
    assert kill is True


def test_layer5_opportunity_evaluation():
    engine = Layer5OpportunityEvaluationEngine()
    opp = OpportunityModel(title="SaaS Tool", expected_value=1_000_000.0, downside_risk=100_000.0, timing_index=1.5)

    eval_res = engine.evaluate_opportunity(opp)
    assert eval_res["viable"] is True
    assert eval_res["timing_adjusted_ev"] == pytest.approx(1_350_000.0)

    # Candidate has lower EFE rate (better)
    assert engine.evaluate_opportunity_switch(current_efe_rate=2.5, candidate_efe_rate=1.0, switching_cost=0.5) is True


def test_layer6_product_creation():
    engine = Layer6ProductCreationEngine()
    jtbd_utility = engine.calculate_jtbd_utility(outcome_speed=10.0, reliability=0.9, cognitive_effort=1.0, friction=1.0)
    assert jtbd_utility == pytest.approx(4.5)

    f_good = FeatureCandidate(name="One-click Checkout", utility_impact=10.0, complexity_cost=2.0)
    f_bad = FeatureCandidate(name="3D Animated Icon", utility_impact=0.1, complexity_cost=5.0)

    assert engine.evaluate_feature_inclusion(f_good) is True
    assert engine.evaluate_feature_inclusion(f_bad) is False


def test_layer7_customer_understanding():
    engine = Layer7CustomerUnderstandingEngine()
    customer = CustomerState(push_force=50.0, pull_force=50.0, anxiety_force=10.0, habit_force=10.0, switching_cost=20.0)
    assert engine.evaluate_switching_trigger(customer) is True

    updated_trust = engine.update_trust(current_trust=0.5, delivered_value=100.0, promised_value=100.0)
    assert updated_trust == pytest.approx(0.6)


def test_layer8_marketing():
    engine = Layer8MarketingEngine()
    r0 = engine.calculate_reproduction_number(transmission_rate=0.5, share_factor=0.8, recovery_rate=0.2)
    assert r0 == pytest.approx(2.0)  # Epidemic growth (viral)

    brand_auth = engine.calculate_brand_authority(brand_vector=[1.0, 0.0], aspiration_vector=[1.0, 0.0], messaging_variance=0.1)
    assert brand_auth > 0.0


def test_layer9_sales():
    engine = Layer9SalesEngine()
    urgency = engine.calculate_buying_urgency(cost_of_inaction=100_000.0, time_sensitivity=2.0, implementation_risk=10_000.0)
    assert urgency == pytest.approx(20.0)

    resolved = engine.is_objection_resolved(initial_risk=1.0, proof_strength=2.0)
    assert resolved is True


def test_layer10_growth():
    engine = Layer10GrowthEngine()
    projected = engine.project_compounding_users(current_users=1000, virality_k=0.1, retention_k=0.05, churn_rate=0.02)
    assert projected == 1130

    slowdown = engine.evaluate_slowdown_gate(churn_derivative=0.08, nps_score=40.0)
    assert slowdown is True


def test_layer11_competition():
    engine = Layer11CompetitionEngine()
    moat = engine.calculate_moat_strength(competitor_replication_cost=10_000_000.0, incumbent_operational_cost=1_000_000.0)
    assert moat == pytest.approx(10.0)

    counter_pos = engine.evaluate_counter_positioning(incumbent_revenue_cannibalization=5_000_000.0, new_entrant_profit=1_000_000.0)
    assert counter_pos is True


def test_layer12_org_design():
    engine = Layer12OrganizationalDesignEngine()
    hire = engine.evaluate_hiring_need(team_utilization=0.9, delay_cost=150_000.0, salary_cost=100_000.0)
    assert hire is True

    mode = engine.determine_decision_mode(operational_risk=0.9, local_context_specificity=0.2)
    assert mode == "Centralized"


def test_layer13_meta_learning():
    engine = Layer13MetaLearningEngine()
    records = [
        DecisionRecord(predicted_probability=0.8, ground_outcome=1),
        DecisionRecord(predicted_probability=0.9, ground_outcome=1),
        DecisionRecord(predicted_probability=0.7, ground_outcome=0)
    ]
    brier = engine.calculate_brier_score(records)
    assert brier > 0.0

    updated_conf = engine.update_confidence_prior(prior_confidence=0.8, brier_score=0.1)
    assert updated_conf > 0.8


def test_layer14_ai_orchestration():
    orchestrator = Layer14AIEntrepreneurshipOrchestrator()
    opps = [
        OpportunityModel(title="Opp A", expected_value=200_000.0, prior_entropy=1.0, post_entropy_simulated=0.2, success_probability=0.8),
        OpportunityModel(title="Opp B", expected_value=500_000.0, prior_entropy=2.0, post_entropy_simulated=0.5, success_probability=0.6)
    ]

    res = orchestrator.allocate_resources(capital_budget=100_000.0, compute_budget=500.0, opportunities=opps)
    assert len(res["allocations"]) > 0
    assert res["unallocated_capital"] >= 0.0


def test_fourteen_layer_unified_engine_full_cycle():
    engine = FourteenLayerEntrepreneurialEngine()

    signals = [
        SignalVector(source="search_volume", value=12.0, historical_mean=2.0, historical_std=1.0),
        SignalVector(source="developer_commits", value=50.0, historical_mean=10.0, historical_std=5.0)
    ]
    problems = [
        ProblemNode(description="High API Latency", solution_cost=1000.0, addressable_friction=10000.0, causal_leverage=0.9)
    ]
    opportunities = [
        OpportunityModel(title="Edge Inference SDK", expected_value=300_000.0, downside_risk=20_000.0)
    ]

    res = engine.execute_full_cycle(signals, problems, opportunities)

    assert res["status"] == "completed"
    assert len(res["fused_signals"]) == 1
    assert len(res["problem_results"]) == 1
    assert len(res["evaluated_opportunities"]) == 1
    assert "resource_allocation_plan" in res
