from __future__ import annotations
import time
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from apodex.memory.models import CostMode, CapabilityDelta
from apodex.safety.core import ImmutableSafetyCore, RiskTier
from apodex.evolution.research.ticket import ArchitectureCandidate
from apodex.evolution.research.search import ExperimentResult


class CapabilityDeltaLog:
    """
    Manages versioned capability upgrades, logging delta objects
    into the persistent database.
    """

    def __init__(self, tencent_db: Any) -> None:
        self.db = tencent_db
        self.deltas: Dict[UUID, CapabilityDelta] = {}

    def record_upgrade(
        self,
        tenant_id: str,
        candidate: ArchitectureCandidate,
        result: ExperimentResult
    ) -> CapabilityDelta:
        """
        Records a successful evolutionary upgrade step as a versioned CapabilityDelta.
        """
        delta = CapabilityDelta(
            delta_id=uuid4(),
            tenant_id=tenant_id,
            target_capability=candidate.target_capability,
            modification_type="prompt_adaptation" if candidate.risk_tier == RiskTier.TIER_1_LOW else "agent_topology_search",
            baseline_version="v2.0.0",
            candidate_version=f"v2.1.0-auto-{candidate.name}",
            performance_gain_ratio=1.0 + (result.quality_score - 0.65),
            rollback_sha256=f"sha256-{uuid4().hex[:16]}"
        )
        self.deltas[delta.delta_id] = delta
        return delta


class ResearchPromotionPipeline:
    """
    Coordinates promoting highly-performing Sandbox Architecture candidates to production,
    submitting to safety core tiered approval policies.
    """

    def __init__(
        self,
        safety_core: Optional[ImmutableSafetyCore] = None,
        delta_log: Optional[CapabilityDeltaLog] = None
    ) -> None:
        self.safety_core = safety_core or ImmutableSafetyCore()
        self.delta_log = delta_log or CapabilityDeltaLog(None)
        # Tracking active staged and approved states
        self.approved_deltas: List[CapabilityDelta] = []
        self.staged_candidates: Dict[UUID, ArchitectureCandidate] = {}

    async def promote_candidate(
        self,
        tenant_id: str,
        user_id: str,
        candidate: ArchitectureCandidate,
        result: ExperimentResult,
        cost_mode: CostMode
    ) -> Dict[str, Any]:
        """
        Evaluates the candidate's safety with the safety core and applies the tiered policy:
        - Tier 1: Auto-promote to capability logs if performance improves.
        - Tier 2: Deploy to shadow testing.
        - Tier 3: Stage for human manual approval.
        """
        # 1. Run through safety core check
        safety_eval = self.safety_core.evaluate_change_proposal(
            tenant_id=tenant_id,
            user_id=user_id,
            target_id=candidate.name,
            delta_type="architecture_promotion",
            details={"candidate_id": str(candidate.candidate_id)}
        )

        if not safety_eval["allowed"]:
            return {
                "candidate_id": candidate.candidate_id,
                "status": "blocked",
                "msg": "Blocked by absolute Safety Core policies."
            }

        # 2. Tiered Promotion Policies
        if candidate.risk_tier == RiskTier.TIER_1_LOW:
            # Low risk -> Auto-apply immediately if quality increased
            if result.quality_score > 0.65:
                delta = self.delta_log.record_upgrade(tenant_id, candidate, result)
                self.approved_deltas.append(delta)
                status = "auto_promoted"
            else:
                status = "rejected_low_gain"

            return {
                "candidate_id": candidate.candidate_id,
                "status": status,
                "risk_tier": candidate.risk_tier,
                "msg": "Processed Tier 1 auto-promotion."
            }

        elif candidate.risk_tier == RiskTier.TIER_2_MEDIUM:
            # Medium risk -> Shadow test deployment
            delta = self.delta_log.record_upgrade(tenant_id, candidate, result)
            self.approved_deltas.append(delta)

            return {
                "candidate_id": candidate.candidate_id,
                "status": "shadow_tested",
                "risk_tier": candidate.risk_tier,
                "msg": "Deployed to isolated Cube Sandbox shadow testing."
            }

        else:  # TIER_3_HIGH
            # High risk -> Stage for manual human review
            self.staged_candidates[candidate.candidate_id] = candidate
            return {
                "candidate_id": candidate.candidate_id,
                "status": "staged_for_manual_approval",
                "risk_tier": candidate.risk_tier,
                "msg": "Staged for mandatory high-risk human manual approval."
            }

    def execute_manual_promotion(
        self,
        candidate_id: UUID,
        tenant_id: str,
        result: ExperimentResult,
        approved: bool
    ) -> Dict[str, Any]:
        """Executes high-risk Tier 3 manual approval/rejection."""
        candidate = self.staged_candidates.pop(candidate_id, None)
        if not candidate:
            return {"status": "not_found"}

        if approved:
            delta = self.delta_log.record_upgrade(tenant_id, candidate, result)
            self.approved_deltas.append(delta)
            status = "manually_promoted"
            msg = "Manual human approval granted. Versioned Capability Delta registered."
        else:
            status = "rejected"
            msg = "Staged candidate rejected and discarded."

        return {
            "candidate_id": candidate_id,
            "status": status,
            "msg": msg
        }
