"""Unit tests for Phase 3 Research Economics Knowledge ROI calculations."""

import pytest
from apodex.ai_eos.domain.models import KnowledgeROI
from apodex.ai_eos.portfolio.manager import PortfolioOperatingSystem


def test_knowledge_roi_metrics():
    """Verify that PortfolioOperatingSystem computes accurate research accounting card."""
    pos = PortfolioOperatingSystem(initial_reserves_cents=10000_00)  # $10k

    # Run an allocation to increase total spent cents
    pos.allocate_portfolio_capital(cells=[], unresolved_uncertainty_score=0.30, total_allocation_cents=5000_00)
    # total_spent = $5,000, research_spend (30%) = $1,500.00

    card = pos.calculate_knowledge_roi(
        validated_theories_count=3,
        total_entropy_reduction=15.0,
        reusable_insights_count=5,
        future_ventures_count=2
    )

    assert isinstance(card, KnowledgeROI)
    # Cost per theory = 1500 / 3 = $500.00
    assert card.cost_per_validated_theory == pytest.approx(500.00)
    # Cost per entropy reduction = 1500 / 15 = $100.00
    assert card.cost_per_uncertainty_reduction == pytest.approx(100.00)
    # Cost per reusable insight = 1500 / 5 = $300.00
    assert card.cost_per_reusable_insight == pytest.approx(300.00)
    # Cost per future venture = 1500 / 2 = $750.00
    assert card.cost_per_future_venture_unlocked == pytest.approx(750.00)
