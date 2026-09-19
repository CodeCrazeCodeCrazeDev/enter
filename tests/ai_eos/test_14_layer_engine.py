"""
Unit and integration test suite for the 14-Layer Computational Architecture Engine.
"""

import pytest
from apodex.ai_eos.intelligence import (
    MarketSignal,
    OpportunityCandidate,
    ProblemStatement,
    ProductSpecification,
    CustomerProfile,
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
    FourteenLayerEntrepreneurialEngine,
)


def test_reality_substrate_engine_invariants():
    engine = RealitySubstrateEngine()
    opp = OpportunityCandidate(
        title="High Margin SaaS",
        domain="saas",
        ltv_cents=300000,
        cac_cents=50000,
        capital_required_cents=1000000,
        success_probability=0.7
    )
    result = engine.evaluate_invariant_compliance(opp)
    assert result["is_viable"] is True
    assert result["invariants"]["asymmetric_risk_reward"] is True
    assert result["ltv_cac_ratio"] == 6.0


def test_opportunity_discovery_engine():
    engine = OpportunityDiscoveryEngine()
    s1 = MarketSignal(source="arxiv", content="Active Inference paper", entropy_score=1.2, growth_rate=0.15, domain="ai")
    s2 = MarketSignal(source="github", content="SaaS framework repo", entropy_score=1.1, growth_rate=0.12, domain="saas")

    flagged = engine.detect_weak_signals([s1, s2])
    assert len(flagged) == 2

    opp = engine.synthesize_cross_domain_opportunity(s1, s2)
    assert opp.domain == "ai_saas"
    assert len(opp.variables) == 3


def test_problem_discovery_engine():
    engine = ProblemDiscoveryEngine()
    nodes = ["inefficient_infra", "slow_queries", "user_churn"]
    edges = [("inefficient_infra", "slow_queries"), ("slow_queries", "user_churn")]

    problem = engine.decompose_and_abduct_root_causes("high user churn", nodes, edges)
    assert problem.stated_symptom == "high user churn"
    assert "inefficient_infra" in problem.root_cause_variables
    assert problem.leverage_scores["inefficient_infra"] == 0.95


def test_decision_making_engine_efe():
    engine = DecisionMakingEngine()
    opp = OpportunityCandidate(
        title="Active Inference Opp",
        domain="ai",
        prior_entropy=1.5,
        post_entropy_simulated=0.3,
        success_probability=0.8,
        target_preference=0.95
    )
    efe = engine.calculate_expected_free_energy(opp)
    assert efe < 0.0  # Favorable policy outcome
    assert engine.evaluate_kill_criteria(opp, threshold=0.1) is False


def test_opportunity_evaluation_sharpe():
    engine = OpportunityEvaluationEngine()
    opp = OpportunityCandidate(
        title="Fintech Engine",
        domain="fintech",
        tam_cents=1000000000,
        capital_required_cents=2000000,
        success_probability=0.6,
        prior_entropy=1.2
    )
    sharpe = engine.compute_sharpe_opportunity_score(opp)
    assert sharpe > 0.0

    cvar = engine.estimate_cvar_downside(opp)
    assert cvar >= opp.capital_required_cents


def test_product_creation_engine_shapley():
    engine = ProductCreationEngine()
    spec = ProductSpecification(name="AI Platform", max_complexity_budget=1.2)
    features = {"core_kernel": 0.9, "advanced_viz": 0.5, "dark_mode": 0.1}

    optimized_spec = engine.optimize_feature_set(spec, features)
    assert "core_kernel" in optimized_spec.features
    assert "advanced_viz" in optimized_spec.features
    assert "dark_mode" not in optimized_spec.features
    assert optimized_spec.kolmogorov_complexity <= 1.2


def test_customer_understanding_switching():
    engine = CustomerUnderstandingEngine()
    profile = CustomerProfile(segment_name="B2B", friction_aversion=1.0, switching_cost_cents=10000)
    result = engine.evaluate_switching_decision(profile, new_product_utility=20.0, price_cents=5000)
    assert result["will_switch"] is True


def test_marketing_growth_sales_engines():
    mkt = MarketingEngine()
    viral_res = mkt.calculate_viral_coefficient(1.6, 0.7)
    assert viral_res["is_exponential"] is True

    sales = SalesEngine()
    urgency_res = sales.evaluate_buying_urgency(cost_of_inaction_cents_per_month=2000, price_cents=10000)
    assert urgency_res["has_buying_urgency"] is True

    growth = GrowthEngine()
    growth_res = growth.evaluate_growth_health(ltv_cents=30000, cac_cents=8000, payback_months=6, nrr_percent=125.0)
    assert growth_res["is_healthy"] is True


def test_competition_org_meta_ai_engines():
    comp = CompetitionEngine()
    moat = comp.compute_moat_defendability_score(0.8, 0.8, 0.8)
    assert moat == pytest.approx(0.8)

    org = OrganizationalDesignEngine()
    hiring = org.evaluate_hiring_trigger(0.9, 0.85)
    assert hiring["should_hire"] is True

    meta = MetaLearningEngine()
    updated = meta.update_mental_model_prior(prior_belief=0.5, experimental_evidence=0.9, likelihood=0.8)
    assert updated > 0.5

    ai = AIEntrepreneurshipEngine()
    opp1 = OpportunityCandidate(title="Opp 1", domain="tech", success_probability=0.85, tam_cents=500000000)
    opp2 = OpportunityCandidate(title="Opp 2", domain="bio", success_probability=0.35, tam_cents=100000000)
    allocations = ai.allocate_capital_and_compute([opp1, opp2], total_capital_cents=1000000, total_compute_flops=1e12)
    assert len(allocations) == 2
    assert allocations[opp1.opportunity_id]["capital_allocated_cents"] > allocations[opp2.opportunity_id]["capital_allocated_cents"]


def test_fourteen_layer_orchestrator_pipeline():
    orchestrator = FourteenLayerEntrepreneurialEngine()
    s1 = MarketSignal(source="arxiv", content="Paper A", entropy_score=1.3, growth_rate=0.2, domain="ai")
    s2 = MarketSignal(source="market", content="Trend B", entropy_score=1.1, growth_rate=0.1, domain="fintech")

    orchestrator.ingest_market_signal(s1)
    orchestrator.ingest_market_signal(s2)

    result = orchestrator.execute_full_14_layer_pipeline(total_capital_cents=50000000)

    assert result["status"] == "completed"
    assert "layer1_invariants" in result
    assert "layer3_problem" in result
    assert "layer4_efe" in result
    assert "layer5_sharpe_score" in result
    assert "layer6_product_complexity" in result
    assert "layer14_allocations" in result
