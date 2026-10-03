"""Tests for the First-Principles Entrepreneurial Operating System (EOS) specification & engine."""

from pathlib import Path
import pytest

from apodex.ai_eos.intelligence.eos_first_principles import (
    EOSEngineFirstPrinciples,
    EOSState,
    GrowthStage,
    JourneyStage,
    ExternalBusinessLoopsEngine,
    CustomerLifecycleEngine,
    GTMSystemSimulator,
    CompanyGrowthStateMachine,
    StrategicMoatEngine,
    FailureModeMonitor,
    EOSOpportunityDecisionTree,
)


def test_eos_specification_file_exists_and_complete():
    """Verify docs/architecture/ENTREPRENEURIAL_OPERATING_SYSTEM_SPEC.md exists and contains all 12 sections."""
    spec_path = Path("docs/architecture/ENTREPRENEURIAL_OPERATING_SYSTEM_SPEC.md")
    assert spec_path.exists(), "EOS specification document does not exist."

    content = spec_path.read_text()
    required_headings = [
        "## 0. Framing & Assumptions",
        "## 1. The Master Loop (Top-Level Architecture)",
        "## 2. Internal Cognitive Loops",
        "## 3. External Business Loops",
        "## 4. Customer Journey (Full Lifecycle)",
        "## 5. Go-to-Market System",
        "## 6. Company Growth System",
        "## 7. Strategic Thinking",
        "## 8. Failure Mode Analysis",
        "## 9. Scientific Foundations",
        "## 10. Integrated AI-Driven Entrepreneurial Research & Execution Operating System",
        "## 11. Explicit Limitations",
    ]

    for heading in required_headings:
        assert heading in content, f"Missing required heading: {heading}"


def test_external_business_loops_engine():
    """Verify all 13 feedback loops are evaluated and failure modes are detected."""
    engine = ExternalBusinessLoopsEngine()
    metrics = {
        "active_users": 2000,
        "retention_30d": 0.5,
        "nps": 10,  # low NPS triggers Product failure
        "cac_cents": 60000,  # high CAC triggers Marketing failure
        "win_rate": 0.10,  # low win rate triggers Sales failure
        "nrr": 0.85,  # low NRR triggers CS failure
        "brand_trust": 0.2,  # low brand trust triggers Brand failure
        "arpu_cents": 1500,  # low ARPU triggers Pricing failure
        "k_factor": 0.02,  # low k-factor triggers Referral failure
        "decision_latency_days": 20.0,  # high latency triggers Data failure
        "burn_multiple": 4.0,  # high burn triggers Financial failure
        "regretted_attrition": 0.25,  # high attrition triggers Hiring failure
        "enps": -10,  # negative eNPS triggers Culture failure
        "experiments_run": 20,
        "hit_rate": 0.02,  # low hit rate triggers Innovation failure
        "feature_parity": 0.98,  # high parity triggers Comp Intel failure
    }

    loop_results = engine.evaluate_all_loops(metrics)
    assert len(loop_results) == 13

    # Ensure failure modes are properly flagged
    assert loop_results["Product"].failure_mode_detected is not None
    assert loop_results["Marketing"].failure_mode_detected is not None
    assert loop_results["Sales"].failure_mode_detected is not None
    assert loop_results["Financial"].failure_mode_detected is not None


def test_customer_lifecycle_engine():
    """Verify Customer Lifecycle bottleneck detection."""
    engine = CustomerLifecycleEngine()
    conversions = {
        JourneyStage.AWARENESS: 0.8,
        JourneyStage.INTEREST: 0.5,
        JourneyStage.ACTIVATION: 0.10,  # Primary bottleneck
        JourneyStage.RETENTION: 0.6,
    }

    res = engine.evaluate_funnel(conversions)
    assert res["primary_bottleneck_stage"] == JourneyStage.ACTIVATION.value
    assert res["lowest_stage_conversion"] == 0.10


def test_gtm_system_simulator():
    """Verify GTM channel motion recommendations."""
    sim = GTMSystemSimulator()

    # Enterprise motion
    ent_res = sim.evaluate_channel_fit(acv_cents=100000_00, complexity_score=0.8, network_density=0.2)
    assert "Sales-Led Growth (SLG) / Enterprise" in ent_res["recommended_gtm_motions"]

    # PLG motion
    plg_res = sim.evaluate_channel_fit(acv_cents=1000_00, complexity_score=0.1, network_density=0.1)
    assert "Product-Led Growth (PLG) / Self-Serve" in plg_res["recommended_gtm_motions"]


def test_company_growth_state_machine():
    """Verify classification across growth stages and binding constraints."""
    sm = CompanyGrowthStateMachine()

    stage_idea, constraint_idea = sm.classify_stage({"paying_customers": 0})
    assert stage_idea == GrowthStage.IDEA
    assert constraint_idea == "Binding constraint: Founder time"

    stage_pmf, constraint_pmf = sm.classify_stage({"paying_customers": 50, "retention_flattened": True})
    assert stage_pmf == GrowthStage.PMF
    assert constraint_pmf == "Binding constraint: Team bandwidth"

    stage_scale, constraint_scale = sm.classify_stage({
        "paying_customers": 1000,
        "retention_flattened": True,
        "revenue_cents": 15000000_00,
        "rule_of_40": 0.45
    })
    assert stage_scale == GrowthStage.SCALE
    assert constraint_scale == "Binding constraint: Org coordination cost"


def test_eos_opportunity_decision_tree():
    """Verify Section 10.2 decision tree logic."""
    tree = EOSOpportunityDecisionTree()

    # Noise anomaly should be discarded
    pursue_noise, reason_noise = tree.evaluate_pursuit(
        is_structural_anomaly=False,
        is_reversible_decision=True,
        multi_source_confidence=0.5,
        cheap_test_available=True,
        cheap_test_passed=True,
        expected_value_positive=True,
        structural_advantage=True
    )
    assert not pursue_noise
    assert "Discard" in reason_noise

    # Valid structural anomaly with passing cheap test and structural advantage
    pursue_valid, reason_valid = tree.evaluate_pursuit(
        is_structural_anomaly=True,
        is_reversible_decision=True,
        multi_source_confidence=0.9,
        cheap_test_available=True,
        cheap_test_passed=True,
        expected_value_positive=True,
        structural_advantage=True
    )
    assert pursue_valid
    assert "Commit Resources" in reason_valid


def test_eos_engine_first_principles_master_cycle():
    """Verify end-to-end master cycle execution of EOSEngineFirstPrinciples."""
    engine = EOSEngineFirstPrinciples()
    result = engine.run_master_loop_cycle()

    assert result["system_state"] == EOSState.SENSING.value
    assert "growth_stage" in result
    assert "binding_constraint" in result
    assert len(result["business_loops"]) == 13
    assert "gtm_evaluation" in result
    assert "moat_durability" in result
