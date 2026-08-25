from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    EntrepreneurialIntelligenceOrchestrator,
    FourteenLayerEngine,
    ComputationalArchitectureOfEntrepreneurship,
    Layer1_Reality,
    Layer14_AIEntrepreneurship,
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
    assert "fourteen_layer_pipeline_results" in pipeline_result


def test_fourteen_layer_reexports() -> None:
    l1 = Layer1_Reality()
    assert l1.analyze_fundamental_reality()["definition"] is not None
    l14 = Layer14_AIEntrepreneurship()
    assert l14.allocate_resources_kelly(100, 0.5, 2.0)["allocated_capital_cents"] >= 0

    orchestrator = ComputationalArchitectureOfEntrepreneurship()
    assert isinstance(orchestrator, FourteenLayerEngine)
