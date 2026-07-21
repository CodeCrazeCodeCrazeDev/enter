"""Unit tests for Phase 4 Entrepreneurial Intelligence System (EIS) strategic decisions."""

import pytest
from apodex.ai_eos.domain.models import Theory
from apodex.ai_eos.intelligence.decision_engine import EntrepreneurialIntelligenceSystem


def test_meta_economic_decision_framework():
    """Verify that the optimal commercialization form is selected based on capital/confidence."""
    eis = EntrepreneurialIntelligenceSystem()

    theory_strong = Theory(
        theory_id="theory_strong",
        statement="Theory of Top Banner Conversion",
        constituent_hypotheses=["hyp1"],
        predictive_scope=["untested1"],
        confidence=0.85
    )

    # High capital and confidence -> BUILD_VENTURE
    form_build = eis.evaluate_opportunity_form(theory_strong, available_capital_cents=50000_00)
    assert form_build == "BUILD_VENTURE"

    # Low capital and confidence -> LICENSE_IP
    form_license = eis.evaluate_opportunity_form(theory_strong, available_capital_cents=5000_00)
    assert form_license == "LICENSE_IP"

    theory_mod = Theory(
        theory_id="theory_mod",
        statement="Theory of Social Media Engagement",
        constituent_hypotheses=["hyp2"],
        predictive_scope=["untested2"],
        confidence=0.65
    )
    # Moderate confidence with predictive scope -> OPEN_SOURCE
    form_os = eis.evaluate_opportunity_form(theory_mod, available_capital_cents=5000_00)
    assert form_os == "OPEN_SOURCE"


def test_recursive_scientific_organization():
    """Verify that high forecasting errors trigger proposals for specialized agent spawning."""
    eis = EntrepreneurialIntelligenceSystem()

    # Small error -> no proposals
    proposals_clean = eis.recommend_capability_refinements(forecasting_errors_ratio=0.04)
    assert len(proposals_clean) == 0

    # Elevated error -> spawn pricing specialist
    proposals_elevated = eis.recommend_capability_refinements(forecasting_errors_ratio=0.18)
    assert "SPAWN_PRICING_SPECIALIST_AGENT" in proposals_elevated

    # Extreme error -> split generalist
    proposals_extreme = eis.recommend_capability_refinements(forecasting_errors_ratio=0.35)
    assert "SPAWN_PRICING_SPECIALIST_AGENT" in proposals_extreme
    assert "SPLIT_GENERALIST_INTO_PEER_REVIEW_TRIAD" in proposals_extreme
