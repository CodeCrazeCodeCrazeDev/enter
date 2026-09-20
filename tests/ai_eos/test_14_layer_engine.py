from __future__ import annotations
import pytest

from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    GlobalState,
    OpportunitySignal,
    ProblemNode,
    DecisionContext,
    OpportunityEvaluation,
    ProductSpecification,
    CustomerModel,
    MarketingCampaign,
    SalesPipeline,
    GrowthFlywheel,
    CompetitiveMoat,
    OrganizationStructure,
    MetaLearningState,
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
    AIEntrepreneurshipOrchestrator,
    FourteenLayerEntrepreneurialEngine
)


def test_layer1_reality_substrate() -> None:
    engine = RealitySubstrateEngine()
    g_state = GlobalState(human_utility_distribution={"health": 0.8, "wealth": 0.9}, non_stationary_drift_rate=0.05)
    report = engine.evaluate_fundamental_invariants(g_state)
    assert report["total_latent_utility"] == pytest.approx(1.7)
    assert report["asymmetric_arbitrage_capacity"] == pytest.approx(0.95)
    assert "scm_causal_inference" in report["can_be_automated"]


def test_layer2_opportunity_discovery() -> None:
    engine = OpportunityDiscoveryEngine()
    sig1 = OpportunitySignal(domain="ai", entropy_shift=0.4)
    sig2 = OpportunitySignal(domain="legacy", entropy_shift=0.1)
    results = engine.search_state_space([sig1, sig2], entropy_threshold=0.3)
    assert len(results) == 1
    assert results[0].domain == "ai"


def test_layer3_problem_discovery() -> None:
    engine = ProblemDiscoveryEngine()
    node = engine.decompose_problem("System Slowdown", {"database_latency": 0.9, "network_lag": 0.3})
    assert node.root_cause_var == "database_latency"
    assert node.latent_friction_score == 0.9


def test_layer4_decision_making() -> None:
    engine = DecisionMakingEngine()
    ctx_low = DecisionContext(hypothesis_title="H1", sample_size=3)
    res_low = engine.evaluate_decision(ctx_low)
    assert res_low["decision_mode"] == "trust_intuition_and_explore"

    ctx_high = DecisionContext(hypothesis_title="H2", sample_size=15)
    res_high = engine.evaluate_decision(ctx_high)
    assert res_high["decision_mode"] == "rely_on_empirical_data"


def test_layer5_opportunity_evaluation() -> None:
    engine = OpportunityEvaluationEngine()
    eval_res = engine.evaluate(tam_cents=100000000, win_prob=0.5, downside_risk=10000.0) # $1M TAM
    assert eval_res.expected_value == 25000.0
    assert eval_res.cvar_downside_risk == 15000.0


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine()
    spec = engine.design_minimum_viable_product("Automate Billing", ["auth", "stripe", "invoicing", "analytics", "dark_mode"])
    assert len(spec.feature_set) == 3
    assert spec.complexity_score == pytest.approx(0.3)


def test_layer7_customer_understanding() -> None:
    engine = CustomerUnderstandingEngine()
    cust = CustomerModel(loss_aversion_coef=2.0, switching_friction=0.5, trust_score=0.8)
    sim = engine.simulate_buying_decision(cust, value_delta=100.0, price=20.0) # 100 - (20*2) = 60 utility. 60 - 0.5 + 0.8 = 60.3 > 0
    assert sim["will_buy"] is True


def test_layer8_marketing() -> None:
    engine = MarketingEngine()
    camp = MarketingCampaign(channel_name="seo", viral_coefficient=1.1, brand_authority_score=0.8)
    res = engine.simulate_viral_spread(camp, initial_users=100)
    assert res["projected_reach"] > 200


def test_layer9_sales() -> None:
    engine = SalesEngine()
    pipe = SalesPipeline(leads_count=100, conversion_rate=0.05, avg_contract_value=2000.0, is_enterprise=False)
    res = engine.optimize_pipeline(pipe)
    assert res["projected_arr"] == 10000.0
    assert res["should_automate_sales"] is True


def test_layer10_growth() -> None:
    engine = GrowthEngine()
    fw = GrowthFlywheel(network_participants=100, compounding_rate=0.2)
    res = engine.calculate_flywheel(fw)
    assert res["metcalfe_network_value"] == 10000
    assert res["compounded_participants"] == 120


def test_layer11_competition() -> None:
    engine = CompetitionEngine()
    moat = CompetitiveMoat(defensibility_score=0.8, switching_cost_barrier=0.8)
    res = engine.evaluate_moat_strength(moat)
    assert res["composite_moat_score"] == pytest.approx(0.8)
    assert res["is_sustainable"] is True


def test_layer12_organizational_design() -> None:
    engine = OrganizationalDesignEngine()
    org = OrganizationStructure(mrpl_over_mcl_ratio=1.5)
    res = engine.evaluate_scaling(org)
    assert res["should_hire"] is True


def test_layer13_meta_learning() -> None:
    engine = MetaLearningEngine()
    init_state = MetaLearningState(meta_policy_version=1, decision_accuracy_score=0.80)
    updated = engine.update_meta_policy(init_state, failure_observed=True)
    assert updated.meta_policy_version == 2
    assert updated.historical_failures_logged == 1
    assert updated.decision_accuracy_score == pytest.approx(0.81)


def test_layer14_ai_orchestrator() -> None:
    orchestrator = AIEntrepreneurshipOrchestrator()
    eval1 = OpportunityEvaluation(expected_value=100000.0, timing_option_value=0.9)
    eval2 = OpportunityEvaluation(expected_value=50000.0, timing_option_value=0.4)
    alloc = orchestrator.orchestrate_resource_allocation([eval1, eval2], total_capital=10000.0, total_compute=100.0)
    assert alloc["primary_opportunity_id"] == str(eval1.opportunity_id)
    assert alloc["capital_allocated"] == 7000.0
    assert alloc["compute_allocated"] == 80.0


def test_fourteen_layer_master_engine_end_to_end() -> None:
    master_engine = FourteenLayerEntrepreneurialEngine()
    raw_signal = {
        "title": "Autonomous Scientific Hardware Venture",
        "domain": "robotics",
        "tam_cents": 500000000
    }
    report = master_engine.run_end_to_end_pipeline(raw_signal)

    assert report["status"] == "completed"
    assert report["layer1_reality"]["total_latent_utility"] >= 0
    assert report["layer2_signals_found"] == 1
    assert report["layer3_root_cause"] == "high_latency"
    assert report["layer5_expected_value"] == 150000.0
    assert report["layer7_will_buy"] is True
    assert report["layer11_moat_sustainable"] is True
    assert report["layer13_meta_policy_version"] == 2
    assert "layer14_orchestration" in report
