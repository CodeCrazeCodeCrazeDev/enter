from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    Signal,
    InvariantsModel,
    OpportunityDiscoveryEngine,
    ProblemDiscoveryEngine,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerPsychologyModel,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitionEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    AIEntrepreneurshipEngine,
    EntrepreneurialIntelligenceOrchestrator
)


def test_layer1_reality_invariants() -> None:
    inv = InvariantsModel()
    res1 = inv.decompose_task_nature("opportunity_evaluation_and_search")
    assert res1["automatable"] is True
    assert res1["requires_human_judgment"] is False

    res2 = inv.decompose_task_nature("trust_foundational_ethics_governance")
    assert res2["automatable"] is False
    assert res2["requires_human_judgment"] is True

    val = inv.compute_value_creation_bounds(pain_severity=0.8, market_size_cents=100000000)
    assert val > 0.0


def test_layer2_opportunity_discovery() -> None:
    disc = OpportunityDiscoveryEngine()
    s1 = Signal(source="tech_rss", content="LLM Agent framework surge", keywords=["agent", "llm"], snr=0.8)
    s2 = Signal(source="noise_feed", content="Random rumor", keywords=["rumor"], snr=0.2)
    s3 = Signal(source="biotech_journal", content="Lab automation hardware", keywords=["lab", "robotics"], snr=0.7)

    filtered = disc.detect_and_filter_signals([s1, s2, s3], min_snr=0.5)
    assert len(filtered) == 2
    assert s2 not in filtered

    syn_opp = disc.synthesize_combinatorial_novelty(s1, s3)
    assert "Synthesized:" in syn_opp.title
    assert "agent" in syn_opp.keywords
    assert "robotics" in syn_opp.keywords


def test_layer3_problem_and_causal_engine() -> None:
    p_disc = ProblemDiscoveryEngine()
    decomp = p_disc.decompose_problem_tree("High Customer Churn", ["poor_onboarding", "slow_support", "buggy_ui"])
    assert decomp["root_problem"] == "High Customer Churn"
    assert len(decomp["first_order_sub_problems"]) == 2

    engine = AdvancedCausalEngine()
    engine.add_causal_relationship("marketing_spend", "click_through_rate", 0.6)
    engine.add_causal_relationship("click_through_rate", "sales_revenue", 1.8)

    state = engine.execute_do_intervention("marketing_spend", 2.0)
    assert state["marketing_spend"] == 2.0
    assert pytest.approx(state["sales_revenue"]) == 2.16

    cf_revenue = engine.estimate_counterfactual(
        factual_observations={"marketing_spend": 1.0, "click_through_rate": 0.8, "sales_revenue": 1.44},
        counterfactual_intervention=("marketing_spend", 2.0),
        target_outcome_var="sales_revenue"
    )
    assert pytest.approx(cf_revenue) == 2.52

    disentangle = engine.disentangle_symptom_vs_root_cause("sales_revenue")
    assert disentangle["is_root_cause"] is False


def test_layer4_active_inference_falsification() -> None:
    planner = ActiveInferencePlanner(curiosity_weight=2.0)
    opp_1 = Opportunity(
        title="high_exploratory_opportunity",
        domain="tech_frontier",
        prior_entropy=2.0,
        post_entropy_simulated=0.4,
        success_probability=0.4,
        target_preference=0.9
    )
    opp_2 = Opportunity(
        title="conservative_replication",
        domain="traditional_retail",
        prior_entropy=0.6,
        post_entropy_simulated=0.5,
        success_probability=0.85,
        target_preference=0.9
    )

    ranked = planner.rank_opportunities([opp_1, opp_2])
    assert ranked[0][0].title == "high_exploratory_opportunity"

    assert planner.evaluate_fast_falsification(opp_1, critical_evidence_pass=True) is True
    assert planner.evaluate_fast_falsification(opp_1, critical_evidence_pass=False) is False
    assert opp_1.is_active is False


def test_layer5_opportunity_evaluation() -> None:
    eval_eng = OpportunityEvaluationEngine()
    opp = Opportunity(title="SaaS App", success_probability=0.6, tam_cents=100000000, estimated_margin=0.8)
    ev = eval_eng.calculate_expected_value_cents(opp)
    assert ev == 48000000.0

    risk = eval_eng.estimate_downside_risk_cents(experiment_cost_cents=500000, failure_probability=0.4)
    assert risk == 200000.0

    cand_opp = Opportunity(title="Better SaaS App", success_probability=0.9, tam_cents=200000000, estimated_margin=0.8)
    should_switch = eval_eng.evaluate_switching_threshold(opp, cand_opp, switching_cost_cents=5000000)
    assert should_switch is True


