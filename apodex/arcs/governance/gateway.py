from __future__ import annotations
import logging
import uuid
from enum import Enum
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.governance")


class GovernanceStage(str, Enum):
    ADVISORY = "advisory"          # AI recommends, human executes
    SUPERVISED = "supervised"      # AI executes low-risk, human approves high-risk
    AUTONOMOUS = "autonomous"      # AI operates fully within strict policy limits
    STRATEGIC = "strategic"        # AI operates company, human adjusts core parameters


class ApprovalRequest(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    action_type: str
    risk_score: float
    context: Dict[str, Any]
    status: str = "pending"  # pending, approved, rejected
    approver: Optional[str] = None


class HumanGovernanceGateway:
    """Centralized governance layer enforcing policy limits, risk scores, and human-in-the-loop approvals."""

    def __init__(self, initial_stage: GovernanceStage = GovernanceStage.SUPERVISED) -> None:
        self.current_stage = initial_stage
        self.pending_approvals: Dict[uuid.UUID, ApprovalRequest] = {}
        self.approved_history: List[ApprovalRequest] = []

    def set_governance_stage(self, stage: GovernanceStage) -> None:
        logger.info(f"Transitioning governance stage: {self.current_stage} -> {stage}")
        self.current_stage = stage

    def process_action(self, action_type: str, risk_score: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process an action. Returns action clearance status or registers an approval request if required."""
        # Enforce Advisory stage
        if self.current_stage == GovernanceStage.ADVISORY:
            req = ApprovalRequest(action_type=action_type, risk_score=risk_score, context=context)
            self.pending_approvals[req.id] = req
            logger.info(f"[Advisory Stage] Registered mandatory recommendation approval: {req.id}")
            return {"cleared": False, "approval_id": req.id, "reason": "Advisory stage requires manual approval for all actions."}

        # Enforce Autonomous stage
        if self.current_stage == GovernanceStage.AUTONOMOUS:
            if risk_score > 0.85:
                logger.warning(f"[Autonomous Stage] Intercepted CRITICAL action exceeding safety envelope (Risk: {risk_score}). Blocking.")
                return {"cleared": False, "approval_id": None, "reason": "Action risk exceeds maximum autonomous threshold of 0.85."}
            logger.info(f"[Autonomous Stage] Instantly cleared low-risk action (Risk: {risk_score})")
            return {"cleared": True, "approval_id": None}

        # Enforce Strategic stage
        if self.current_stage == GovernanceStage.STRATEGIC:
            logger.info(f"[Strategic Stage] Autocleared company-level operational action (Risk: {risk_score})")
            return {"cleared": True, "approval_id": None}

        # Enforce Supervised (default) stage
        # Low risk (<0.50) is auto-cleared; High risk (>=0.50) is escalated to Human Governance
        if risk_score < 0.50:
            logger.info(f"[Supervised Stage] Auto-cleared low-risk action (Risk: {risk_score})")
            return {"cleared": True, "approval_id": None}
        else:
            req = ApprovalRequest(action_type=action_type, risk_score=risk_score, context=context)
            self.pending_approvals[req.id] = req
            logger.warning(f"[Supervised Stage] High-risk action detected (Risk: {risk_score}). Escalated to Human Approval Gateway.")
            return {"cleared": False, "approval_id": req.id, "reason": "Action requires explicit Human approval due to risk level."}

    def grant_approval(self, approval_id: uuid.UUID, approver_name: str) -> bool:
        """Resolve a pending approval request as APPROVED."""
        if approval_id not in self.pending_approvals:
            return False
        req = self.pending_approvals.pop(approval_id)
        req.status = "approved"
        req.approver = approver_name
        self.approved_history.append(req)
        logger.info(f"APPROVAL GRANTED by {approver_name} for request {approval_id}")
        return True

    def deny_approval(self, approval_id: uuid.UUID, approver_name: str) -> bool:
        """Resolve a pending approval request as REJECTED."""
        if approval_id not in self.pending_approvals:
            return False
        req = self.pending_approvals.pop(approval_id)
        req.status = "rejected"
        req.approver = approver_name
        self.approved_history.append(req)
        logger.warning(f"APPROVAL REJECTED by {approver_name} for request {approval_id}")
        return True
