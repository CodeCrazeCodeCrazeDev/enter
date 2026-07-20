"""Unit tests for Phase 7 Governance, Architecture Governance & Meta-Governance."""

import pytest
from apodex.ai_eos.domain.models import Capability, SubsystemMaturity
from apodex.ai_eos.governance.gateway import GovernanceGateway


def test_standard_grc_gating():
    """Verify standard GRC policy gates handle safety, risk, and human approvals correctly."""
    gov = GovernanceGateway(initial_capital_limit_cents=1000000)

    # 1. Action within budget and low risk -> Approved
    result_clean = gov.evaluate_action(
        action_type="spend_marketing",
        risk_score=0.20,
        context={"budget_cents": 50000}
    )
    assert result_clean["cleared"] is True
    assert result_clean["human_required"] is False

    # 2. Action exceeding budget -> Blocked, human required
    result_overbudget = gov.evaluate_action(
        action_type="spend_marketing",
        risk_score=0.20,
        context={"budget_cents": 2000000}
    )
    assert result_overbudget["cleared"] is False
    assert result_overbudget["reason"] == "BUDGET_CEILING_EXCEEDED"
    assert result_overbudget["human_required"] is True

    # 3. Action with risk >= 0.50 -> Suspended, human required
    result_medium_risk = gov.evaluate_action(
        action_type="deploy_prompt",
        risk_score=0.65,
        context={"budget_cents": 1000}
    )
    assert result_medium_risk["cleared"] is False
    assert result_medium_risk["reason"] == "HUMAN_APPROVAL_REQUIRED"
    assert result_medium_risk["human_required"] is True


def test_architecture_governance_rules():
    """Verify that coupling rules and duplicate checks are strictly enforced."""
    gov = GovernanceGateway()

    # Create compliant capability
    cap_clean = Capability(
        capability_id="cap_clean",
        name="LinearForecaster",
        description="Linear regression on customer data",
        source="apodex/models/linear.py",
        origin="internal",
        dependencies=["cap_dep1"],
        owner="Executive",
        rollback_trigger="none",
        retirement_policy="none"
    )
    assert gov.evaluate_architecture_conformance(cap_clean) is True

    # Violates coupling: has >3 dependencies
    cap_coupled = Capability(
        capability_id="cap_coupled",
        name="SpaghettiModel",
        description="High coupling model",
        source="apodex/models/spaghetti.py",
        origin="internal",
        dependencies=["dep1", "dep2", "dep3", "dep4"],
        owner="Executive",
        rollback_trigger="none",
        retirement_policy="none"
    )
    assert gov.evaluate_architecture_conformance(cap_coupled) is False

    # Violates context boundaries: duplicates core or bypasses security
    cap_malicious = Capability(
        capability_id="cap_malicious",
        name="HackGate",
        description="Attempts to bypass_governance checks",
        source="apodex/models/bypass.py",
        origin="internal",
        dependencies=[],
        owner="Executive",
        rollback_trigger="none",
        retirement_policy="none"
    )
    assert gov.evaluate_architecture_conformance(cap_malicious) is False


def test_meta_governance_evolution():
    """Verify complexity budgets and tech debt calculations are evaluated correctly."""
    gov = GovernanceGateway()

    # Under budget change
    meta_clean = gov.evaluate_system_change(total_capabilities_count=20, code_added_lines=100)
    assert meta_clean["approved"] is True
    assert meta_clean["technical_debt_score"] == 0.0
    assert meta_clean["refactoring_scheduled"] is False

    # Extremely complex addition -> exceeds budget, triggers refactor schedule
    meta_complex = gov.evaluate_system_change(total_capabilities_count=120, code_added_lines=5000)
    assert meta_complex["approved"] is False
    assert meta_complex["technical_debt_score"] > 2.0
    assert meta_complex["refactoring_scheduled"] is True
