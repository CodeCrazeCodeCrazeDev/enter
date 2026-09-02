"""
Unit and Integration test suite for the 14-Layer Computational Architecture of Entrepreneurship.
"""

from __future__ import annotations
import pytest
from apodex.ai_eos.intelligence import (
    FourteenLayerEntrepreneurialEngine,
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
    RealitySignal,
    DiscoveredOpportunity,
    ProblemDefinition
)


def test_layer1_reality_decomposition() -> None:
    layer1 = Layer1_Reality()
    res = layer1.decompose_nature()
    assert "definition" in res
    assert len(res["invariants"]) >= 4
    assert "Value creation strictly precedes sustainable value capture." in res["invariants"]
    assert "non_automatable" in res
    assert "automatable" in res


def test_layer2_opportunity_discovery() -> None:
    layer2 = Layer2_OpportunityDiscovery()
    signals = [
        RealitySignal(source="arxiv", description="Breakthrough in local SLM inference speed", domain="AI"),
        RealitySignal(source="regulatory_feed", description="New EU data privacy framework", domain="LegalTech")
    ]
    opp = layer2.search_state_space(signals)
    assert isinstance(opp, DiscoveredOpportunity)
    assert opp.novelty_score >= 0.7
    assert len(opp.weak_signals) == 2


def test_layer3_problem_discovery() -> None:
    layer3 = Layer3_ProblemDiscovery()
    prob = layer3.decompose_problem("High customer drop-off on onboarding")
    assert isinstance(prob, ProblemDefinition)
    assert prob.is_first_order is True
    assert "Root cause" in prob.root_cause_problem
    assert len(prob.symptoms) == 2


def test_layer4_decision_making_active_inference() -> None:
    layer4 = Layer4_DecisionMaking(curiosity_weight=1.5)
    opp = DiscoveredOpportunity(
        title="High value opportunity",
        domain="AI",
        prior_entropy=2.0,
        post_entropy_simulated=0.5,
        success_probability=0.7,
        target_preference=0.9
    )
    decision = layer4.make_decision(opp, data_confidence=0.9, intuition_prior=0.8)
    assert decision.expected_free_energy < 0.5
    assert decision.status == "EXECUTING"


def test_layer5_evaluation_and_layer6_product() -> None:
    layer5 = Layer5_OpportunityEvaluation()
    opp = DiscoveredOpportunity(title="SaaS", domain="SaaS", success_probability=0.8, tam_cents=100_000_000)
    eval_res = layer5.evaluate(opp, dev_cost_cents=10_000_000)
    assert eval_res.expected_value_cents == 70_000_000
    assert eval_res.recommendation == "PROCEED"

    layer6 = Layer6_ProductCreation()
    prob = ProblemDefinition(stated_problem="Manual data entry", root_cause_problem="Incentive misalignment")
    product = layer6.design_product(prob, ["Auto Parser", "Realtime Dashboard", "Theme Selector"])
    assert len(product.core_features) == 2
    assert "Theme Selector" in product.pruned_features


def test_layer7_through_layer13() -> None:
    layer7 = Layer7_CustomerUnderstanding()
    cust = layer7.model_customer("DevOps")
    assert cust.churn_risk == 0.05

    layer8 = Layer8_Marketing()
    layer6 = Layer6_ProductCreation()
    prob = ProblemDefinition(stated_problem="P", root_cause_problem="R")
    prod = layer6.design_product(prob, [])
    mkt = layer8.Formulate_strategy(prod)
    assert mkt.virality_k_factor > 1.0

    layer9 = Layer9_Sales()
    sales = layer9.design_sales_system(acv_cents=60_000_00)
    assert sales.automation_mode == "ENTERPRISE_HYBRID"

    layer10 = Layer10_Growth()
    growth = layer10.evaluate_growth(mkt, churn_rate=cust.churn_risk)
    assert growth.strategic_slowdown_required is False

    layer11 = Layer11_Competition()
    moat = layer11.analyze_moats(prod)
    assert len(moat.moat_types) >= 3

    layer12 = Layer12_OrganizationalDesign()
    org = layer12.optimize_topology(bottleneck_shadow_price=0.6)
    assert org.hire_trigger is True

    layer13 = Layer13_MetaLearning()
    meta = layer13.update_meta_knowledge([0.05, 0.05], ["Deployment delay"])
    assert meta.brier_forecast_accuracy == 0.95


def test_full_fourteen_layer_engine_orchestration() -> None:
    engine = FourteenLayerEntrepreneurialEngine(curiosity_weight=1.2)

    signals = [
        RealitySignal(source="market_pulse", description="High latency in enterprise LLM tool use", domain="AI Infrastructure"),
        RealitySignal(source="dev_survey", description="Developers demand local autonomous verifiers", domain="Software Engineering")
    ]

    results = engine.run_full_entrepreneurial_cycle(
        signals=signals,
        raw_problem_statement="Enterprise AI agent workflows stall during verification failures",
        candidate_features=["Local Sandbox Isolation", "SCM Active Inference Verification Engine", "Custom UI"],
        acv_cents=75_000_00,
        available_capital_cents=1000_000_00,
        available_flops=1e19
    )

    assert "reality_summary" in results
    assert "opportunity" in results
    assert "problem" in results
    assert "decision" in results
    assert "evaluation" in results
    assert "product" in results
    assert "customer" in results
    assert "marketing" in results
    assert "sales" in results
    assert "growth" in results
    assert "moat" in results
    assert "org" in results
    assert "meta_learning" in results
    assert "ai_execution" in results

    assert results["ai_execution"].recommended_action == "FULL_SCALE_AUTONOMOUS_LAUNCH"
    assert results["sales"].automation_mode == "ENTERPRISE_HYBRID"
