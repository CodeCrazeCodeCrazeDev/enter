from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    EntrepreneurialIntelligenceOrchestrator,
    Layer1_RealityEngine,
    Layer2_OpportunityDiscoveryEngine,
    Layer3_ProblemDiscoveryEngine,
    Layer4_DecisionMakingEngine,
    Layer5_OpportunityEvaluationEngine,
    Layer6_ProductCreationEngine,
    Layer7_CustomerUnderstandingEngine,
    Layer8_MarketingEngine,
    Layer9_SalesEngine,
    Layer10_GrowthEngine,
    Layer11_CompetitionEngine,
    Layer12_OrganizationalDesignEngine,
    Layer13_MetaLearningEngine,
    Layer14_AIEntrepreneurshipEngine,
    ComputationalArchitectureOfEntrepreneurship,
)


def test_active_inference_planner_ranking() -> None:
    planner = ActiveInferencePlanner(curiosity_weight=2.0)

    # Opportunity 1: High curiosity path (high expected entropy reduction from 2.0 to 0.4 = 1.6)
    opp_1 = Opportunity(
        title="high_exploratory_opportunity",
        domain="tech_frontier",
        prior_entropy=2.0,
        post_entropy_simulated=0.4,
        success_probability=0.4,
        target_preference=0.9
    )

    # Opportunity 2: Conservative replica (low entropy reduction from 0.6 to 0.5 = 0.1)
    opp_2 = Opportunity(
        title="conservative_replication",
        domain="traditional_retail",
        prior_entropy=0.6,
        post_entropy_simulated=0.5,
        success_probability=0.85,
        target_preference=0.9
    )

    ranked = planner.rank_opportunities([opp_1, opp_2])

    # Under curiosity_weight = 2.0, opp_1 should yield a more negative Expected Free Energy (superior)
    assert ranked[0][0].title == "high_exploratory_opportunity"
    assert ranked[0][1] < ranked[1][1]


def test_advanced_causal_engine_do_and_counterfactual() -> None:
    engine = AdvancedCausalEngine()

    # Build causal path: marketing_spend -> click_through_rate -> sales_revenue
    engine.add_causal_relationship("marketing_spend", "click_through_rate", 0.6)
    engine.add_causal_relationship("click_through_rate", "sales_revenue", 1.8)

    # 1. Verify do-calculus intervention (do(marketing_spend = 2.0))
    state = engine.execute_do_intervention("marketing_spend", 2.0)
    assert state["marketing_spend"] == 2.0
    # click_through_rate = 2.0 * 0.6 = 1.2
    assert pytest.approx(state["click_through_rate"]) == 1.2
    # sales_revenue = 1.2 * 1.8 = 2.16
    assert pytest.approx(state["sales_revenue"]) == 2.16

    # 2. Verify Counterfactual estimation (Abduction -> Action -> Prediction)
    # Factual: marketing_spend = 1.0, click_through_rate = 0.8 (noise = 0.2), sales_revenue = 1.44
    factual_observations = {
        "marketing_spend": 1.0,
        "click_through_rate": 0.8,
        "sales_revenue": 1.44
    }
    # "What would sales_revenue be if marketing_spend was 2.0?"
    counterfactual_revenue = engine.estimate_counterfactual(
        factual_observations=factual_observations,
        counterfactual_intervention=("marketing_spend", 2.0),
        target_outcome_var="sales_revenue"
    )
    # Under marketing_spend = 2.0:
    # click_through_rate = 2.0 * 0.6 + noise = 1.2 + 0.2 = 1.4
    # sales_revenue = 1.4 * 1.8 + noise = 2.52 + 0.0 = 2.52
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


