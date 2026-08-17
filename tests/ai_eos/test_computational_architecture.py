from __future__ import annotations
import pytest
from uuid import uuid4

from apodex.ai_eos.intelligence.computational_architecture import (
    Opportunity,
    AdvancedCausalEngine,
    ActiveInferencePlanner,
    RealityEngine,
    OpportunityDiscoveryEngine,
    ProblemDiscoveryEngine,
    DecisionMakingSystem,
    OpportunityEvaluationSystem,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingDynamicsEngine,
    SalesSystemsEngine,
    GrowthEcosystemEngine,
    CompetitionMoatEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    AIEntrepreneurshipEngine,
    EntrepreneurialIntelligenceOrchestrator,
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


def test_reality_and_opportunity_discovery_engines() -> None:
    reality = RealityEngine()
    task_p = reality.partition_task("pricing_model_optimization")
    assert task_p["automatable"] is True
    assert task_p["recommended_executor"] == "ALGORITHMIC_AGENT"

    task_h = reality.partition_task("investor_pitch_and_empathy_building")
    assert task_h["automatable"] is False
    assert task_h["recommended_executor"] == "HUMAN_FOUNDER"

    discovery = OpportunityDiscoveryEngine()
    filtered = discovery.filter_weak_signal({"title": "noisy_signal", "signal_strength": 0.1, "noise_level": 0.9}, noise_threshold=0.3)
    assert filtered is None

    jaccard = discovery.compute_jaccard_similarity(["ai", "saas", "b2b"], ["ai", "saas", "fintech"])
    assert pytest.approx(jaccard, 0.01) == 2.0 / 4.0

    novelty = discovery.evaluate_novelty_score(["quantum", "bio"], [["ai", "saas"], ["crypto", "web3"]])
    assert novelty == 1.0


def test_problem_discovery_and_decision_making() -> None:
    problem_engine = ProblemDiscoveryEngine()
    decomp = problem_engine.decompose_problem("High_User_Churn")
    assert "first_order_root_cause" in decomp
    assert decomp["should_ignore"] is False

    root_eval = problem_engine.evaluate_root_cause_vs_symptom("latency_spike", confounding_score=0.8)
    assert root_eval["classification"] == "SYMPTOM"

    decision_sys = DecisionMakingSystem()
    opp_risky = Opportunity(title="risky", domain="tech", success_probability=0.05, prior_entropy=3.0)
    assert decision_sys.evaluate_kill_gate(opp_risky) is True

    skeptic = decision_sys.run_skeptic_node_counter_model(
        Opportunity(title="test", domain="tech", success_probability=0.9),
        factual_conversion_rate=0.2
    )
    assert skeptic["has_confirmation_bias"] is True
    assert skeptic["corrected_success_probability"] == 0.2


def test_opportunity_evaluation_and_product_creation() -> None:
    eval_sys = OpportunityEvaluationSystem()
    opp = Opportunity(
        title="B2B AI Platform",
        domain="software",
        tam_cents=500000000,
        success_probability=0.4,
        downside_cvar_cents=10000000,
        timing_window_months=12
    )
    quality = eval_sys.evaluate_opportunity_quality(opp)
    assert quality["expected_value_cents"] == 200000000
    assert quality["recommendation"] == "PROCEED"

    product_engine = ProductCreationEngine()
    val = product_engine.evaluate_feature_value("analytics_dashboard", jtbd_impact=0.9, complexity_cost=0.4)
    # 0.9 - 0.5*(0.4^2) = 0.9 - 0.08 = 0.82
    assert pytest.approx(val, 0.01) == 0.82

    jtbd = product_engine.discover_job_to_be_done([{"action": "automate_invoice_reconciliation"}])
    assert "automate_invoice_reconciliation" in jtbd


def test_customer_marketing_and_sales_engines() -> None:
    customer_engine = CustomerUnderstandingEngine()
    s1 = customer_engine.transition_customer_state("AWARE", "TRY_DEMO", trust_score=0.5)
    assert s1 == "CONSIDERING"

    s2 = customer_engine.transition_customer_state("CONSIDERING", "NONE", trust_score=0.8)
    assert s2 == "ACTIVE_USER"

    friction = customer_engine.calculate_switching_friction(data_lock_in=0.9, workflow_embedding=0.8)
    assert pytest.approx(friction, 0.01) == 0.86

    marketing_engine = MarketingDynamicsEngine()
    k = marketing_engine.calculate_viral_coefficient_k(invite_rate=5.0, conversion_rate=0.25)
    assert pytest.approx(k, 0.01) == 1.25

    sales_engine = SalesSystemsEngine()
    objection = sales_engine.resolve_objection("PRICE_TOO_HIGH")
    assert "usage-based tiering" in objection["resolution_strategy"]

    motion = sales_engine.route_sales_motion(contract_value_cents=10000000)
    assert motion == "ENTERPRISE_HIGH_TOUCH"


def test_growth_competition_and_org_design() -> None:
    growth_engine = GrowthEcosystemEngine()
    health = growth_engine.calculate_growth_health(
        ltv_cents=300000,
        cac_cents=50000,
        nrr_percent=1.25,
        burn_multiple=1.2
    )
    assert health["is_compounding_healthy"] is True

    moat_engine = CompetitionMoatEngine()
    moat_score = moat_engine.score_7_powers_moat({
        "network_effects": 0.9,
        "counter_positioning": 0.8,
        "switching_costs": 0.7
    })
    assert moat_score > 0.4

    org_engine = OrganizationalDesignEngine()
    triggers = org_engine.evaluate_hiring_triggers({"talent_capacity": 0.85, "compute": 0.2})
    assert "HIRE_SPECIALIST_FOR_TALENT_CAPACITY" in triggers


def test_meta_learning_and_unified_14_layer_orchestrator() -> None:
    meta_engine = MetaLearningEngine()
    a, b = meta_engine.update_mental_model_prior(prior_alpha=10.0, prior_beta=10.0, observed_successes=5, observed_failures=1)
    assert a == 15.0 and b == 11.0

    schema = meta_engine.convert_failure_to_schema({"root_cause": "uncalibrated_pricing", "binding_constraint": "capital"})
    assert "uncalibrated_pricing" in schema["root_cause"]

    ai_engine = AIEntrepreneurshipEngine()
    task_matrix = ai_engine.formalize_task_matrix(["pricing_optimization", "culture_setting"])
    assert len(task_matrix) == 2

    orchestrator = EntrepreneurialIntelligenceOrchestrator()
    signal = {
        "title": "Quantum AI Cloud Engine",
        "domain": "deep_tech",
        "signal_strength": 0.9,
        "noise_level": 0.1,
        "variables": ["compute_scale", "customer_retention"],
        "causal_edges": [("compute_scale", "customer_retention")],
        "coefficients": {"compute_scale->customer_retention": 0.8},
        "prior_entropy": 1.2,
        "post_entropy_simulated": 0.3,
        "success_probability": 0.7,
        "tam_cents": 1000000000
    }
    orchestrator.ingest_signal(signal)
    res = orchestrator.execute_orchestrated_pipeline()
    assert res["status"] == "executed"
    assert res["selected_opportunity"] == "Quantum AI Cloud Engine"
    assert "moat_score" in res
    assert "job_to_be_done" in res
