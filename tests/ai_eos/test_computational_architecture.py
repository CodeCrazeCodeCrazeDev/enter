from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    RealityInvariantsEngine,
    OpportunityDiscoveryEngine,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    OpportunityEvaluator,
    ProductCreationEngine,
    CustomerPsychologyEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitiveEngine,
    OrganizationalEngine,
    MetaLearningEngine,
    EntrepreneurialIntelligenceOrchestrator
)


def test_layer1_reality_invariants() -> None:
    # Test task automation classification
    res_human = RealityInvariantsEngine.classify_task_automatability(
        task_name="Legal Restructuring",
        ambiguity_level=0.9,
        emotional_charge=0.2,
        legal_sovereignty_required=True
    )
    assert not res_human.is_automatable
    assert res_human.requires_human_judgment

    res_ai = RealityInvariantsEngine.classify_task_automatability(
        task_name="Ad Budget Optimization",
        ambiguity_level=0.2,
        emotional_charge=0.1,
        legal_sovereignty_required=False
    )
    assert res_ai.is_automatable
    assert not res_ai.requires_human_judgment


def test_layer2_opportunity_discovery() -> None:
    discovery = OpportunityDiscoveryEngine()

    raw_signals = [
        {"name": "SignalA", "magnitude": 1.2, "noise_variance": 2.0},  # low SNR = 0.6
        {"name": "SignalB", "magnitude": 0.1, "noise_variance": 1.0},  # low SNR = 0.1
        {"name": "SignalC", "magnitude": 2.5, "noise_variance": 0.5},  # high SNR = 5.0
    ]

    filtered = discovery.detect_weak_signals(raw_signals, snr_threshold=0.5)
    assert len(filtered) == 2
    assert filtered[0]["name"] == "SignalA"
    assert filtered[1]["name"] == "SignalC"

    # Combinatorial synthesis
    opp_synthesis = discovery.combinatorial_synthesis(
        {"name": "AI_Agents", "domain": "software", "keywords": ["ai", "agent"], "tam_cents": 100000000},
        {"name": "BioTech", "domain": "health", "keywords": ["pharma", "ai"], "tam_cents": 200000000}
    )
    assert "Synergy: AI_Agents + BioTech" in opp_synthesis.title
    assert opp_synthesis.tam_cents == 210000000

    # Trend velocity
    velocity = discovery.calculate_trend_velocity([10.0, 15.0, 30.0])
    assert velocity == 1.0  # (30 - 15) / 15 = 1.0


def test_layer3_causal_engine_and_symptom_decomposition() -> None:
    engine = AdvancedCausalEngine()
    engine.add_causal_relationship("marketing_spend", "click_through_rate", 0.6)
    engine.add_causal_relationship("click_through_rate", "sales_revenue", 1.8)

    # 1. do-calculus
    state = engine.execute_do_intervention("marketing_spend", 2.0)
    assert state["marketing_spend"] == 2.0
    assert pytest.approx(state["click_through_rate"]) == 1.2
    assert pytest.approx(state["sales_revenue"]) == 2.16

    # 2. Counterfactual
    factual = {"marketing_spend": 1.0, "click_through_rate": 0.8, "sales_revenue": 1.44}
    counterfactual = engine.estimate_counterfactual(
        factual_observations=factual,
        counterfactual_intervention=("marketing_spend", 2.0),
        target_outcome_var="sales_revenue"
    )
    assert pytest.approx(counterfactual) == 2.52

    # 3. Root cause vs symptom decomposition
    decomp = engine.decompose_symptom_vs_root_cause("sales_revenue")
    assert "marketing_spend" in decomp["root_causes"]
    assert "sales_revenue" in decomp["symptoms"]


def test_layer4_active_inference_planner() -> None:
    planner = ActiveInferencePlanner(curiosity_weight=2.0)

    opp_1 = Opportunity(
        title="high_exploratory",
        domain="tech",
        prior_entropy=2.0,
        post_entropy_simulated=0.4,
        success_probability=0.4,
        target_preference=0.9
    )
    opp_2 = Opportunity(
        title="conservative",
        domain="retail",
        prior_entropy=0.6,
        post_entropy_simulated=0.5,
        success_probability=0.85,
        target_preference=0.9
    )

    ranked = planner.rank_opportunities([opp_1, opp_2])
    assert ranked[0][0].title == "high_exploratory"

    # Fast kill gate
    bad_opp = Opportunity(title="doomed", domain="legacy", success_probability=0.05)
    killed = planner.evaluate_fast_kill_gate(bad_opp, min_success_prob=0.2)
    assert killed
    assert not bad_opp.is_active


