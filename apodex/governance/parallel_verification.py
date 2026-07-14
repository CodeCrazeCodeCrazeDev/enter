from __future__ import annotations
from typing import List, Dict, Any, Optional

from apodex.common.text import is_balanced_brackets


class VerificationReport:
    """Consolidated outcome of the parallel verifiers."""

    def __init__(self, is_valid: bool, confidence: float, details: Dict[str, Any]) -> None:
        self.is_valid = is_valid
        self.confidence = confidence
        self.details = details


class FactVerifier:
    def __init__(self, verifier_id: str) -> None:
        self.verifier_id = verifier_id

    async def verify(self, content: str) -> Dict[str, Any]:
        """Verify content factual accuracy. Simple heuristic check for testing."""
        # Simple heuristic: contradictions or lack of balance reduces validity
        is_valid = "contradiction" not in content.lower()
        return {"valid": is_valid, "confidence": 0.95 if is_valid else 0.3}


class SyntaxVerifier:
    def __init__(self, verifier_id: str) -> None:
        self.verifier_id = verifier_id

    async def verify(self, content: str) -> Dict[str, Any]:
        """Verify syntax validity (e.g. matched brackets/parentheses)."""
        return {"valid": is_balanced_brackets(content), "confidence": 1.0}


class MetaVerifier:
    """Asynchronously evaluates verification reports in parallel and resolves a consensus score."""

    def __init__(self, verifiers: List[Any]) -> None:
        self.verifiers = verifiers

    async def verify_consensus(self, content: str) -> VerificationReport:
        import asyncio

        # Gather verifications concurrently
        tasks = [v.verify(content) for v in self.verifiers]
        individual_results = await asyncio.gather(*tasks)

        reports_map = {}
        valid_votes = 0
        total_confidence = 0.0

        for verifier, res in zip(self.verifiers, individual_results):
            v_id = getattr(verifier, "verifier_id", str(id(verifier)))
            reports_map[v_id] = res
            if res["valid"]:
                valid_votes += 1
            total_confidence += res["confidence"]

        # Consensus logic: valid if majority are valid (>= 50%)
        is_valid = (valid_votes / len(self.verifiers)) >= 0.5 if self.verifiers else False
        confidence = total_confidence / len(self.verifiers) if self.verifiers else 0.0

        return VerificationReport(
            is_valid=is_valid,
            confidence=confidence,
            details={"individual_reports": reports_map}
        )
