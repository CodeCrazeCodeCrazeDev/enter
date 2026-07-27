"""Unit tests for Phase 2 Collective Intelligence Layer multi-mind reasoning."""

import pytest
from apodex.ai_eos.intelligence.collective import CollectiveIntelligenceEngine


def test_collective_intelligence_multi_mind_deliberation():
    """Verify that all six reasoning minds evaluate a proposal and resolve consensus."""
    engine = CollectiveIntelligenceEngine()

    proposal_clean = {
        "title": "GRPO-based Ad Layout optimization",
        "has_high_information_gain": True,
        "info_gain_estimate": 0.24,
        "violates_context_boundaries": False,
        "is_causally_validated": True,
        "estimated_npv_cents": 12000_00,  # $120.00
        "has_competitive_moat": True,
        "latency_ms": 120.0
    }

    report = engine.evaluate_with_multi_mind(proposal_clean)

    # Verify score aggregation
    assert report["proposal_title"] == "GRPO-based Ad Layout optimization"
    assert report["approved"] is True
    assert report["consensus_score"] >= 0.75

    # Check individual minds
    minds = report["individual_minds"]
    assert minds["bayesian"]["score"] == 0.90
    assert minds["symbolic"]["score"] == 0.95
    assert minds["causal"]["score"] == 0.85
    assert "Nash equilibrium" in minds["game_theoretic"]["log"]
