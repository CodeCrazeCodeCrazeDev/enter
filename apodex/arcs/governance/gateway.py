from __future__ import annotations
import logging
import uuid
import hashlib
from datetime import datetime, UTC
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.governance")


class GovernanceStage(str, Enum):
    ADVISORY = "advisory"          # AI recommends, human executes
    SUPERVISED = "supervised"      # AI executes low-risk, human approves high-risk
    AUTONOMOUS = "autonomous"      # AI operates fully within strict policy limits
    STRATEGIC = "strategic"        # AI operates company, human adjusts core parameters


class ActionState(str, Enum):
    PROPOSED = "PROPOSED"
    VALIDATED = "VALIDATED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"


class AuditEvent(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    from_state: str
    to_state: str
    details: str
    signature: str = ""


class GovernanceActionProposal(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    action_type: str  # e.g., publishing, spending, hiring, legal_filing, investment, acquisition
    risk_score: float
    context: Dict[str, Any] = Field(default_factory=dict)
    state: ActionState = ActionState.PROPOSED
    audit_trail: List[AuditEvent] = Field(default_factory=list)
    audit_hash: str = ""

    def transition_to(self, to_state: ActionState, details: str) -> None:
        """Execute a state transition, record to audit log, and update rolling hash."""
        from_state = self.state.value
        self.state = to_state
        event = AuditEvent(from_state=from_state, to_state=to_state.value, details=details)

        # Compute SHA-256 signature for this event
        event_str = f"{event.timestamp}|{event.from_state}|{event.to_state}|{event.details}|{self.audit_hash}"
        event.signature = hashlib.sha256(event_str.encode("utf-8")).hexdigest()

        self.audit_trail.append(event)
        self.audit_hash = event.signature
        logger.info(f"[Governance Audit] Action {self.id} transitioned {from_state} -> {to_state.value}. Audit Hash: {self.audit_hash[:8]}")


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
        # State machine active proposals store
        self.proposals: Dict[uuid.UUID, GovernanceActionProposal] = {}

    def set_governance_stage(self, stage: GovernanceStage) -> None:
        logger.info(f"Transitioning governance stage: {self.current_stage} -> {stage}")
        self.current_stage = stage

    def create_proposal(self, action_type: str, risk_score: float, context: Dict[str, Any]) -> GovernanceActionProposal:
        """Instantiate a new proposal, entering the PROPOSED state."""
        proposal = GovernanceActionProposal(
            action_type=action_type,
            risk_score=risk_score,
            context=context,
            state=ActionState.PROPOSED,
            audit_hash=hashlib.sha256(str(uuid.uuid4()).encode("utf-8")).hexdigest()
        )
        proposal.transition_to(ActionState.PROPOSED, "Proposal created and registered.")
        self.proposals[proposal.id] = proposal
        return proposal

    def process_action(self, action_type: str, risk_score: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process an action. Returns action clearance status or registers an approval request if required."""
        # Align with the state machine proposal tracking
        proposal = self.create_proposal(action_type, risk_score, context)
        proposal.transition_to(ActionState.VALIDATED, "Self-verification and validation completed.")

        # Enforce Advisory stage
        if self.current_stage == GovernanceStage.ADVISORY:
            req = ApprovalRequest(id=proposal.id, action_type=action_type, risk_score=risk_score, context=context)
            self.pending_approvals[req.id] = req
            proposal.transition_to(ActionState.PENDING_APPROVAL, "Escalated for mandatory Advisory-stage manual review.")
            logger.info(f"[Advisory Stage] Registered mandatory recommendation approval: {req.id}")
            return {"cleared": False, "approval_id": req.id, "reason": "Advisory stage requires manual approval for all actions."}

        # Enforce Autonomous stage
        if self.current_stage == GovernanceStage.AUTONOMOUS:
            if risk_score > 0.85:
                proposal.transition_to(ActionState.REJECTED, f"Action risk {risk_score} exceeds maximum autonomous threshold of 0.85.")
                logger.warning(f"[Autonomous Stage] Intercepted CRITICAL action exceeding safety envelope (Risk: {risk_score}). Blocking.")
                return {"cleared": False, "approval_id": None, "reason": "Action risk exceeds maximum autonomous threshold of 0.85."}
            proposal.transition_to(ActionState.APPROVED, "Instantly approved under low-risk autonomous envelope.")
            proposal.transition_to(ActionState.EXECUTING, "Direct autonomous execution initiated.")
            logger.info(f"[Autonomous Stage] Instantly cleared low-risk action (Risk: {risk_score})")
            return {"cleared": True, "approval_id": None}

        # Enforce Strategic stage
        if self.current_stage == GovernanceStage.STRATEGIC:
            proposal.transition_to(ActionState.APPROVED, "Approved under Strategic operating stage.")
            proposal.transition_to(ActionState.EXECUTING, "Direct execution initiated.")
            logger.info(f"[Strategic Stage] Autocleared company-level operational action (Risk: {risk_score})")
            return {"cleared": True, "approval_id": None}

        # Enforce Supervised (default) stage
        # Low risk (<0.50) is auto-cleared; High risk (>=0.50) is escalated to Human Governance
        if risk_score < 0.50:
            proposal.transition_to(ActionState.APPROVED, "Auto-cleared under low-risk Supervised stage.")
            proposal.transition_to(ActionState.EXECUTING, "Execution started.")
            logger.info(f"[Supervised Stage] Auto-cleared low-risk action (Risk: {risk_score})")
            return {"cleared": True, "approval_id": None}
        else:
            req = ApprovalRequest(id=proposal.id, action_type=action_type, risk_score=risk_score, context=context)
            self.pending_approvals[req.id] = req
            proposal.transition_to(ActionState.PENDING_APPROVAL, "Escalated to human-in-the-loop approval gate.")
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

        # Transition the proposal to APPROVED -> EXECUTING
        if approval_id in self.proposals:
            p = self.proposals[approval_id]
            p.transition_to(ActionState.APPROVED, f"Approved by {approver_name}.")
            p.transition_to(ActionState.EXECUTING, "Execution initiated by approval resolution.")

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

        # Transition the proposal to REJECTED
        if approval_id in self.proposals:
            p = self.proposals[approval_id]
            p.transition_to(ActionState.REJECTED, f"Rejected by {approver_name}.")

        logger.warning(f"APPROVAL REJECTED by {approver_name} for request {approval_id}")
        return True

    def complete_action(self, approval_id: uuid.UUID) -> None:
        """Transition an executing action proposal to COMPLETED."""
        if approval_id in self.proposals:
            p = self.proposals[approval_id]
            if p.state == ActionState.EXECUTING:
                p.transition_to(ActionState.COMPLETED, "Execution successfully completed.")