def test_layer1_to_14_individual_engines() -> None:
    # Layer 1
    l1 = Layer1_RealityEngine()
    l1_res = l1.evaluate_reality_principles({"unit_econ_positive": True})
    assert l1_res["invariants_satisfied"] is True
    assert "definition" in l1_res

    # Layer 2
    l2 = Layer2_OpportunityDiscoveryEngine()
    l2_res = l2.search_state_space([
        {"magnitude": 0.1, "signal_to_noise": 1.5, "novelty": 0.8},
        {"magnitude": 0.2, "signal_to_noise": 2.0, "novelty": 0.9}
    ])
    assert l2_res["weak_signals_detected"] == 2

    # Layer 3
    l3 = Layer3_ProblemDiscoveryEngine()
    l3_res = l3.decompose_and_analyze_problem({"stated_problem": "low_conversion", "causal_parents": ["high_checkout_latency"]})
    assert l3_res["real_problem"] == "high_checkout_latency"

    # Layer 4
    l4 = Layer4_DecisionMakingEngine()
    l4_res = l4.make_decision_under_uncertainty(0.8, 0.9, 0.5, 50.0)
    assert l4_res["kill_recommendation"] is False

    # Layer 5
    l5 = Layer5_OpportunityEvaluationEngine()
    l5_res = l5.evaluate_opportunity_quality(1000000_00, 0.6, 100000_00, 0.8)
    assert l5_res["expected_value_cents"] == 600000_00

    # Layer 6
    l6 = Layer6_ProductCreationEngine()
    l6_res = l6.design_product_and_learning_loop(["f1", "f2", "f3", "f4", "f5", "f6"], complexity_budget=3)
    assert len(l6_res["built_features"]) == 3
    assert len(l6_res["rejected_features"]) == 3

    # Layer 7
    l7 = Layer7_CustomerUnderstandingEngine()
    l7_res = l7.model_customer_psychology(0.9, 0.2, 0.8)
    assert l7_res["customer_will_switch"] is True

    # Layer 8
    l8 = Layer8_MarketingEngine()
    l8_res = l8.model_market_and_growth(1.5, 0.8, [1.0, 0.5])
    assert l8_res["is_viral_epidemic"] is True

    # Layer 9
    l9 = Layer9_SalesEngine()
    l9_res = l9.run_sales_system(100000_00, 0.9, ["security"])
    assert l9_res["sales_motion"] == "enterprise_human"

    # Layer 10
    l10 = Layer10_GrowthEngine()
    l10_res = l10.evaluate_growth_dynamics(20000, 4000_00, 1000_00, 0.1)
    assert l10_res["is_platform_transition_ready"] is True

    # Layer 11
    l11 = Layer11_CompetitionEngine()
    l11_res = l11.evaluate_competitive_landscape(10000_00, 0.8, 0.5, 0.2)
    assert l11_res["moat_durability_score"] > 0.5

    # Layer 12
    l12 = Layer12_OrganizationalDesignEngine()
    l12_res = l12.design_organization_and_delegation(0.9, "seed", 0.5)
    assert l12_res["should_hire"] is True
    assert l12_res["delegation_recommendation"] == "delegate"

    # Layer 13
    l13 = Layer13_MetaLearningEngine()
    l13_res = l13.execute_meta_learning(0.7, [True, True], [0.9, 0.8])
    assert l13_res["brier_score"] < 0.1

    # Layer 14
    l14 = Layer14_AIEntrepreneurshipEngine()
    l14_res = l14.synthesize_ai_entrepreneurship(100000_00, 500.0, 3, [])
    assert "task_taxonomy" in l14_res


def test_computational_architecture_master_orchestration() -> None:
    master = ComputationalArchitectureOfEntrepreneurship()

    signal_data = {
        "title": "Quantum AI Hardware Platform",
        "domain": "quantum_ai",
        "variables": ["rd_spend", "performance", "market_adoption"],
        "causal_edges": [("rd_spend", "performance"), ("performance", "market_adoption")],
        "coefficients": {"rd_spend->performance": 1.8, "performance->market_adoption": 2.2},
        "hypothesis_confidence": 0.7,
        "evidence_strength": 0.8,
        "entropy": 1.1,
        "tam_cents": 500000000_00,
        "success_probability": 0.65,
        "downside_cents": 20000000_00,
        "timing_readiness": 0.85,
        "viral_k": 1.3,
        "deal_size_cents": 50000_00,
        "signals": [
            {"magnitude": 0.2, "signal_to_noise": 1.8, "novelty": 0.95},
            {"magnitude": 0.3, "signal_to_noise": 2.5, "novelty": 0.90}
        ],
        "problem": {
            "stated_problem": "slow_compute",
            "causal_parents": ["memory_bottleneck", "bus_bandwidth"]
        }
    }

    res = master.run_complete_14_layer_pipeline(signal_data)

    assert res["status"] == "success"
    assert res["pipeline_executed_layers"] == 14
    assert res["layer1_reality"]["invariants_satisfied"] is True
    assert res["layer2_opportunity_discovery"]["weak_signals_detected"] == 2
    assert res["layer3_problem_discovery"]["real_problem"] == "memory_bottleneck"
    assert res["layer14_ai_entrepreneurship"]["top_opportunity_title"] == "Quantum AI Hardware Platform"
