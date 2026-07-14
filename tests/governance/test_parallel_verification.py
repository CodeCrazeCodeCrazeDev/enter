from __future__ import annotations

from apodex.governance.parallel_verification import (
    FactVerifier,
    MetaVerifier,
    SyntaxVerifier,
    VerificationReport,
)


async def test_fact_verifier_valid_content():
    res = await FactVerifier("f1").verify("balanced statement")
    assert res == {"valid": True, "confidence": 0.95}


async def test_fact_verifier_detects_contradiction():
    res = await FactVerifier("f1").verify("this is a Contradiction here")
    assert res["valid"] is False
    assert res["confidence"] == 0.3


async def test_syntax_verifier_balanced_brackets():
    res = await SyntaxVerifier("s1").verify("(a[b]{c})")
    assert res == {"valid": True, "confidence": 1.0}


async def test_syntax_verifier_mismatched_bracket():
    res = await SyntaxVerifier("s1").verify("(a]")
    assert res["valid"] is False


async def test_syntax_verifier_unclosed_bracket():
    res = await SyntaxVerifier("s1").verify("(a(b)")
    assert res["valid"] is False


async def test_syntax_verifier_closing_without_opening():
    res = await SyntaxVerifier("s1").verify("a)")
    assert res["valid"] is False


async def test_meta_verifier_consensus_all_valid():
    verifiers = [FactVerifier("f1"), SyntaxVerifier("s1")]
    report = await MetaVerifier(verifiers).verify_consensus("clean (content)")
    assert isinstance(report, VerificationReport)
    assert report.is_valid is True
    assert report.confidence == (0.95 + 1.0) / 2
    assert set(report.details["individual_reports"].keys()) == {"f1", "s1"}


async def test_meta_verifier_consensus_majority_invalid():
    # both verifiers fail: contradiction + mismatched brackets
    verifiers = [FactVerifier("f1"), SyntaxVerifier("s1")]
    report = await MetaVerifier(verifiers).verify_consensus("contradiction (]")
    assert report.is_valid is False


async def test_meta_verifier_empty_verifiers():
    report = await MetaVerifier([]).verify_consensus("anything")
    assert report.is_valid is False
    assert report.confidence == 0.0


async def test_meta_verifier_tie_is_valid():
    # one valid, one invalid -> 0.5 ratio >= 0.5 -> valid
    verifiers = [FactVerifier("f1"), SyntaxVerifier("s1")]
    report = await MetaVerifier(verifiers).verify_consensus("clean text (]")
    assert report.is_valid is True
