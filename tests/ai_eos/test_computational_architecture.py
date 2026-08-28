from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    EntrepreneurialIntelligenceOrchestrator,
    ComputationalArchitectureOfEntrepreneurship,
    Layer1_Reality,
    Layer2_OpportunityDiscovery,
    Layer3_ProblemDiscovery,
    Layer4_DecisionMaking,
    Layer5_OpportunityEvaluation,
    Layer6_ProductCreation,
    Layer7_CustomerUnderstanding,
    Layer8_Marketing,
    Layer9_Sales,
    Layer10_Growth,
    Layer11_Competition,
    Layer12_OrganizationalDesign,
    Layer13_MetaLearning,
    Layer14_AIEntrepreneurship,
)


def test_layer1_reality_task_deconstruction() -> None:
    l1 = Layer1_Reality()
    res_high = l1.deconstruct_task("Brand Identity & Vision Strategy", 0.9)
    assert not res_high["automatable"]
    assert res_high["recommended_executor"] == "human_in_the_loop_ai_hybrid"

    res_low = l1.deconstruct_task("Data ETL Pipeline", 0.2)
    assert res_low["automatable"]
    assert res_low["recommended_executor"] == "algorithmic_script"


def test_layer2_opportunity_discovery_and_synthesis() -> None:
    l2 = Layer2_OpportunityDiscovery()
    raw_signals = [
        {"title": "AI Drug Discovery", "strength": 0.8, "noise_ratio": 0.2, "domain": "bio"},
        {"title": "Noise Signal", "strength": 0.1, "noise_ratio": 0.9, "domain": "trash"},
    ]
    filtered = l2.detect_weak_signals(raw_signals)
    assert len(filtered) == 1
    assert filtered[0]["title"] == "AI Drug Discovery"

    sig_b = {"title": "Quantum Computing", "strength": 0.9, "noise_ratio": 0.1, "domain": "physics"}
    opp = l2.synthesize_novel_opportunity(filtered[0], sig_b)
    assert "Cross-Domain Solution" in opp.title
    assert "bio_physics" in opp.domain


def test_layer3_problem_decomposition() -> None:
    l3 = Layer3_ProblemDiscovery()
    decomp = l3.decompose_problem("Low Customer Retention", ["unclear_onboarding", "slow_response", "churn"])
    assert decomp["root_causes"] == ["unclear_onboarding"]
    assert "slow_response" in decomp["symptoms"]
    assert not decomp["should_ignore"]


def test_layer4_decision_making_confidence() -> None:
    l4 = Layer4_DecisionMaking()
    eval_res = l4.evaluate_decision_confidence(data_points=60, intuition_score=0.9)
    assert eval_res["mode"] == "data_driven"
    assert eval_res["data_weight"] == 0.85
    assert not eval_res["kill_idea_recommended"]


def test_layer5_opportunity_evaluation_and_switching() -> None:
    l5 = Layer5_OpportunityEvaluation()
    opp = Opportunity(
        title="B2B SaaS Security",
        domain="cyber",
        prior_entropy=1.2,
        success_probability=0.7,
        tam_cents=200000000
    )
    res = l5.evaluate_opportunity(opp)
    assert res["tam_dollars"] == 2000000.0
    assert res["expected_value"] == 1400000.0

    should_switch = l5.evaluate_switching_decision(current_opp_score=100.0, new_opp_score=200.0, switching_cost=20.0)
    assert should_switch


def test_layer6_product_creation_jtbd() -> None:
    l6 = Layer6_ProductCreation()
    decomp = l6.decompose_jtbd(
        user_statement="Manual Invoice Processing Friction",
        feature_candidates=[
            {"name": "One-Click OCR Extraction", "value_impact": 0.95, "complexity": 0.2},
            {"name": "Over-Engineered VR Interface", "value_impact": 0.1, "complexity": 0.9}
        ]
    )
    assert "One-Click OCR Extraction" in decomp["approved_features"]
    assert len(decomp["rejected_features"]) == 1


def test_layer7_customer_psychology() -> None:
    l7 = Layer7_CustomerUnderstanding()
    cust = l7.model_customer_psychology(perceived_value=0.9, trust_score=0.85, switching_barrier=0.1)
    assert cust["buy_decision"]
    assert cust["churn_risk"] < 0.4
    assert cust["evangelist_potential"] > 0.0


def test_layer8_marketing_virality() -> None:
    l8 = Layer8_Marketing()
    viral = l8.calculate_viral_coefficient(invites_per_user=3.0, conversion_rate=0.4)
    assert pytest.approx(viral["viral_coefficient_r0"]) == 1.2
    assert viral["is_exponential_growth"]


