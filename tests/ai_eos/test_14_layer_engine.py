"""
Unit and integration test suite for the 14-Layer Computational Architecture Engine.
"""

from __future__ import annotations
import pytest
import math
from uuid import uuid4

from apodex.ai_eos.intelligence.fourteen_layer_engine import (
    VentureState,
    OpportunitySignal,
    ProblemSCM,
    CustomerAgentModel,
    ProductSpec,
    RealitySubstrateEngine,
    OpportunityDiscoveryEngine,
    ProblemDiscoveryEngine,
    DecisionMakingEngine,
    OpportunityEvaluationEngine,
    ProductCreationEngine,
    CustomerUnderstandingEngine,
    MarketingEngine,
    SalesEngine,
    GrowthEngine,
    CompetitionEngine,
    OrganizationalDesignEngine,
    MetaLearningEngine,
    AIEntrepreneurshipMasterOrchestrator
)


def test_layer1_reality_substrate() -> None:
    engine = RealitySubstrateEngine()

    res = engine.evaluate_thermodynamic_bounds(inputs_cents=1000, outputs_cents=2500)
    assert res["thermodynamically_viable"] is True
    assert res["net_value_created_cents"] == 1500
    assert pytest.approx(res["roi"]) == 1.5

    task_human = engine.classify_task_automation_boundary("Define ultimate human meaning and ethical alignment")
    assert task_human["automatable"] is False

    task_algo = engine.classify_task_automation_boundary("Optimize marketing spend ad bidding allocation")
    assert task_algo["automatable"] is True


def test_layer2_opportunity_discovery() -> None:
    engine = OpportunityDiscoveryEngine()

    signal = OpportunitySignal(
        title="AI Medical Diagnostics",
        domain="healthcare",
        market_entropy=2.5,
        reality_entropy=0.5,
        prior_success_prob=0.1
    )

    res = engine.detect_weak_signals(signal)
    assert res["is_actionable_weak_signal"] is True
    assert res["kl_divergence"] == 2.0
    assert res["shannon_surprise"] > 2.0

    scm_a = ProblemSCM(title="Tech", variables=["compute_cost"], causal_edges=[])
    scm_b = ProblemSCM(title="Bio", variables=["sequencing_speed"], causal_edges=[])
    combined = engine.combine_disparate_domains(scm_a, scm_b)

    assert len(combined.variables) == 2
    assert ("compute_cost", "sequencing_speed") in combined.causal_edges


def test_layer3_problem_discovery() -> None:
    engine = ProblemDiscoveryEngine()

    scm = ProblemSCM(
        title="E-commerce Churn",
        variables=["page_load_time", "cart_abandonment", "churn_rate"],
        causal_edges=[("page_load_time", "cart_abandonment"), ("cart_abandonment", "churn_rate")],
        coefficients={"page_load_time->cart_abandonment": 0.8, "cart_abandonment->churn_rate": 1.5}
    )

    res = engine.isolate_root_cause(scm)
    assert res["root_cause"] == "page_load_time"
    assert res["symptom"] == "churn_rate"

    ignore = engine.evaluate_ignore_criteria(evig=10.0, delta_utility=20.0, cost_investigate=50.0)
    assert ignore is True


def test_layer4_decision_making() -> None:
    engine = DecisionMakingEngine()

    posterior = engine.resolve_bayesian_intuition_data(
        prior_prob=0.3,
        evidence_likelihood=0.9,
        sample_size=50
    )
    assert pytest.approx(posterior) == 0.9  # With N=50, data dominates

    # SPRT test
    log_ratios_accept = [0.8, 1.2, 0.9, 1.5]
    res_accept = engine.evaluate_sprt_kill_gate(log_ratios_accept)
    assert res_accept == "ACCEPT_HYPOTHESIS"

    log_ratios_kill = [-1.0, -1.2, -1.5]
    res_kill = engine.evaluate_sprt_kill_gate(log_ratios_kill)
    assert res_kill == "KILL_IDEA_IMMEDIATELY"


