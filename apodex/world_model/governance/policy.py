from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class PolicyRule(BaseModel):
    """A single regulatory, ethical, or safety constraint constraint rule."""
    rule_id: str
    category: str  # "ETHICS", "LEGAL", "BRAND", "COMPLIANCE"
    description: str
    is_active: bool = True
    severity: str = "HIGH"  # "LOW", "MEDIUM", "HIGH", "CRITICAL"


class PolicyEnforcementFrame(BaseModel):
    """Collection of active policies deployed for a given tenant."""
    tenant_id: str
    rules: List[PolicyRule] = Field(default_factory=list)

    def find_rule(self, rule_id: str) -> Optional[PolicyRule]:
        """Look up a rule in the frame."""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
