from __future__ import annotations
import pytest

from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    EntrepreneurialRealityModel,
    Layer2OpportunityEngine,
    OpportunitySignal,
    Layer3ProblemEngine,
    Layer4DecisionEngine,
    Layer5EvaluationEngine,
    Layer6ProductEngine,
    Layer7CustomerEngine,
    Layer8MarketingEngine,
    Layer9SalesEngine,
    Layer10GrowthEngine,
    Layer11CompetitionEngine,
    Layer12OrgDesignEngine,
    Layer13MetaLearningEngine,
    Layer14AIEntrepreneurshipOrchestrator
)


def test_layer_1_to_4_reality_discovery_decision() -> None:
    # Layer 1 Reality Bounds
    reality = EntrepreneurialRealityModel()
    bound_psych = reality.evaluate_automation_bounds("Build customer trust and founder vision", "leadership")
    assert bound_psych.category == "human_psychology"
    assert not bound_psych.is_automatable

    bound_opt = reality.evaluate_automation_bounds("Ad bidding and pricing optimization", "marketing")
    assert bound_opt.category == "optimization_problem"
    assert bound_opt.is_automatable

    # Layer 2 Opportunity Search & Recombination
    opp_engine = Layer2OpportunityEngine()
    sig1 = OpportunitySignal(source="web_scan", domain="ai_agents", raw_intensity=0.8, novelty_score=0.7)
    sig2 = OpportunitySignal(source="patent_db", domain="biotech", raw_intensity=0.6, novelty_score=0.9)
    combined = opp_engine.recombine_unrelated_signals(sig1, sig2)
    assert combined.domain == "ai_agents×biotech"
    assert combined.novelty_score > 0.7

    # Layer 3 Problem SC Decomposition:
    # graph mapping parent -> children (drivers -> symptoms). Root drivers have empty children or are not in children set.
    prob_engine = Layer3ProblemEngine()
    graph = {"high_latency": ["churn"], "bad_ui": ["churn"], "churn": []}
    impacts = {"high_latency": 0.7, "bad_ui": 0.2}
    prob_res = prob_engine.decompose_problem("churn", graph, impacts)
    assert set(prob_res["root_causes"]) == {"high_latency", "bad_ui"}
    assert not prob_res["is_ignoreable_symptom"]

    # Layer 4 Active Inference & Falsification
    dec_engine = Layer4DecisionEngine()
    hypotheses = [
        {"name": "hyp_1", "posterior_confidence": 0.8, "pragmatic_value": 0.9, "epistemic_gain": 0.5},
        {"name": "hyp_2", "posterior_confidence": 0.1, "pragmatic_value": 0.2, "epistemic_gain": 0.1}
    ]
    dec_res = dec_engine.evaluate_and_kill_hypotheses(hypotheses, falsification_threshold=0.2)
    assert "hyp_2" in dec_res["killed_hypotheses"]
    assert dec_res["best_decision"] == "hyp_1"


def test_layer_5_to_9_evaluation_product_growth() -> None:
    # Layer 5 Evaluation EV
    eval_engine = Layer5EvaluationEngine()
    ev_res = eval_engine.calculate_opportunity_ev(tam_cents=500000000, p_success=0.7, downside_risk_cents=20000000)
    assert ev_res["expected_value_cents"] > 0
    assert ev_res["is_viable"]

    # Layer 6 Product JTBD
    prod_engine = Layer6ProductEngine()
    jtbd_res = prod_engine.extract_jtbd_core(
        user_complaints=["High price", "Clunky UX"],
        candidate_features=[
            {"name": "Fast Checkout", "value_impact": 0.8, "complexity": 0.3},
            {"name": "Bloated Feature", "value_impact": 0.2, "complexity": 0.9}
        ]
    )
    assert "Fast Checkout" in jtbd_res["mvp_features"]
    assert "Bloated Feature" in jtbd_res["pruned_features"]

    # Layer 7 Customer Utility
    cust_engine = Layer7CustomerEngine()
    cust_res = cust_engine.model_customer_psychology(trust_level=0.9, perceived_value=0.85, switching_friction=0.2)
    assert cust_res["will_buy"]
    assert cust_res["is_evangelist"]

    # Layer 8 Marketing Viral Propagation
    mktg_engine = Layer8MarketingEngine()
    mktg_res = mktg_engine.propagate_attention(initial_reach=1000, viral_k_factor=1.5, conversion_rate=0.1)
    assert mktg_res["total_acquired_customers"] > 100

    # Layer 9 Sales Objection Graph
    sales_engine = Layer9SalesEngine()
    sales_res = sales_engine.resolve_objection_graph("No budget", {"No budget": "Offer monthly payment"}, urgency_score=0.8)
    assert sales_res["automation_recommended"]
    assert sales_res["sales_motion"] == "automated_self_serve"


def test_layer_10_to_13_competition_org_metalearning() -> None:
    # Layer 10 Growth Network Effects
    growth_engine = Layer10GrowthEngine()
    growth_res = growth_engine.evaluate_network_effects(user_count=900, engagement_factor=0.05, system_capacity=1000)
    assert growth_res["should_throttle_growth"]

    # Layer 11 Competition Moat
    comp_engine = Layer11CompetitionEngine()
    comp_res = comp_engine.simulate_competitor_moves("Feature release", {"Copy feature": 0.8}, moat_type="network_effects")
    assert comp_res["is_defensible"]

    # Layer 12 Org Design Hiring Trigger
    org_engine = Layer12OrgDesignEngine()
    org_res = org_engine.evaluate_hiring_triggers(task_backlog_hours=60.0, agent_utilization_ratio=0.9, unit_economics_positive=True)
    assert org_res["should_expand_org"]

    # Layer 13 Meta-Learning Playbook Distillation
    meta_engine = Layer13MetaLearningEngine()
    meta_res = meta_engine.distill_closed_loop_playbook(predicted_outcome=100.0, actual_outcome=80.0, decision_context={"domain": "fintech"})
    assert meta_res["update_mental_model"]
    assert "calibration score" in meta_res["distilled_playbook_lesson"]


def test_layer_14_orchestrator_end_to_end_pipeline() -> None:
    orchestrator = Layer14AIEntrepreneurshipOrchestrator()
    signal_data = {
        "title": "Autonomous AI Agent OS",
        "source": "developer_trends",
        "domain": "artificial_intelligence",
        "intensity": 0.9,
        "tam_cents": 1000000000
    }
    result = orchestrator.run_end_to_end_pipeline(signal_data)
    assert result["status"] == "completed"
    assert result["opportunity_title"] == "Autonomous AI Agent OS"
    assert "meta_learning_lesson" in result
