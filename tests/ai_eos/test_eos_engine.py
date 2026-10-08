"""Comprehensive unit, integration, and chaotic tests for the EOS Cognitive Engine.

Verifies all systems and their interactions under standard and boundary scenarios.
"""

from __future__ import annotations
import math
import pytest
from uuid import uuid4

from apodex.ai_eos.domain.models import VentureCell, Hypothesis, Evidence
from apodex.ai_eos.intelligence.eos_engine import (
    EntrepreneurialWorldModel,
    OpportunityGraph,
    HypothesisEngine,
    BusinessSimulator,
    StrategicPlanner,
    CapitalAllocationEngine,
    PortfolioManager,
    CompetitiveIntelligenceEngine,
    MoatAnalyzer,
    FailurePredictionEngine,
    ReinventionEngine,
    EntrepreneurialMemory,
    EvaluationFramework,
    EOSOpportunityDecisionTree,
    CompanyGrowthStateMachine,
    CompanyStage,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    EOSEngine,
)


def test_world_model_stochastic():
    """Verify stochastic transitions and platform shifts in the World Model."""
    wm = EntrepreneurialWorldModel()
    assert wm.state["competitor_count"] == 5
    assert not wm.state["technology_platform_shift"]

    # Run multiple transitions to ensure stability and potential shifts
    for _ in range(50):
        wm.transition_state()

    assert wm.state["market_demand_index"] > 0.0
    entropy = wm.calculate_state_entropy()
    assert 0.0 <= entropy <= 1.0


def test_opportunity_graph_similarity():
    """Verify Directed Graph representation and Jaccard similarity searches."""
    og = OpportunityGraph()
    og.add_opportunity("op_001", "AI Code Assistant", 500000_00, ["ai", "developer", "automation"])
    og.add_opportunity("op_002", "Developer Tools Platform", 200000_00, ["developer", "cli", "platform"])
    og.add_opportunity("op_003", "BioTech Drug Discovery", 12000000_00, ["biotech", "ai", "pharma"])

    og.add_dependency("op_001", "op_002")
    assert "op_002" in og.nodes["op_001"].adjacent_ids

    # Search similarity for "ai" and "developer"
    matches = og.find_similar_opportunities(["ai", "developer"], threshold=0.1)
    assert len(matches) >= 2
    # op_001 has highest overlap
    assert matches[0][0] == "op_001"


def test_hypothesis_engine_lifecycle():
    """Verify hypothesis promotion and Beta conjugate updates via statistical evidence."""
    engine = HypothesisEngine()
    hyp = Hypothesis(
        hypothesis_id=uuid4(),
        statement="Top banner increases signups by 10%.",
        prior_confidence=0.50,
        posterior_confidence=0.50,
        confidence_distribution={"type": "beta", "params": {"alpha": 10.0, "beta": 10.0}},
        status="proposed"
    )
    engine.add_hypothesis(hyp)

    # 1. Add supporting evidence (low p-value, positive effect size)
    ev_sup = Evidence(
        evidence_id="ev_001",
        source="A/B Test Run 1",
        source_type="experiment",
        method="experiment",
        reliability_weight=0.9,
        strength={"p_value": 0.01, "effect_size": 0.15},
        linked_hypotheses=[str(hyp.hypothesis_id)]
    )
    engine.update_with_evidence(hyp.hypothesis_id, ev_sup)
    assert hyp.confidence_distribution["params"]["alpha"] == 11.0
    assert hyp.posterior_confidence > 0.50

    # 2. Add contradicting evidence (high p-value or non-positive effect size)
    ev_con = Evidence(
        evidence_id="ev_002",
        source="A/B Test Run 2",
        source_type="experiment",
        method="experiment",
        reliability_weight=0.8,
        strength={"p_value": 0.45, "effect_size": -0.05},
        linked_hypotheses=[str(hyp.hypothesis_id)]
    )
    engine.update_with_evidence(hyp.hypothesis_id, ev_con)
    assert hyp.confidence_distribution["params"]["beta"] == 11.0

    # 3. Add multiple supporting items to trigger promotion (need enough to exceed 0.80)
    for i in range(40):
        ev = Evidence(
            evidence_id=f"ev_sup_{i}",
            source="A/B Multi Test",
            source_type="experiment",
            strength={"p_value": 0.001, "effect_size": 0.2},
            linked_hypotheses=[str(hyp.hypothesis_id)]
        )
        engine.update_with_evidence(hyp.hypothesis_id, ev)

    promoted = engine.evaluate_promotions()
    assert hyp.hypothesis_id in promoted
    assert hyp.status == "active"


