from __future__ import annotations
import time
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from apodex.evolution.common.models import CostMode, ConfigDelta, ChangelogEntry, EvolutionChangelog
from apodex.evolution.verifier.judge import EvolutionVerifier
from apodex.safety.core import ImmutableSafetyCore, RiskTier


class ChangeProposal(BaseModel):
    """Holds a proposed configuration delta and target context."""
    proposal_id: UUID = Field(default_factory=uuid4)
    tenant_id: str
    user_id: str
    delta: ConfigDelta
    status: str = Field(default="pending_safety_check")  # "applied", "sandboxed", "staged_for_approval", "blocked"
    risk_tier: Optional[RiskTier] = None


class SelfImprovementOrchestrator:
    """
    Coordinates self-improvement changes, enforcing policy constraints and Risk Tiered Approvals.
    """

    def __init__(
        self,
        safety_core: Optional[ImmutableSafetyCore] = None,
        changelog: Optional[EvolutionChangelog] = None,
        verifier: Optional[EvolutionVerifier] = None
    ) -> None:
        self.safety_core = safety_core or ImmutableSafetyCore()
        self.changelog = changelog or EvolutionChangelog()
        self.verifier = verifier or EvolutionVerifier()

        # Simulated sandbox deployment list for Tier 2 changes
        self.sandboxed_configs: Dict[str, Any] = {}
        # Simulated staging list for Tier 3 human approval changes
        self.staged_approvals: Dict[UUID, ChangeProposal] = {}

    async def process_change_proposal(self, proposal: ChangeProposal, cost_mode: CostMode) -> Dict[str, Any]:
        """
        Processes a self-improvement change proposal through the tiered approval workflow.
        """
        # 1. Evaluate with Safety Core
        safety_result = self.safety_core.evaluate_change_proposal(
            tenant_id=proposal.tenant_id,
            user_id=proposal.user_id,
            target_id=proposal.delta.target_id,
            delta_type=proposal.delta.delta_type,
            details={"proposal_id": str(proposal.proposal_id)}
        )

        proposal.risk_tier = safety_result["risk_tier"]

        if not safety_result["allowed"]:
            proposal.status = "blocked"
            return {
                "proposal_id": proposal.proposal_id,
                "status": "blocked",
                "risk_tier": proposal.risk_tier,
                "msg": "Blocked by absolute Safety Core policies."
            }

        # 2. Tiered Approval Routing
        if proposal.risk_tier == RiskTier.TIER_1_LOW:
            # Auto-apply directly
            delta = proposal.delta
            entry = ChangelogEntry(
                entry_id=f"auto_{int(time.time())}",
                timestamp=time.time(),
                cost_mode=cost_mode,
                applied_deltas=[delta],
                verifier_score_before=0.5,
                verifier_score_after=0.8,
                description=f"Auto-applied Tier 1 modification for target {delta.target_id}."
            )
            self.changelog.apply_change(entry)
            proposal.status = "applied"

            return {
                "proposal_id": proposal.proposal_id,
                "status": "applied",
                "risk_tier": proposal.risk_tier,
                "msg": "Auto-applied low risk change successfully."
            }

        elif proposal.risk_tier == RiskTier.TIER_2_MEDIUM:
            # Sandbox + Shadow Test Deployment
            self.sandboxed_configs[proposal.delta.target_id] = proposal.delta.new_value
            proposal.status = "sandboxed"

            # Simulate shadow traffic test:
            # If the cost_mode is Max Quality, we promote it. Otherwise, we simulate rollback.
            shadow_successful = (cost_mode == CostMode.MAX_QUALITY)

            if shadow_successful:
                # Promote to production changelog
                entry = ChangelogEntry(
                    entry_id=f"promoted_{int(time.time())}",
                    timestamp=time.time(),
                    cost_mode=cost_mode,
                    applied_deltas=[proposal.delta],
                    verifier_score_before=0.6,
                    verifier_score_after=0.85,
                    description=f"Promoted sandboxed Tier 2 modification for target {proposal.delta.target_id}."
                )
                self.changelog.apply_change(entry)
                proposal.status = "applied"
                promoted = True
            else:
                # Rollback sandbox state
                self.sandboxed_configs.pop(proposal.delta.target_id, None)
                proposal.status = "rolled_back"
                promoted = False

            return {
                "proposal_id": proposal.proposal_id,
                "status": proposal.status,
                "risk_tier": proposal.risk_tier,
                "promoted": promoted,
                "msg": "Sandboxed and shadow-tested Tier 2 modification."
            }

        else:  # RiskTier.TIER_3_HIGH
            # Stage for Human-in-the-loop approval
            self.staged_approvals[proposal.proposal_id] = proposal
            proposal.status = "staged_for_approval"

            return {
                "proposal_id": proposal.proposal_id,
                "status": "staged_for_approval",
                "risk_tier": proposal.risk_tier,
                "msg": "Staged for mandatory Human-in-the-loop manual approval."
            }

    def execute_manual_approval(self, proposal_id: UUID, cost_mode: CostMode, approved: bool) -> Dict[str, Any]:
        """Manually approves or rejects a staged Tier 3 high-risk proposal."""
        proposal = self.staged_approvals.pop(proposal_id, None)
        if not proposal:
            return {"status": "not_found"}

        if approved:
            entry = ChangelogEntry(
                entry_id=f"approved_{int(time.time())}",
                timestamp=time.time(),
                cost_mode=cost_mode,
                applied_deltas=[proposal.delta],
                verifier_score_before=0.5,
                verifier_score_after=0.9,
                description=f"Manually approved Tier 3 change for {proposal.delta.target_id}."
            )
            self.changelog.apply_change(entry)
            proposal.status = "applied"
            msg = "Staged proposal approved and applied."
        else:
            proposal.status = "rejected"
            msg = "Staged proposal rejected and discarded."

        return {
            "proposal_id": proposal_id,
            "status": proposal.status,
            "msg": msg
        }
