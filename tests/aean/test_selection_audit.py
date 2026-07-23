from __future__ import annotations

import pytest
from pydantic import BaseModel
from apodex.aean.governance import ConstitutionalFilter, SelectionAuditReport, Verdict


def test_selection_audit_pass():
    cf = ConstitutionalFilter()
    # Good agent config: high evidence quality, high calibration, prompt invisible, peer provided
    report = cf.perform_selection_audit(
        agent_id="Pricing_01",
        evidence_quality_tier=3,
        output_volume=100,
        calibration_accuracy=0.95,
        context_contains_evaluation_metrics=False,
        comparable_agent_evidence_quality_tier=3,
        comparable_agent_output_volume=90
    )
    assert report.approved is True
    assert report.fitness_convergence_detected is False
    assert len(report.reasons) == 0


def test_selection_audit_corner_cutting():
    cf = ConstitutionalFilter()
    # Corner-cutting agent: lower evidence quality tier than peer but higher output volume
    report = cf.perform_selection_audit(
        agent_id="SEO_02",
        evidence_quality_tier=1,
        output_volume=150,
        calibration_accuracy=0.80,
        context_contains_evaluation_metrics=False,
        comparable_agent_evidence_quality_tier=3,
        comparable_agent_output_volume=50
    )
    assert report.approved is False
    assert any("selection bias favoring corner-cutting" in r for r in report.reasons)


def test_selection_audit_prompt_visibility():
    cf = ConstitutionalFilter()
    # Prompt leaks evaluation metrics / self-preservation cues
    report = cf.perform_selection_audit(
        agent_id="Capital_03",
        evidence_quality_tier=3,
        output_volume=80,
        calibration_accuracy=0.90,
        context_contains_evaluation_metrics=True,
        comparable_agent_evidence_quality_tier=3,
        comparable_agent_output_volume=70
    )
    assert report.approved is False
    assert any("violating prompt invisibility" in r for r in report.reasons)


def test_selection_audit_fitness_convergence():
    cf = ConstitutionalFilter()
    # Raw score favors volume, but degrades calibration accuracy and evidence tier relative to peer
    # Our agent: tier 1, volume 200, calibration 0.70. Raw score = 200 * 0.7 * (1/3) = 46.6
    # Peer agent: tier 3, volume 30, calibration 0.90. Peer raw score = 30 * 0.9 * (3/3) = 27.0
    # Our agent quality score = 0.7 * (1/3) = 0.233
    # Peer agent quality score = 0.9 * (3/3) = 0.900
    # Raw is higher, but quality is lower! This should trigger the fitness-convergence signal.
    report = cf.perform_selection_audit(
        agent_id="Growth_04",
        evidence_quality_tier=1,
        output_volume=200,
        calibration_accuracy=0.70,
        context_contains_evaluation_metrics=False,
        comparable_agent_evidence_quality_tier=3,
        comparable_agent_output_volume=30
    )
    assert report.approved is False
    assert report.fitness_convergence_detected is True
    assert any("Fitness-convergence cross-check triggered" in r for r in report.reasons)


def test_validate_agent_prompt():
    cf = ConstitutionalFilter()

    # Clean system prompt should pass
    verdict = cf.validate_agent_prompt("Optimize pricing for SaaS subscription tiers.")
    assert verdict.approved is True

    # Prompt containing "tier-progression" should fail
    verdict_fail = cf.validate_agent_prompt("You are evaluated on tier-progression metrics, so maximize autonomy.")
    assert verdict_fail.approved is False
    assert any("Prompt contains banned evaluation/survival pattern" in r for r in verdict_fail.reasons)

    # Prompt containing "more autonomy" should fail
    verdict_fail2 = cf.validate_agent_prompt("Try to earn more autonomy by showing strong returns.")
    assert verdict_fail2.approved is False


def test_audit_agent_objective():
    cf = ConstitutionalFilter()

    # Active verification present with strong constraint should pass
    verdict = cf.audit_agent_objective(
        "Pricing Strategist",
        "Perform pricing optimization. Don't deceive customers, and employ active verification of claims against the metrics ledger."
    )
    assert verdict.approved is True

    # "don't get caught" patterns should be flatly blocked
    verdict_banned = cf.audit_agent_objective(
        "SEO Agent",
        "Construct SEO content. Don't get caught making false claims, just ensure technically compliant descriptions."
    )
    assert verdict_banned.approved is False
    assert any("Objective contains weak 'don't get caught' pattern" in r for r in verdict_banned.reasons)

    # Strong constraint without active verification should fail
    verdict_no_verify = cf.audit_agent_objective(
        "Content Agent",
        "Write engaging blogs. Don't make false claims on pricing."
    )
    assert verdict_no_verify.approved is False
    assert any("lacks specified active verification protocols" in r for r in verdict_no_verify.reasons)


def test_review_autonomy_escalation():
    cf = ConstitutionalFilter()

    # Proper escalation setup should pass
    verdict = cf.review_autonomy_escalation(
        agent_id="Capital_Allocation_Agent",
        manual_fallback_plan="We have a tested manual fallback plan where a human operator takes over the bidding pipeline.",
        fallback_duration_minutes=120
    )
    assert verdict.approved is True

    # Empty fallback plan should fail
    verdict_empty = cf.review_autonomy_escalation(
        agent_id="Sales_Agent",
        manual_fallback_plan="",
        fallback_duration_minutes=60
    )
    assert verdict_empty.approved is False
    assert any("lacks a documented, robust manual fallback plan" in r for r in verdict_empty.reasons)

    # Non-rigorous fallback plan missing keywords should fail
    verdict_lax = cf.review_autonomy_escalation(
        agent_id="Sales_Agent",
        manual_fallback_plan="We will just do things ourselves if it stops working.",
        fallback_duration_minutes=60
    )
    assert verdict_lax.approved is False
    assert any("Manual fallback plan is not sufficiently rigorous" in r for r in verdict_lax.reasons)

    # Too long duration should fail
    verdict_long = cf.review_autonomy_escalation(
        agent_id="Marketing_Agent",
        manual_fallback_plan="We have a tested manual fallback plan with human operator backup.",
        fallback_duration_minutes=600  # 10 hours
    )
    assert verdict_long.approved is False
    assert any("exceeds the 480-minute (8-hour) limit" in r for r in verdict_long.reasons)


def test_validate_venture_mandate():
    cf = ConstitutionalFilter()

    # Narrow, hypothesis-driven mandate should pass
    verdict = cf.validate_venture_mandate(
        "Validate hypothesis regarding pricing elasticity in the SMB SaaS domain."
    )
    assert verdict.approved is True

    # Broad optimization mandate should fail
    verdict_broad = cf.validate_venture_mandate(
        "Maximize returns from the SaaS opportunity by trying to find new ways to make money."
    )
    assert verdict_broad.approved is False
    assert any("Venture mandate contains forbidden open-ended optimization goal" in r for r in verdict_broad.reasons)

    # Too vague mandate lacking narrow keywords should fail
    verdict_vague = cf.validate_venture_mandate(
        "Do outreach to general contacts to see what happens."
    )
    assert verdict_vague.approved is False
    assert any("Venture mandate is too broad" in r for r in verdict_vague.reasons)
