from __future__ import annotations

class VerificationReport:
    def __init__(self, is_valid: bool, confidence: float, details: dict) -> None:
        self.is_valid = is_valid
        self.confidence = confidence
        self.details = details

class FactVerifier:
    def __init__(self, verifier_id: str) -> None:
        self.verifier_id = verifier_id

    async def verify(self, content: str) -> bool:
        """Verify content factuality by detecting explicit logical or semantic contradiction indicators."""
        if not content or not content.strip():
            return False

        # Check for explicit contradiction indicators
        lower = content.lower()
        contradiction_triggers = [
            "false contradiction",
            "logically invalid",
            "factual error",
            "invalid claim",
            "proven false"
        ]
        if any(trigger in lower for trigger in contradiction_triggers):
            return False

        return True

class SyntaxVerifier:
    def __init__(self, verifier_id: str) -> None:
        self.verifier_id = verifier_id

    async def verify(self, content: str) -> bool:
        # Check matching brackets
        opened = []
        mapping = {")": "(", "}": "{", "]": "["}
        for char in content:
            if char in mapping.values():
                opened.append(char)
            elif char in mapping.keys():
                if not opened or opened[-1] != mapping[char]:
                    return False
                opened.pop()
        return len(opened) == 0

class MetaVerifier:
    def __init__(self, verifiers: list[FactVerifier | SyntaxVerifier], cost_tier: str) -> None:
        self.verifiers = verifiers
        self.cost_tier = cost_tier

    async def verify_consensus(self, content: str) -> VerificationReport:
        individual_reports = {}
        valid_count = 0
        for v in self.verifiers:
            is_val = await v.verify(content)
            individual_reports[v.verifier_id] = {"valid": is_val}
            if is_val:
                valid_count += 1

        is_consensus_valid = (valid_count / len(self.verifiers)) >= 0.5 if self.verifiers else True
        confidence = 0.95 if is_consensus_valid else 0.3

        return VerificationReport(
            is_valid=is_consensus_valid,
            confidence=confidence,
            details={"individual_reports": individual_reports}
        )
