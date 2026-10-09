"""Comprehensive unit, integration, and chaotic tests for the EOS Cognitive Engine.

Verifies all 14 systems and their interactions under standard and boundary scenarios.
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
    GTMSystemSimulator,
    StrategicPlanner,
    CapitalAllocationEngine,
    PortfolioManager,
    CompetitiveIntelligenceEngine,
    MoatAnalyzer,
    StrategicMoatEngine,
    FailurePredictionEngine,
    FailureModeMonitor,
    ReinventionEngine,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    CompanyGrowthStateMachine,
    CompanyStage,
    ExternalLoopType,
    EntrepreneurialMemory,
    EvaluationFramework,
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

    # 3. Add multiple supporting items to trigger promotion
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


def test_gtm_system_simulator():
    """Verify channel selection logic in GTMSystemSimulator."""
    gtm_sim = GTMSystemSimulator()

    # Self-serve low ACV -> PLG
    plg_recs = gtm_sim.evaluate_channel_fit(target_acv_cents=30_00, complexity_score=0.2, network_effects=False)
    assert plg_recs[0]["channel"] == "plg"

    # High ACV enterprise -> SLG
    slg_recs = gtm_sim.evaluate_channel_fit(target_acv_cents=50000_00, complexity_score=0.8, network_effects=True)
    assert slg_recs[0]["channel"] == "slg"


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
    """Verify feature parity and 7 powers moat score computations."""
    cie = CompetitiveIntelligenceEngine()
    cie.register_competitor("Competitor X", 0.40, ["sso", "analytics", "realtime"])
    cie.register_competitor("Competitor Y", 0.20, ["sso", "billing"])

    parity = cie.compute_feature_parity(["sso", "analytics"])
    assert parity == 0.5

    sme = StrategicMoatEngine()
    powers_result = sme.score_7_powers({
        "network_effects": 0.9,
        "switching_costs": 0.8,
        "scale_economies": 0.7,
        "counter_positioning": 0.85
    })
    assert powers_result["dominant_power"] == "network_effects"
    assert powers_result["composite_moat_score"] > 0.5


def test_failure_mode_monitor():
    """Verify failure mode audits and insolvency predictions."""
    fmm = FailureModeMonitor()
    prob_high = fmm.predict_insolvency_probability(burn_multiple=3.0, runway_months=3.0, ltv_to_cac=1.5)
    assert prob_high > 0.60

    alerts = fmm.audit_failure_modes({
        "survey_satisfaction_high": True,
        "usage_engagement": 0.1,
        "build_velocity": 0.9,
        "demand_signal": 0.1,
        "retention_curve_flattens": False,
        "monthly_spend": 100000
    })
    assert len(alerts) >= 3


def test_external_loops_and_lifecycle():
    """Verify External Business Loops and Customer Lifecycle funnel metrics."""
    loops_engine = ExternalBusinessLoopsEngine()
    fin_health = loops_engine.evaluate_loop_health(
        ExternalLoopType.FINANCIAL,
        {"burn_multiple": 3.0, "runway_months": 4.0}
    )
    assert fin_health["healthy"] is False

    lifecycle = CustomerLifecycleEngine()
    conversions = lifecycle.compute_funnel_efficiency({"awareness": 1000, "interest": 200, "consideration": 50})
    assert conversions["awareness_to_interest"] == 0.20
    assert conversions["interest_to_consideration"] == 0.25


def test_growth_stage_classifier():
    """Verify Company Growth Stage classifications."""
    sm = CompanyGrowthStateMachine()
    assert sm.classify_stage({"paying_customers": 0}) == CompanyStage.IDEA
    assert sm.classify_stage({"paying_customers": 5, "mrr_cents": 200_00}) == CompanyStage.VALIDATION
    assert sm.classify_stage({"paying_customers": 60, "mrr_cents": 5000_00}) == CompanyStage.PMF
    assert sm.classify_stage({"paying_customers": 500, "mrr_cents": 120000_00}) == CompanyStage.GROWTH
    assert sm.classify_stage({"third_party_developers": 150}) == CompanyStage.PLATFORM


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

    # Confirm trajectory is saved in memory
    matching_records = engine.memory.retrieve_matching_trajectories("allocated_capital", 100)
    assert len(matching_records) >= 1