def test_business_simulator_cohorts():
    """Verify customer GTM cohort conversion and unit economics math."""
    sim = BusinessSimulator()
    res_healthy = sim.simulate_gtm_cohort(
        traffic=10000,
        conversion_rate=0.03,
        arpu_cents=50_00,       # $50
        cac_cents=100_00,       # $100
        churn_rate=0.02        # 2% monthly
    )
    assert res_healthy["customers_acquired"] == 300
    assert res_healthy["monthly_recurring_revenue_cents"] == 15000_00
    assert res_healthy["ltv_cents"] == 2500_00  # $50 / 0.02 = $2500
    assert res_healthy["ltv_to_cac_ratio"] == 25.0
    assert res_healthy["cac_payback_months"] == 2.0
    assert res_healthy["unit_economics_healthy"] is True

    res_unhealthy = sim.simulate_gtm_cohort(
        traffic=5000,
        conversion_rate=0.01,
        arpu_cents=10_00,       # $10
        cac_cents=200_00,       # $200
        churn_rate=0.10        # 10% monthly
    )
    assert res_unhealthy["unit_economics_healthy"] is False


def test_strategic_planner_efe():
    """Verify that the Strategic Planner selects policy sequences minimizing EFE."""
    planner = StrategicPlanner()

    # Policy A: high utility, low uncertainty, low risk
    policy_a = {"name": "Test Segment A", "expected_utility": 10.0, "predictive_entropy": 0.2, "risk_factor": 0.1}
    # Policy B: low utility, high uncertainty, high risk
    policy_b = {"name": "Explore Segment B", "expected_utility": 2.0, "predictive_entropy": 0.9, "risk_factor": 0.8}

    best = planner.select_optimal_policy([policy_a, policy_b])
    assert best["name"] == "Test Segment A"
    assert best["computed_efe"] < 2.0


def test_capital_allocation_engine_ceilings():
    """Verify multi-objective allocation logic with capacity/risk ceilings."""
    allocator = CapitalAllocationEngine()

    cell_safe = VentureCell(
        name="Venture Alpha",
        namespace="alpha",
        allocated_capital_cents=0,
        expected_free_energy=5.0,
        risk=0.1
    )
    cell_risky = VentureCell(
        name="Venture Beta",
        namespace="beta",
        allocated_capital_cents=0,
        expected_free_energy=10.0,
        risk=0.8  # Exceeds risk limit -> capped at 25% of total budget
    )

    allocations = allocator.allocate([cell_safe, cell_risky], total_budget_cents=100000_00)

    # Cents allocated to risky should be capped
    risky_allocation = allocations[cell_risky.cell_id]
    assert risky_allocation <= 25000_00


def test_portfolio_manager_adaptation():
    """Verify budget shifts based on systemic market uncertainty."""
    pm = PortfolioManager()

    # Case 1: Low uncertainty
    pm.adjust_proportions(total_capital_cents=100000_00, market_uncertainty=0.2)
    assert pm.research_budget_cents == 15000_00
    assert pm.venture_budget_cents == 85000_00

    # Case 2: High uncertainty (explores options value)
    pm.adjust_proportions(total_capital_cents=100000_00, market_uncertainty=0.8)
    assert pm.research_budget_cents == 40000_00
    assert pm.venture_budget_cents == 60000_00


def test_competitor_intel_and_moats():
    """Verify feature parity and moat score computations."""
    cie = CompetitiveIntelligenceEngine()
    cie.register_competitor("Competitor X", 0.40, ["sso", "analytics", "realtime"])
    cie.register_competitor("Competitor Y", 0.20, ["sso", "billing"])

    parity = cie.compute_feature_parity(["sso", "analytics"])
    assert parity == 0.5

    ma = MoatAnalyzer()
    score = ma.score_moat(
        network_density=0.8,
        avg_switching_cost_cents=5000_00,  # $5,000
        brand_trust_score=0.9,
        cost_advantage_percent=0.15
    )
    assert 0.0 <= score <= 1.0


def test_failure_predictor_and_reinvention():
    """Verify insolvency hazard modeling, bottleneck analysis, and pivot triggers."""
    fpe = FailurePredictionEngine()
    prob_high = fpe.predict_insolvency_probability(burn_multiple=3.0, runway_months=3.0, ltv_to_cac=1.5)
    assert prob_high > 0.60

    prob_low = fpe.predict_insolvency_probability(burn_multiple=1.1, runway_months=18.0, ltv_to_cac=4.5)
    assert prob_low < 0.15

    # Bottleneck latency
    latencies = [0.5, 4.2, 0.2, 8.5]
    bottlenecks = fpe.detect_bottlenecks(latencies, sla_threshold=3.0)
    assert len(bottlenecks) == 2
    assert "process_step_3" in bottlenecks[1]

    # Reinvention
    re = ReinventionEngine()
    assert re.check_reinvention_trigger(monthly_revenue_decay=0.20, customer_attrition_rate=0.25) is True
    assert re.check_reinvention_trigger(monthly_revenue_decay=0.01, customer_attrition_rate=0.02) is False


