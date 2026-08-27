"""
Comprehensive Unit Tests for the 14-Layer Computational Architecture of Entrepreneurship.
"""

from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    Opportunity,
    ProblemStatement,
    RealityEngine,
    OpportunityDiscoveryEngine,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitiveMoatEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    EntrepreneurialIntelligenceOrchestrator,
    FourteenLayerEngine,
    ComputationalArchitectureOfEntrepreneurship,
)


def test_layer1_reality_engine() -> None:
    engine = RealityEngine(loss_aversion_lambda=2.25)
    # Gain of $100 vs Loss of $100 with 50% probability
    utility = engine.evaluate_prospect_utility(gain=100.0, loss=-100.0, p_gain=0.5)
    # Subjective loss should outweigh gain under prospect theory
    assert utility < 0.0

    auto_task = engine.classify_automation_boundary("Linear Search Optimization", 0.2, 0.3)
    assert auto_task["is_automatable"] is True
    human_task = engine.classify_automation_boundary("Strategic Company Vision", 0.9, 0.95)
    assert human_task["is_automatable"] is False


def test_layer2_opportunity_discovery_engine() -> None:
    discovery = OpportunityDiscoveryEngine()
    signals = [
        {"title": "Noise Signal", "amplitude": 0.1, "confidence": 0.5},
        {"title": "Weak Trend Signal", "amplitude": 0.8, "confidence": 0.6},
    ]
    detected = discovery.detect_weak_signals(signals, signal_threshold=0.3)
    assert len(detected) == 1
    assert detected[0]["title"] == "Weak Trend Signal"

    novelty_pairs = discovery.generate_combinatorial_novelty(["AI", "Bio"], ["Robotics", "Finance"])
    assert len(novelty_pairs) == 4
    assert ("AI", "Robotics") in novelty_pairs


def test_layer3_causal_problem_discovery() -> None:
    causal = AdvancedCausalEngine()
    causal.add_causal_relationship("root_market_demand", "customer_signups", 2.0)
    causal.add_causal_relationship("customer_signups", "monthly_recurring_revenue", 50.0)

    roots = causal.identify_root_causes("monthly_recurring_revenue")
    assert roots == ["root_market_demand"]

    state = causal.execute_do_intervention("root_market_demand", 10.0)
    assert state["customer_signups"] == 20.0
    assert state["monthly_recurring_revenue"] == 1000.0


def test_layer4_active_inference_decision_making() -> None:
    planner = ActiveInferencePlanner(curiosity_weight=1.5)
    opp = Opportunity(
        title="High Epistemic Gain Venture",
        domain="quantum_computing",
        prior_entropy=2.0,
        post_entropy_simulated=0.5,
        success_probability=0.5,
        target_preference=0.9
    )
    efe = planner.calculate_efe(opp)
    assert efe < 0.0  # Favorable Expected Free Energy

    counter_hypo = planner.generate_counter_hypothesis("Market demand will double")
    assert "Falsification Hypothesis" in counter_hypo


def test_layer5_opportunity_evaluation() -> None:
    eval_engine = OpportunityEvaluationEngine()
    opp1 = Opportunity(
        title="Base Venture",
        domain="saas",
        tam_cents=100000000,
        success_probability=0.6,
        timing_score=0.8,
        downside_risk=0.2
    )
    score1 = eval_engine.evaluate_pareto_score(opp1)
    assert score1["expected_value_dollars"] == 600000.0

    opp2 = Opportunity(
        title="Superior Venture",
        domain="saas",
        tam_cents=300000000,
        success_probability=0.8,
        timing_score=0.9,
        downside_risk=0.1
    )
    assert eval_engine.should_switch_opportunity(opp1, opp2) is True


def test_layer6_product_creation() -> None:
    product_engine = ProductCreationEngine()
    eval_res = product_engine.calculate_jtbd_value_to_complexity(
        core_jtbd="Automate Financial Auditing",
        feature_set=["pdf_parser", "ocr", "reconciliation_engine"],
        perceived_value=0.9,
        complexity_weights={"pdf_parser": 0.1, "ocr": 0.2, "reconciliation_engine": 0.2}
    )
    assert eval_res["total_complexity"] == 0.5
    assert eval_res["value_density"] == 1.8
    assert eval_res["recommendation"] == "Lean Build"


