"""Unit tests for Phase 3 Epistemic Risk queries and Calibration Audits."""

import pytest
from uuid import uuid4
from apodex.ai_eos.domain.models import Hypothesis
from apodex.ai_eos.active_inference.engine import ExecutiveOptimizer


def test_epistemic_risk_queries():
    """Verify that unproven high-impact nodes and deep dependency chains are correctly identified."""
    opt = ExecutiveOptimizer()

    # 1. High impact, low evidence flag
    h_risky = Hypothesis(
        statement="A risky unproven assumption",
        domain="onboarding",
        supporting_evidence=[],
        contradicting_evidence=[],
        downstream_decisions=["dec_1", "dec_2", "dec_3"]  # High impact (>= 3 decisions)
    )

    h_safe = Hypothesis(
        statement="A safe proven assumption",
        domain="onboarding",
        supporting_evidence=["ev_1", "ev_2"],
        downstream_decisions=["dec_4"]
    )

    flagged = opt.flag_high_impact_low_evidence([h_risky, h_safe])
    assert len(flagged) == 1
    assert flagged[0].statement == "A risky unproven assumption"
    assert flagged[0].high_impact_low_evidence_flag is True

    # 2. Ignorance Registry
    registry = opt.ignorance_registry([h_risky, h_safe])
    assert str(h_risky.hypothesis_id) in registry["high_impact_low_evidence"]
    assert "onboarding" in registry["sparse_domains"]


def test_recursive_assumption_depth():
    """Verify recursive calculation of dependent unproven hypothesis chain depth."""
    opt = ExecutiveOptimizer()

    h_leaf = Hypothesis(statement="Leaf node", domain="ads", dependent_hypotheses=[])
    h_mid = Hypothesis(statement="Middle node", domain="ads", dependent_hypotheses=[str(h_leaf.hypothesis_id)])
    h_root = Hypothesis(statement="Root node", domain="ads", dependent_hypotheses=[str(h_mid.hypothesis_id)])

    kos_dict = {
        str(h_leaf.hypothesis_id): h_leaf,
        str(h_mid.hypothesis_id): h_mid,
        str(h_root.hypothesis_id): h_root
    }

    # Root -> Mid -> Leaf (depth of root is 2)
    depth = opt.assumption_depth(h_root, kos_dict)
    assert depth == 2


def test_calibration_audit_thresholds():
    """Verify that calibration audits correctly calculate deviations and raise warnings upon mismatch."""
    opt = ExecutiveOptimizer()

    # Record simulated strategic choices with high predicted confidence but low actual success
    opt.calibration_trail = [
        {"confidence": 0.85, "realized": False},
        {"confidence": 0.82, "realized": False},
        {"confidence": 0.88, "realized": False}
    ]

    deviations = opt.audit_calibration()

    # 80-90 bucket midpoint is 0.85. Realized success rate is 0%. Deviation is 0.85 (which is > 0.15 limit!)
    assert deviations["80-90"]["deviation"] == pytest.approx(0.85)
