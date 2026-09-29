"""
Unit and integration tests for the 14-Layer Computational Engine of Entrepreneurship.
"""

import pytest
from apodex.ai_eos.intelligence import (
    RealitySubstrate,
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
    FourteenLayerEntrepreneurshipOrchestrator,
)


def test_reality_substrate():
    substrate = RealitySubstrate()
    val = substrate.evaluate_transformation(delta_utility=10.0, energy_cost=2.0)
    assert val == 10.0  # 1.2 * 10 - 2 = 10


def test_opportunity_discovery_engine():
    discovery = OpportunityDiscoveryEngine()
    signals = [
        {"name": "Signal Low", "signal_amplitude": 0.5, "noise_variance": 1.0, "novelty": 0.2, "tam": 100000},
        {"name": "Signal High A", "signal_amplitude": 5.0, "noise_variance": 1.0, "novelty": 0.8, "tam": 2000000},
        {"name": "Signal High B", "signal_amplitude": 8.0, "noise_variance": 1.0, "novelty": 0.9, "tam": 5000000},
    ]
    detected = discovery.detect_weak_signals(signals)
    assert len(detected) == 2

    synth = discovery.synthesize_cross_domain_opportunity(detected[0], detected[1])
    assert "Signal High A" in synth["title"]
    assert synth["estimated_tam"] == 7000000


def test_problem_discovery_engine():
    engine = ProblemDiscoveryEngine()
    dag = engine.decompose_problem_dag("Root Friction", ["Sub 1", "Sub 2", "Sub 3"])
    assert dag["root"] == "Root Friction"
    assert len(dag["first_order"]) == 2
    assert len(dag["second_order"]) == 1

    assert engine.calculate_resolution_viability(100.0, 150.0) is True
    assert engine.calculate_resolution_viability(100.0, 105.0) is False


def test_decision_making_engine():
    engine = DecisionMakingEngine()
    efe = engine.calculate_expected_free_energy(
        p_success=0.8, p_target=0.9, prior_entropy=1.5, post_entropy=0.5, curiosity_weight=1.0
    )
    assert isinstance(efe, float)


def test_opportunity_evaluation_engine():
    engine = OpportunityEvaluationEngine()
    res = engine.evaluate_opportunity(tam=10000000, margin=0.8, p_success=0.5, capital_required=50000)
    assert res["expected_value"] == 4000000 - 50000
    assert res["var_95"] > 0


def test_product_creation_engine():
    engine = ProductCreationEngine()
    features = [
        {"name": "Low ROI Feature", "complexity": 3.0, "wtp": 10.0},
        {"name": "High ROI Feature", "complexity": 1.0, "wtp": 100.0},
    ]
    pruned = engine.prune_features_by_wtp(features, max_complexity_budget=2.0)
    assert len(pruned) == 1
    assert pruned[0]["name"] == "High ROI Feature"


def test_customer_understanding_engine():
    engine = CustomerUnderstandingEngine()
    u = engine.compute_customer_utility(1.0, 0.2, 0.1)
    assert u == pytest.approx(0.87)

    p_switch = engine.evaluate_switching_likelihood(new_utility=2.0, current_utility=1.0, switching_cost=0.5)
    assert p_switch > 0.5


def test_marketing_engine():
    engine = MarketingEngine()
    spread = engine.simulate_viral_spread(initial_users=100, virality_rate=0.2, churn_rate=0.05, timesteps=5)
    assert len(spread) == 6
    assert spread[-1] > spread[0]


def test_sales_engine():
    engine = SalesEngine()
    funnel = engine.execute_sales_funnel_fsm(1000, [0.1, 0.5, 0.4, 0.8])
    assert funnel["leads"] == 1000
    assert funnel["qualified"] == 100
    assert funnel["closed_won"] == 16


def test_growth_and_competition_engines():
    growth = GrowthEngine()
    comp = CompetitionEngine()
    nv = growth.calculate_network_value(100)
    assert nv == 100.0

    moat = comp.evaluate_moat_strength(0.8, 0.8, 0.8, 0.8)
    assert moat == 0.8


def test_org_design_and_meta_learning():
    org = OrganizationalDesignEngine()
    meta = MetaLearningEngine()

    strat = org.determine_delegation_strategy(task_complexity=5.0, bandwidth_limit=3.0)
    assert strat == "DELEGATE_TO_SUB_AGENTS"

    new_prior = meta.update_priors_from_failure(current_prior=0.8, failure_severity=0.5)
    assert new_prior == pytest.approx(0.7)


def test_ai_entrepreneurship_engine():
    ai_eng = AIEntrepreneurshipEngine()
    opps = [{"title": "Venture A", "score": 2.0}, {"title": "Venture B", "score": 1.0}]
    alloc = ai_eng.allocate_resources(opps, total_capital=300000.0, total_compute=300.0)
    assert len(alloc) == 2
    assert alloc[0]["allocated_capital"] == 200000.0
    assert alloc[1]["allocated_capital"] == 100000.0


def test_fourteen_layer_orchestrator_e2e():
    orchestrator = FourteenLayerEntrepreneurshipOrchestrator()
    raw_signals = [
        {"name": "AI Search Disruption", "signal_amplitude": 6.0, "noise_variance": 1.0, "novelty": 0.85, "tam": 10000000},
        {"name": "Automated Legal Workflows", "signal_amplitude": 7.0, "noise_variance": 1.0, "novelty": 0.9, "tam": 20000000},
    ]

    result = orchestrator.run_full_14_layer_pipeline(raw_signals, total_capital=500000.0, total_compute=5000.0)

    assert result["status"] == "success"
    assert "opportunity" in result
    assert "problem_dag" in result
    assert "expected_free_energy" in result
    assert "evaluation" in result
    assert "product_features" in result
    assert "sales_funnel" in result
    assert "moat_score" in result
    assert "resource_allocations" in result
