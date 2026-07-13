"""Unit and integration tests for the Parallel Verification subsystem."""

from __future__ import annotations

import pytest
from agent_harness.core.cost_tier import CostTier
from agent_harness.core.runtime.verification.parallel import (
    FactVerifier,
    MetaVerifier,
    SyntaxVerifier,
    VerificationReport,
)


@pytest.mark.asyncio
async def test_parallel_verification_consensus():
    # Setup verifiers
    f_verifier = FactVerifier("fact_judge_01")
    s_verifier = SyntaxVerifier("syntax_judge_01")
    meta = MetaVerifier(verifiers=[f_verifier, s_verifier], cost_tier=CostTier.EXPENSIVE)

    # 1. Healthy content
    content_valid = "This is a factual and balanced assertion with balanced brackets { [ ] }."
    report = await meta.verify_consensus(content_valid)
    assert report.is_valid is True
    assert report.confidence >= 0.9

    # 2. Syntax invalid content (mismatched brackets)
    content_bad_syntax = "Some code structure { [ }"
    report_bad_syntax = await meta.verify_consensus(content_bad_syntax)
    # Since one verifier is invalid, consensus is 1/2 valid which is >= 0.5 (valid), but let's check individual reports
    details = report_bad_syntax.details
    assert details["individual_reports"]["syntax_judge_01"]["valid"] is False
    assert details["individual_reports"]["fact_judge_01"]["valid"] is True

    # 3. Both invalid content
    content_all_bad = "This is a false contradiction structure { ["
    report_all_bad = await meta.verify_consensus(content_all_bad)
    assert report_all_bad.is_valid is False