def test_memory_trajectories():
    """Verify trajectory history recording and value-based selective matching."""
    mem = EntrepreneurialMemory()
    cell_id = uuid4()

    mem.record_step(cell_id, "GTM Launch", {"cac": 120, "mrr": 5000})
    mem.record_step(cell_id, "Scale GTM", {"cac": 180, "mrr": 12000})

    matches = mem.retrieve_matching_trajectories("mrr", 8000)
    assert len(matches) == 1
    assert matches[0]["step"] == "Scale GTM"


def test_evaluation_framework_grc():
    """Verify GRC and risk score filters."""
    ef = EvaluationFramework()
    assert ef.audit_ethical_alignment("Launch high-risk unaligned campaign", 0.95) is False
    assert ef.audit_ethical_alignment("Deploy standard refactoring", 0.10) is True


def test_eos_decision_tree():
    """Verify Section 10.2 decision tree logic."""
    tree = EOSOpportunityDecisionTree()

    # Noise signal -> Discard
    res_noise = tree.evaluate(is_structural_anomaly=False, is_reversible=True)
    assert res_noise["pursue"] is False
    assert "Noise" in res_noise["reason"]

    # Irreversible without high confidence -> Discard
    res_type1 = tree.evaluate(is_structural_anomaly=True, is_reversible=False, multi_source_confidence=0.5)
    assert res_type1["pursue"] is False

    # Valid opportunity -> Pursue
    res_valid = tree.evaluate(
        is_structural_anomaly=True,
        is_reversible=True,
        cheap_test_available=True,
        test_result_score=0.8,
        kill_threshold=0.6,
        has_structural_advantage=True
    )
    assert res_valid["pursue"] is True


def test_growth_state_machine():
    """Verify stage classification across Section 6 growth stages."""
    sm = CompanyGrowthStateMachine()

    assert sm.classify_stage(0, False, 0.0, 0, 0.0) == CompanyStage.IDEA
    assert sm.classify_stage(5, False, 0.0, 0, 0.0) == CompanyStage.VALIDATION
    assert sm.classify_stage(20, False, 0.1, 0, 0.0) == CompanyStage.STARTUP
    assert sm.classify_stage(100, True, 0.1, 0, 0.0) == CompanyStage.PMF
    assert sm.classify_stage(500, True, 0.3, 0, 0.0) == CompanyStage.GROWTH
    assert sm.classify_stage(2000, True, 0.6, 0, 0.0) == CompanyStage.SCALE
    assert sm.classify_stage(5000, True, 0.6, 15, 0.0) == CompanyStage.PLATFORM
    assert sm.classify_stage(10000, True, 0.6, 60, 0.0) == CompanyStage.ECOSYSTEM
    assert sm.classify_stage(50000, True, 0.6, 100, 0.45) == CompanyStage.MARKET_LEADERSHIP


def test_external_business_loops_and_lifecycle():
    """Verify 13 external loops and 15 lifecycle stages tracking."""
    loops = ExternalBusinessLoopsEngine()
    assert len(loops.loop_health) == 13
    assert loops.compute_systemic_health() == 1.0

    loops.update_loop_health("pricing", 0.5)
    assert loops.compute_systemic_health() < 1.0

    lifecycle = CustomerLifecycleEngine()
    assert len(lifecycle.stage_counts) == 15
    lifecycle.record_transition("awareness", 100)
    lifecycle.record_transition("activation", 25)
    funnel = lifecycle.get_conversion_funnel()
    assert funnel["awareness"] == 100
    assert funnel["activation"] == 25


def test_eos_engine_e2e_sensing_loop():
    """Verify end-to-end sensing, allocation, and tracking loop in the unified EOSEngine."""
    engine = EOSEngine()

    # Register some opportunities
    engine.opportunity_graph.add_opportunity("op_001", "Developer OS", 800000_00, ["developer", "os", "productivity"])

    # Register competitors
    engine.competitor_intel.register_competitor("Competitor A", 0.15, ["developer"])

    cell_1 = VentureCell(name="Venture A", namespace="v_a", expected_free_energy=3.0, risk=0.1)
    cell_2 = VentureCell(name="Venture B", namespace="v_b", expected_free_energy=1.5, risk=0.2)

    # Run continuous sensing cycle
    res = engine.run_continuous_sensing_cycle([cell_1, cell_2], total_budget_cents=50000_00)

    assert "world_state" in res
    assert res["market_uncertainty"] >= 0.0
    assert cell_1.allocated_capital_cents > 0
    assert cell_2.allocated_capital_cents > 0
    assert "systemic_loop_health" in res

    # Confirm trajectory is saved in memory
    matching_records = engine.memory.retrieve_matching_trajectories("allocated_capital", 100)
    assert len(matching_records) >= 1