def test_layer5_opportunity_evaluation() -> None:
    ev = OpportunityEvaluator.calculate_expected_value(
        tam_cents=100000000,
        win_prob=0.6,
        cac_cents=5000,  # $50
        ltv_cents=25000  # $250
    )
    assert ev == 10000.0

    kelly = OpportunityEvaluator.kelly_criterion_fraction(win_prob=0.6, win_loss_ratio=5.0)
    assert kelly == 0.25

    var = OpportunityEvaluator.estimate_downside_var(capital_at_risk_cents=100000, confidence_level=0.95)
    assert var > 0.0

    abandon = OpportunityEvaluator.evaluate_abandonment(current_ev=100.0, alternative_ev=250.0, switching_cost=50.0)
    assert abandon


def test_layers_6_to_13_specialized_engines() -> None:
    # Layer 6 Product Creation
    product_eng = ProductCreationEngine()
    jtbd = product_eng.discover_core_jtbd(["high latency", "manual overhead"], ["instant execution", "low cost"])
    assert "Eliminate [high latency, manual overhead]" in jtbd["core_jtbd"]

    feats = product_eng.minimize_feature_complexity([
        {"name": "F1", "value_impact": 10.0, "complexity": 2.0},
        {"name": "F2", "value_impact": 2.0, "complexity": 10.0},
    ])
    assert feats[0]["name"] == "F1"

    # Layer 7 Customer Psychology
    cust_eng = CustomerPsychologyEngine()
    trust = cust_eng.model_trust_decay(initial_trust=1.0, failure_events=2, days_elapsed=10)
    assert trust < 1.0

    hazard = cust_eng.compute_churn_hazard(usage_drop_percent=0.4, support_ticket_count=4, nps_score=5)
    assert hazard > 0.5

    # Layer 8 Marketing
    mkt_eng = MarketingEngine()
    k_factor = mkt_eng.calculate_virality_k_factor(invites_per_user=3.0, conversion_rate_per_invite=0.4)
    assert pytest.approx(k_factor) == 1.2  # K > 1 implies virality

    # Layer 9 Sales
    sales_eng = SalesEngine()
    routing = sales_eng.route_sales_mode(acv_cents=5000000, complexity_score=0.8)
    assert routing == "ENTERPRISE_HIGH_TOUCH"

    # Layer 10 Growth
    growth_eng = GrowthEngine()
    density = growth_eng.calculate_network_effect_density(active_nodes=5, total_edges=8)
    assert density == 0.8

    # Layer 11 Competition
    comp_eng = CompetitiveEngine()
    moat = comp_eng.score_moat_durability(switching_costs=0.8, network_density=0.9, scale_economies=0.7, brand_trust=0.9)
    assert moat > 0.8

    # Layer 12 Organizational Design
    org_eng = OrganizationalEngine()
    delegation = org_eng.determine_delegation_boundary(reversibility_score=0.9, capital_risk_cents=500000)
    assert delegation == "DELEGATE_TO_AUTONOMOUS_AGENT"

    # Layer 13 Meta-Learning (normalized outcomes in [0, 1])
    meta_eng = MetaLearningEngine()
    quality = meta_eng.measure_decision_quality(predicted_outcome=0.90, actual_outcome=0.80)
    assert pytest.approx(quality) == 0.90


def test_layer14_master_orchestrator_pipeline() -> None:
    orchestrator = EntrepreneurialIntelligenceOrchestrator()

    signal = {
        "title": "Autonomous AI Hardware Venture",
        "domain": "robotics",
        "variables": ["spend", "conversion", "revenue"],
        "causal_edges": [("spend", "conversion"), ("conversion", "revenue")],
        "coefficients": {"spend->conversion": 0.5, "conversion->revenue": 2.0},
        "prior_entropy": 1.8,
        "post_entropy_simulated": 0.5,
        "success_probability": 0.6,
        "tam_cents": 500000000
    }

    orchestrator.ingest_signal(signal)
    pipeline_result = orchestrator.execute_orchestrated_pipeline()

    assert pipeline_result["status"] == "executed"
    assert pipeline_result["selected_opportunity"] == "Autonomous AI Hardware Venture"
    assert "best_expected_free_energy" in pipeline_result
    assert "expected_value_cents" in pipeline_result
    assert pytest.approx(pipeline_result["virality_k_factor"]) == 1.0
    assert pipeline_result["sales_routing_mode"] == "AUTOMATED_SELF_SERVE"
    assert len(orchestrator.learned_lessons) == 1