def test_layer9_sales_motion() -> None:
    l9 = Layer9_Sales()
    sales = l9.evaluate_sales_motion(acv_dollars=50000.0, deal_complexity=0.8)
    assert sales["recommended_motion"] == "enterprise_field_sales"
    assert sales["requires_human_rep"]


def test_layer10_growth_and_throttling() -> None:
    l10 = Layer10_Growth()
    net = l10.calculate_network_effect(active_nodes=2000)
    assert net["platform_transformation_ready"]

    throttle = l10.evaluate_growth_throttle(churn_rate=0.12, infrastructure_load=0.5)
    assert throttle["should_throttle_growth"]


def test_layer11_competition_moat() -> None:
    l11 = Layer11_Competition()
    moat = l11.evaluate_moat_durability(moat_types=["Proprietary Data", "Network Effect"], replication_time_months=36)
    assert moat["defensibility_class"] == "strong_moat"


def test_layer12_org_delegation() -> None:
    l12 = Layer12_OrganizationalDesign()
    org = l12.evaluate_hiring_and_delegation(workload_capacity_ratio=0.9, task_criticality=0.2)
    assert org["should_hire"]
    assert org["delegation_strategy"] == "fully_autonomous_ai_delegation"


def test_layer13_meta_learning() -> None:
    l13 = Layer13_MetaLearning()
    q = l13.record_decision_postmortem("dec_alpha", predicted_outcome=0.8, actual_outcome=0.85)
    assert pytest.approx(q) == 0.95
    knowledge = l13.synthesize_failure_into_knowledge("Overestimated TAM in Market X")
    assert knowledge["status"] == "knowledge_incorporated"


def test_layer14_ai_resource_allocation() -> None:
    l14 = Layer14_AIEntrepreneurship()
    opp1 = Opportunity(title="Opp 1", domain="tech")
    opp2 = Opportunity(title="Opp 2", domain="bio")
    alloc = l14.allocate_resources(capital_available_dollars=100000.0, compute_budget_gpu_hours=500.0, opportunities=[opp1, opp2])
    assert alloc["portfolio_size"] == 2
    assert alloc["allocation"]["Opp 1"]["allocated_capital_dollars"] == 50000.0


def test_master_architecture_full_14_layer_pipeline() -> None:
    arch = ComputationalArchitectureOfEntrepreneurship()
    signals = [
        {"title": "Autonomous AI Agent Infra", "strength": 0.8, "noise_ratio": 0.2, "domain": "ai"},
        {"title": "Decentralized Energy Grid", "strength": 0.75, "noise_ratio": 0.25, "domain": "energy"}
    ]
    res = arch.run_full_14_layer_pipeline(raw_signals=signals)
    assert res["status"] == "completed_14_layers"
    assert "Cross-Domain Solution" in res["opportunity_title"]
    assert res["layer2_weak_signals_found"] == 2
    assert res["layer8_marketing_virality"]["is_exponential_growth"]
    assert res["layer14_resource_allocation"]["status"] == "optimally_allocated"


def test_active_inference_planner_ranking() -> None:
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
    assert ranked[0][1] < ranked[1][1]


def test_advanced_causal_engine_do_and_counterfactual() -> None:
    engine = AdvancedCausalEngine()
    engine.add_causal_relationship("marketing_spend", "click_through_rate", 0.6)
    engine.add_causal_relationship("click_through_rate", "sales_revenue", 1.8)

    state = engine.execute_do_intervention("marketing_spend", 2.0)
    assert state["marketing_spend"] == 2.0
    assert pytest.approx(state["click_through_rate"]) == 1.2
    assert pytest.approx(state["sales_revenue"]) == 2.16

    factual_observations = {
        "marketing_spend": 1.0,
        "click_through_rate": 0.8,
        "sales_revenue": 1.44
    }
    counterfactual_revenue = engine.estimate_counterfactual(
        factual_observations=factual_observations,
        counterfactual_intervention=("marketing_spend", 2.0),
        target_outcome_var="sales_revenue"
    )
    assert pytest.approx(counterfactual_revenue) == 2.52


def test_orchestrated_pipeline_execution() -> None:
    engine = AdvancedCausalEngine()
    planner = ActiveInferencePlanner(curiosity_weight=1.5)
    orchestrator = EntrepreneurialIntelligenceOrchestrator(engine, planner)

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
        "tam_cents": 500000000
    }

    orchestrator.ingest_signal(signal)
    pipeline_result = orchestrator.execute_orchestrated_pipeline()

    assert pipeline_result["status"] == "executed"
    assert pipeline_result["selected_opportunity"] == "Autonomous Scientific Hardware Venture"
    assert "best_expected_free_energy" in pipeline_result
    assert pipeline_result["propagated_state"]["marketing_spend"] == 1.5
    assert pipeline_result["14_layer_pipeline"]["status"] == "completed_14_layers"