def test_layer6_product_creation() -> None:
    prod = ProductCreationEngine()
    retained = prod.minimize_complexity_pareto({
        "core_editor": 80.0,
        "export_pdf": 15.0,
        "dark_mode_theme": 3.0,
        "custom_fonts": 2.0
    })
    assert "core_editor" in retained
    assert len(retained) <= 2

    vel = prod.calculate_learning_velocity(experiments_completed=10, total_days=5.0)
    assert vel == 2.0


def test_layer7_customer_psychology() -> None:
    cust = CustomerPsychologyModel()
    p_switch = cust.compute_switching_probability(value_delta=3.0, switching_friction=1.0)
    assert p_switch > 0.8

    trust = cust.calculate_trust_index(delivered_promises=9, total_promises=10, resolution_speed_days=1.0)
    assert trust == 0.9


def test_layer8_marketing() -> None:
    mkt = MarketingEngine()
    k_factor = mkt.compute_viral_coefficient(invites_per_user=5.0, conversion_rate=0.25)
    assert k_factor == 1.25

    synergy_roi = mkt.evaluate_channel_synergy(channel_a_roi=2.0, channel_b_roi=3.0, cross_overlap=0.5)
    assert synergy_roi > 5.0


def test_layer9_sales() -> None:
    sales = SalesEngine()
    route = sales.determine_sales_route(deal_size_cents=5000000, sales_cycle_days=45)
    assert route == "enterprise_high_touch"

    res = sales.resolve_objection("price")
    assert res["recommended_strategy"] == "frame_roi_and_payback_period"


def test_layer10_growth() -> None:
    growth = GrowthEngine()
    m_val = growth.compute_metcalfe_value(100)
    assert m_val == 10000.0

    r_val = growth.compute_reed_group_value(10)
    assert r_val == 1024.0

    slow_down = growth.check_growth_deceleration_need(system_churn_rate=0.20, infrastructure_load=0.50)
    assert slow_down is True


def test_layer11_competition() -> None:
    comp = CompetitionEngine()
    score = comp.compute_moat_durability_score(
        network_density=0.8,
        avg_switching_cost_cents=500000,
        brand_trust=0.9,
        cost_advantage=0.4
    )
    assert 0.0 <= score <= 1.0


def test_layer12_org_design() -> None:
    org = OrganizationalDesignEngine()
    hire = org.evaluate_hiring_trigger(capacity_utilization=0.90, decision_latency_hours=24.0)
    assert hire is True

    eff = org.compute_delegation_efficiency(central_workload=20.0, delegated_workload=80.0)
    assert eff == 0.8


def test_layer13_meta_learning() -> None:
    meta = MetaLearningEngine()
    brier = meta.audit_decision_brier_score(predicted_probability=0.8, actual_outcome=True)
    assert pytest.approx(brier) == 0.04

    updated_prior = meta.update_prior_confidence_bayes(prior_confidence=0.5, likelihood=0.8)
    assert updated_prior > 0.5


def test_layer14_ai_entrepreneurship() -> None:
    ai_eng = AIEntrepreneurshipEngine()
    opp_id_1 = uuid4()
    opp_id_2 = uuid4()

    allocs = ai_eng.allocate_multi_resource_budget(
        total_capital_cents=100000000,
        total_compute_flops=1e18,
        total_talent_hours=500.0,
        opportunity_priorities={opp_id_1: 3.0, opp_id_2: 1.0}
    )

    assert allocs[opp_id_1]["capital_cents"] == 75000000
    assert allocs[opp_id_2]["capital_cents"] == 25000000


def test_orchestrated_pipeline_execution() -> None:
    orchestrator = EntrepreneurialIntelligenceOrchestrator()

    signal = {
        "title": "Autonomous Scientific Hardware Venture",
        "domain": "robotics",
        "variables": ["marketing_spend", "click_through_rate", "sales_revenue"],
        "causal_edges": [("marketing_spend", "click_through_rate"), ("click_through_rate", "sales_revenue")],
        "coefficients": {
            "marketing_spend->click_through_rate": 0.5,
            "click_through_rate->sales_revenue": 2.0
        },
        "prior_entropy": 1.8,
        "post_entropy_simulated": 0.5,
        "success_probability": 0.6,
        "tam_cents": 500000000,
        "keywords": ["hardware", "ai", "robotics"]
    }

    orchestrator.ingest_signal(signal)
    pipeline_result = orchestrator.execute_orchestrated_pipeline()

    assert pipeline_result["status"] == "executed"
    assert pipeline_result["selected_opportunity"] == "Autonomous Scientific Hardware Venture"
    assert "layer1_reality_decomposition" in pipeline_result
    assert "layer4_best_expected_free_energy" in pipeline_result
    assert "layer3_causal_intervention" in pipeline_result
    assert "layer5_expected_value_cents" in pipeline_result
    assert "layer8_viral_k_factor" in pipeline_result
    assert "layer10_growth_metcalfe_value" in pipeline_result
    assert "layer14_multi_resource_allocation" in pipeline_result