def test_layer7_customer_understanding() -> None:
    cust_engine = CustomerUnderstandingEngine()
    res = cust_engine.simulate_customer_lifecycle(
        initial_trust=0.7,
        perceived_value_delivered=0.9,
        switching_barrier=0.4,
        friction_events=0
    )
    assert res["is_evangelist"] is True
    assert res["customer_state"] == "Evangelist"


def test_layer8_marketing_and_virality() -> None:
    mkt = MarketingEngine()
    k_factor = mkt.calculate_virality_coefficient(sharing_rate=0.8, conversion_per_invite=1.5)
    assert pytest.approx(k_factor) == 1.2
    spread = mkt.simulate_attention_spread(initial_seeds=100, k_factor=1.2, rounds=3)
    assert spread == [100, 120, 144, 172]


def test_layer9_sales_systems() -> None:
    sales = SalesEngine()
    small_deal = sales.evaluate_sales_routing(deal_size_dollars=5000, sales_cycle_complexity=0.2)
    assert small_deal["route"] == "Automated Self-Serve Funnel"

    large_deal = sales.evaluate_sales_routing(deal_size_dollars=50000, sales_cycle_complexity=0.8)
    assert large_deal["route"] == "Enterprise High-Touch Sales"


def test_layer10_growth_and_ecosystems() -> None:
    growth = GrowthEngine()
    m_val = growth.calculate_metcalfe_value(active_nodes=100, value_per_connection=0.01)
    # Connections = 100 * 99 / 2 = 4950 -> value = 49.5
    assert pytest.approx(m_val) == 49.5
    assert growth.evaluate_platform_transition(user_count=15000, developer_count=60) is True


def test_layer11_competitive_moats() -> None:
    moat = CompetitiveMoatEngine()
    score = moat.score_moat_durability(switching_costs=0.8, network_effects=0.8, scale_advantages=0.7, brand_equity=0.7)
    assert score["is_defensible"] is True
    assert moat.evaluate_pivot_trigger(quarterly_growth=-0.05, moat_decay_rate=0.20) is True


def test_layer12_organizational_design() -> None:
    org = OrganizationalDesignEngine()
    budget = org.optimize_capital_allocation(1000000.0)
    assert budget["rd_budget"] == 400000.0
    assert budget["gtm_budget"] == 400000.0

    type2_decision = org.determine_delegation_level(decision_reversibility=0.8, decision_impact_dollars=10000)
    assert "Type 2" in type2_decision


def test_layer13_meta_learning() -> None:
    meta = MetaLearningEngine()
    post_belief = meta.update_mental_model(prior_belief=0.5, outcome_observation=1.0, learning_rate=0.2)
    assert pytest.approx(post_belief) == 0.6

    rule = meta.Synthesize_failure_lesson("Churn Spike", "Unclear Onboarding")
    assert "WHEN encountering 'Churn Spike'" in rule["rule_statement"]


def test_layer14_full_14_layer_master_orchestrator() -> None:
    orchestrator = FourteenLayerEngine()
    signal = {
        "title": "Autonomous AI Entrepreneurship Engine",
        "domain": "autonomous_software",
        "variables": ["rd_investment", "product_quality", "user_adoption"],
        "causal_edges": [("rd_investment", "product_quality"), ("product_quality", "user_adoption")],
        "coefficients": {
            "rd_investment->product_quality": 0.8,
            "product_quality->user_adoption": 2.5
        },
        "prior_entropy": 1.8,
        "post_entropy_simulated": 0.4,
        "success_probability": 0.7,
        "tam_cents": 1000000000,
        "timing_score": 0.9,
        "downside_risk": 0.15
    }

    orchestrator.ingest_signal(signal)
    res = orchestrator.execute_orchestrated_pipeline()

    assert res["status"] == "executed"
    assert res["selected_opportunity"] == "Autonomous AI Entrepreneurship Engine"
    assert "best_expected_free_energy" in res
    assert "pareto_evaluation" in res
    assert "product_evaluation" in res
    assert "customer_evaluation" in res
    assert "virality_k_factor" in res
    assert "sales_routing" in res
    assert "growth_metcalfe_value" in res
    assert "moat_durability" in res
    assert "capital_allocation" in res
    assert "meta_learning_rule" in res
