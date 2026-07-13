from __future__ import annotations
from typing import Dict, List
from apodex.world_model.governance.policy import PolicyEnforcementFrame


class ComplianceAuditor:
    """Enforces rules inside PolicyEnforcementFrame, screening creative concepts and parameters."""

    def __init__(self, frame: PolicyEnforcementFrame) -> None:
        self.frame = frame

    async def audit_concept(self, prompt: str, metadata: dict) -> List[str]:
        """Verify prompt against active ethical and brand regulations."""
        violations = []
        for rule in self.frame.rules:
            if not rule.is_active:
                continue
            # Basic demo verification: check if keyword contains banned concepts
            if rule.rule_id == "RULE_ETH_01" and "deceive" in prompt.lower():
                violations.append(f"Violation of {rule.rule_id}: {rule.description}")
            if rule.rule_id == "RULE_BRAND_01" and "competitor_slander" in prompt.lower():
                violations.append(f"Violation of {rule.rule_id}: {rule.description}")
        return violations
