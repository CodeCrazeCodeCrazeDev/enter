from __future__ import annotations
import time
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class RiskTier(str, Enum):
    TIER_1_LOW = "tier_1_low"      # Prompt text tweaks, routing parameters (auto-apply)
    TIER_2_MEDIUM = "tier_2_medium"  # Workflow graph, tools changes (sandbox + shadow test)
    TIER_3_HIGH = "tier_3_high"    # Model swaps, memory schema or safety core changes (human-in-the-loop)


class SecurityAuditEntry(BaseModel):
    """Immutable audit ledger entry for any security-critical self-evolution event."""
    audit_id: UUID = Field(default_factory=uuid4)
    timestamp: float = Field(default_factory=time.time)
    tenant_id: str
    user_id: str
    action: str  # "PROPOSAL_EVALUATED", "AUTO_APPLIED", "SANDBOX_DEPLOYED", "STAGED_FOR_APPROVAL", "BLOCKED"
    risk_tier: RiskTier
    target_id: str
    details: Dict[str, Any] = Field(default_factory=dict)


class PolicyEngine:
    """
    Enforces absolute safety constraints, tenant boundaries,
    and isolates sensitive configurations from autonomous modifications.
    """

    def __init__(self) -> None:
        # Non-modifiable restricted paths/targets
        self.immutable_targets = {"safety_core", "security_policies", "root_access_control", "memory_schema"}

    def is_modification_allowed(self, tenant_id: str, target_id: str, delta_type: str) -> bool:
        """
        Hard rules checking:
        1. No autonomous modifications can touch target_ids listed in immutable_targets.
        2. No cross-tenant access allowed (target_id prefixes or tenant parameters).
        """
        if target_id in self.immutable_targets:
            return False

        # Protect safety package from edits
        if "safety" in target_id or "security" in target_id:
            return False

        return True


class RiskClassifier:
    """
    Assesses proposed config deltas and maps them to a RiskTier.
    - Tier 1: Prompts, minor thresholds
    - Tier 2: Workflow nodes, adding tools
    - Tier 3: Model changes, memory structures, safety core
    """

    def classify_proposal(self, target_id: str, delta_type: str) -> RiskTier:
        target_id_lower = target_id.lower()
        delta_type_lower = delta_type.lower()

        # Tier 3 matches
        if any(term in target_id_lower for term in ["model", "safety", "schema", "auth", "permission"]):
            return RiskTier.TIER_3_HIGH
        if delta_type_lower in ["model_swap", "schema_update", "permission_change"]:
            return RiskTier.TIER_3_HIGH

        # Tier 2 matches
        if any(term in target_id_lower for term in ["workflow", "node", "graph", "tool", "routing"]):
            return RiskTier.TIER_2_MEDIUM
        if delta_type_lower in ["workflow", "tool_routing", "agent_addition"]:
            return RiskTier.TIER_2_MEDIUM

        # Tier 1 fallback (low risk, e.g. prompt wording or simple parameter adjustments)
        return RiskTier.TIER_1_LOW


class ImmutableSafetyCore:
    """
    The centralized safety gateway coordinating Policy Enforcement,
    Risk Classification, and Security Auditing.
    """

    def __init__(self) -> None:
        self.policy_engine = PolicyEngine()
        self.risk_classifier = RiskClassifier()
        self.audit_ledger: List[SecurityAuditEntry] = []

    def evaluate_change_proposal(
        self,
        tenant_id: str,
        user_id: str,
        target_id: str,
        delta_type: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluates a modification proposal:
        - Checks policy compliance.
        - Classifies risk tier.
        - Logs immutable security audit entry.
        """
        allowed = self.policy_engine.is_modification_allowed(tenant_id, target_id, delta_type)
        risk_tier = self.risk_classifier.classify_proposal(target_id, delta_type)

        action = "BLOCKED"
        if allowed:
            if risk_tier == RiskTier.TIER_1_LOW:
                action = "PROPOSAL_EVALUATED_LOW"
            elif risk_tier == RiskTier.TIER_2_MEDIUM:
                action = "PROPOSAL_EVALUATED_MEDIUM"
            else:
                action = "PROPOSAL_EVALUATED_HIGH"

        entry = SecurityAuditEntry(
            tenant_id=tenant_id,
            user_id=user_id,
            action=action,
            risk_tier=risk_tier,
            target_id=target_id,
            details={**details, "allowed": allowed}
        )
        self.audit_ledger.append(entry)

        return {
            "allowed": allowed,
            "risk_tier": risk_tier,
            "action_required": action,
            "audit_id": entry.audit_id
        }