def test_layer5_opportunity_evaluation() -> None:
    engine = OpportunityEvaluationEngine()

    ev_res = engine.calculate_expected_value_and_risk(
        tam_cents=100000000,
        gross_margin=80.0,
        success_prob=0.5,
        jump_volatility=0.2
    )
    assert ev_res["raw_expected_value_cents"] == 40000000
    assert ev_res["discounted_ev_cents"] < 40000000

    timing = engine.evaluate_real_options_timing(volatility=0.9, competitor_preemption_rate=0.1)
    assert timing == "DEFER_AND_GATHER_INFORMATION"


def test_layer6_product_creation() -> None:
    engine = ProductCreationEngine()

    spec = ProductSpec(
        title="Bloated SaaS Product",
        features=["f1", "f2", "f3", "f4", "f5", "f6"],
        complexity_score=4.0,
        estimated_build_cost_cents=1000000
    )

    regularized = engine.regularize_product_complexity(spec, max_complexity=2.0)
    assert len(regularized.features) < len(spec.features)
    assert regularized.complexity_score < spec.complexity_score


def test_layer7_customer_understanding() -> None:
    engine = CustomerUnderstandingEngine()

    customer = CustomerAgentModel(
        segment="enterprise",
        push_friction=0.8,
        pull_attraction=0.9,
        inertia_cost=0.2,
        anxiety_risk=0.1
    )

    p_switch = engine.calculate_switch_probability(customer)
    assert p_switch > 0.7

    updated_trust = engine.update_trust_vector(current_trust=0.8, delivered_value=1.0, failure_magnitude=0.5)
    assert updated_trust < 0.8  # Rapid drop under failure


def test_layers8_to_13_engines() -> None:
    marketing = MarketingEngine()
    sales = SalesEngine()
    growth = GrowthEngine()
    competition = CompetitionEngine()
    org = OrganizationalDesignEngine()
    meta = MetaLearningEngine()

    # Marketing
    dist = marketing.project_positioning_distance([1.0, 1.0], [[0.0, 0.0]])
    assert pytest.approx(dist) == math.sqrt(2.0)

    # Sales
    loss = sales.calculate_inaction_compounding_loss(50000, 12)
    assert loss > 50000

    mode = sales.determine_sales_automation_mode(acv_cents=200000)
    assert mode == "AUTOMATED_SELF_SERVE_FUNNEL"

    # Growth
    net_val = growth.evaluate_network_value(100)
    assert pytest.approx(net_val) == 100 * math.log(100)

    # Competition
    moat = competition.calculate_7_powers_moat_score({"scale_economies": 0.8, "switching_costs": 0.6})
    assert moat > 0.0

    # Org
    hiring = org.calculate_hiring_shadow_price(bottleneck_utility_delta=200.0, wage_cents=1000000)
    assert hiring["trigger_hiring_workflow"] is True

    # Meta
    triple_loop = meta.execute_triple_loop_backprop(prediction_error=0.6, current_model_params={"theta": 0.5})
    assert triple_loop["loop3_trigger_architecture_rewrite"] is True


def test_layer14_master_orchestrator_pipeline() -> None:
    orchestrator = AIEntrepreneurshipMasterOrchestrator()

    signal = OpportunitySignal(
        title="Autonomous AI Agent Operating System",
        domain="ai_infrastructure",
        market_entropy=2.2,
        reality_entropy=0.4,
        prior_success_prob=0.2,  # Low prior = high Shannon surprise (-ln(0.2) = 1.6 > 1.0)
        tam_cents=500000000
    )

    venture = VentureState(
        title="Apodex AI EOS Venture",
        capital_reserves_cents=50000000,
        monthly_burn_cents=2000000,
        active_customers=50,
        monthly_recurring_revenue_cents=3000000
    )

    res = orchestrator.run_full_14_layer_pipeline(signal, venture)

    assert res["status"] == "orchestrated"
    assert res["opportunity_title"] == "Autonomous AI Agent Operating System"
    assert res["layer1_viability"] is True
    assert res["layer2_weak_signal"] is True
    assert res["layer3_root_cause"] == "marketing_spend"
    assert res["layer5_discounted_ev_cents"] > 0
    assert res["layer7_switch_probability"] > 0.5
    assert res["layer10_network_value"] > 0
    assert res["layer12_hiring"] is True
