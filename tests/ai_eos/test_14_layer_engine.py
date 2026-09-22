"""
Unit and Integration Test Suite for the 14-Layer Computational Architecture of Entrepreneurship.
"""

import pytest
from apodex.ai_eos.intelligence import (
    RealityState,
    RealitySubstrateEngine,
    SignalObservation,
    OpportunityDiscoveryEngine,
    ProblemNode,
    ProblemDiscoveryEngine,
    DecisionMakingEngine,
    CandidateOpportunity,
    OpportunityEvaluationEngine,
    FeatureProposal,
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


def test_layer_1_reality_substrate():
    engine = RealitySubstrateEngine()
    arb = engine.evaluate_arbitrage_potential(150.0, 50.0)
    assert arb["is_viable"] is True
    assert arb["arbitrage_delta"] == 100.0

    task_human = engine.partition_task_automation("ultimate_value_axiology")
    assert task_human["can_be_automated"] is False

    task_algo = engine.partition_task_automation("price_optimization")
    assert task_algo["can_be_automated"] is True


def test_layer_2_opportunity_discovery():
    engine = OpportunityDiscoveryEngine(filter_threshold=0.3)
    sig_strong = SignalObservation(domain="fintech", title="Decentralized clearing", kl_surprise=0.8, tam_estimate_usd=1e9)
    assert engine.filter_signal(sig_strong) is True

    synth = engine.synthesize_cross_domain(["AI", "Robotics"], ["Healthcare", "Agriculture"])
    assert len(synth) == 4
    assert synth[0][2] >= synth[-1][2]


def test_layer_3_problem_discovery():
    engine = ProblemDiscoveryEngine()
    p1 = ProblemNode(node_id="root_cause_1", description="Slow DB queries")
    p2 = ProblemNode(node_id="symptom_1", description="High latency")
    p3 = ProblemNode(node_id="symptom_2", description="User churn")

    edges = [("root_cause_1", "symptom_1"), ("symptom_1", "symptom_2")]
    decomp = engine.decompose_problem_dag([p1, p2, p3], edges)

    assert decomp["root_causes"] == ["root_cause_1"]
    assert decomp["symptoms"] == ["symptom_2"]
    assert engine.should_ignore_problem(10000.0, 5000.0) is True


def test_layer_4_decision_making():
    engine = DecisionMakingEngine()
    voi_res = engine.calculate_value_of_information(100.0, 200.0, 30.0)
    assert voi_res["voi"] == 100.0
    assert voi_res["net_voi"] == 70.0
    assert voi_res["should_run_experiment"] is True

    attention = engine.allocate_attention_softmax({"lever_a": 0.5, "lever_b": 1.5, "lever_c": 3.0})
    assert attention["lever_a"] > attention["lever_c"]


def test_layer_5_opportunity_evaluation():
    engine = OpportunityEvaluationEngine()
    opp = CandidateOpportunity(
        title="AI Medical Assistant",
        tam_usd=100000000.0,
        p_success=0.6,
        gross_margin=0.8,
        cac_usd=500.0,
        ltv_usd=3000.0,
        downside_risk_usd=10000.0,
    )
    eval_res = engine.evaluate_opportunity(opp)
    assert eval_res["expected_value"] == (0.6 * 3000.0) - (0.4 * 10000.0)
    assert eval_res["ltv_cac_ratio"] == 6.0
    assert eval_res["expected_free_energy"] < 0  # Pragmatic value dominates


def test_layer_6_product_creation():
    engine = ProductCreationEngine()
    good_feat = FeatureProposal(feature_name="Fast Checkout", jtbd_impact_score=9.0, complexity_cost=2.0)
    bad_feat = FeatureProposal(feature_name="3D Animations", jtbd_impact_score=1.0, complexity_cost=8.0)

    res_good = engine.anti_build_filter(good_feat)
    res_bad = engine.anti_build_filter(bad_feat)

    assert res_good["should_build"] is True
    assert res_bad["should_build"] is False


def test_layer_7_customer_understanding():
    engine = CustomerUnderstandingEngine()
    util = engine.model_customer_utility(perceive_benefit=300.0, price_usd=50.0, switching_cost=100.0)
    assert util["net_utility"] == 150.0
    assert util["will_switch"] is True

    trust = engine.update_trust_score(0.5, expected_performance=0.8, actual_performance=0.9)
    assert trust > 0.5


def test_layer_8_marketing():
    engine = MarketingEngine()
    viral_res = engine.calculate_viral_coefficient(invites_per_user=4.0, conversion_rate=0.3)
    assert viral_res["k_factor"] == 1.2
    assert viral_res["is_viral"] is True

    traj = engine.simulate_epidemic_spread(susceptible=1000.0, infected=10.0, beta=0.001, gamma=0.1, steps=5)
    assert len(traj) == 5


def test_layer_9_sales():
    engine = SalesEngine()
    step1 = engine.process_sales_funnel_transition("prospect", "qualify", 0.5)
    assert step1["next_stage"] == "qualified"

    step2 = engine.process_sales_funnel_transition("qualified", "demo", 0.8)
    assert step2["next_stage"] == "demo_completed"

    step3 = engine.process_sales_funnel_transition("demo_completed", "close", 0.85)
    assert step3["next_stage"] == "closed_won"


def test_layer_10_growth():
    engine = GrowthEngine()
    net = engine.evaluate_network_effect_utility(500)
    assert net["metcalfe_network_value"] == 250000

    comp = engine.predict_cohort_retention_compounding(initial_cohort=1000, monthly_retention_rate=0.95, months=12)
    assert comp["retained_users"] < 1000.0


def test_layer_11_competition():
    engine = CompetitionEngine()
    moat = engine.evaluate_moat_strength({"network_effects": 0.9, "switching_costs": 0.8, "brand": 0.7})
    assert moat["aggregate_moat_score"] == 0.8
    assert moat["is_defensible"] is True

    pivot = engine.check_pivot_trigger(ltv_cac_ratio=0.8, burn_months_left=2.0)
    assert pivot is True


def test_layer_12_org_design():
    engine = OrganizationalDesignEngine()
    hire = engine.evaluate_hiring_trigger(workload_utilization=0.9, expected_marginal_roi=400000.0, fully_loaded_cost=100000.0)
    assert hire["should_hire"] is True


def test_layer_13_meta_learning():
    engine = MetaLearningEngine()
    posterior = engine.update_hypothesis_prior(prior_prob=0.5, likelihood=0.8, marginal_evidence=0.5)
    assert posterior == 0.8

    dq = engine.evaluate_decision_quality(ex_ante_voi=50.0, risk_adjusted_ev=30.0, actual_outcome=100.0)
    assert dq["process_quality_score"] == 0.8


def test_layer_14_ai_entrepreneurship():
    engine = AIEntrepreneurshipEngine()
    opp1 = CandidateOpportunity(title="Opp A", tam_usd=1e7, p_success=0.5, gross_margin=0.8, cac_usd=100.0, ltv_usd=1000.0, downside_risk_usd=5000.0)
    opp2 = CandidateOpportunity(title="Opp B", tam_usd=1e8, p_success=0.7, gross_margin=0.9, cac_usd=200.0, ltv_usd=3000.0, downside_risk_usd=10000.0)

    res = engine.allocate_resources(1000000.0, 1e15, [opp1, opp2])
    assert "Opp A" in res["allocations"]
    assert "Opp B" in res["allocations"]


def test_fourteen_layer_master_orchestrator():
    orchestrator = FourteenLayerEntrepreneurialEngine()

    sig = SignalObservation(domain="SaaS", title="Autonomous Customer Care", kl_surprise=0.9, tam_estimate_usd=50000000.0)
    opp = CandidateOpportunity(title="Autonomous Support AI", tam_usd=5e7, p_success=0.7, gross_margin=0.85, cac_usd=300.0, ltv_usd=2500.0, downside_risk_usd=15000.0)
    feat = FeatureProposal(feature_name="Instant Ticket Solver", jtbd_impact_score=9.5, complexity_cost=1.5)

    res = orchestrator.run_full_14_layer_pipeline(sig, opp, feat, capital_usd=500000.0)

    assert res["status"] == "completed"
    assert res["layer_1_reality"]["is_viable"] is True
    assert res["layer_2_opportunity_discovery_passed"] is True
    assert res["layer_6_product_filter"]["action"] == "APPROVED"
    assert res["layer_9_sales_funnel"]["next_stage"] == "qualified"
    assert res["layer_13_belief_posterior"] > 0
    assert "allocations" in res["layer_14_ai_allocations"]
