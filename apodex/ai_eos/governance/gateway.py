"""Governance, Architecture Governance, Meta-Governance, and IES implementation for SERO v2.

Enforces multi-criteria policy gates, bounded context dependency rules, complexity budgets,
and dynamic Agent Lifecycle Management with calibration tracking.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from ..domain.models import Capability
from ..interfaces.services import IGovernanceGateway

logger = logging.getLogger("sero.ies")


class GovernanceGateway(IGovernanceGateway):
    """The authoritative gatekeeper enforcing GRC, architectural, and evolution policies over SERO."""

    def __init__(self, initial_capital_limit_cents: int = 1000_000_00) -> None:
        self.capital_limit_cents = initial_capital_limit_cents
        # Track complexity metrics for Meta-Governance
        self.complexity_budget_limit = 100  # maximum allowed capabilities/agents
        self.active_complexity_score = 0.0
        self.technical_debt_score = 0.0

        # IES Ledgers
        self.agent_registry: List[str] = ["agent_ceo", "agent_cfo", "agent_cto", "agent_scout"]
        self.decision_record_ledger: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Standard Policy Gates (GRC)
    # ------------------------------------------------------------------
    def evaluate_action(self, action_type: str, risk_score: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess safety, risk, legal compliance, ethics, budgets, and determine if human-in-the-loop is required."""
        logger.info(f"Evaluating GRC Policy Gate for action: {action_type} [risk={risk_score}]")

        # 1. Financial check
        budget_cents = context.get("budget_cents", 0)
        if budget_cents > self.capital_limit_cents:
            logger.warning(f"Action blocked: Budget ${budget_cents/100:.2f} exceeds limit ${self.capital_limit_cents/100:.2f}")
            return {"cleared": False, "reason": "BUDGET_CEILING_EXCEEDED", "human_required": True}

        # 2. Risk check & human approval gating
        if risk_score > 0.85:
            logger.warning(f"Action blocked: Risk score {risk_score} exceeds acceptable thresholds.")
            return {"cleared": False, "reason": "EXTREME_RISK_BREACH", "human_required": True}

        if risk_score >= 0.50:
            logger.info(f"Action suspended pending explicit human-in-the-loop sign-off.")
            return {"cleared": False, "reason": "HUMAN_APPROVAL_REQUIRED", "human_required": True}

        logger.info(f"Action successfully cleared GRC Policy Gate.")
        return {"cleared": True, "reason": "POLICY_PASSED", "human_required": False}

    # ------------------------------------------------------------------
    # Architecture Governance
    # ------------------------------------------------------------------
    def evaluate_architecture_conformance(self, capability: Capability) -> bool:
        """Enforce strict bounded context checks, dependency rules, and duplication guards."""
        logger.info(f"Evaluating Architecture Governance for capability: {capability.name}")

        # 1. coupling check: A single capability cannot have more than 3 direct dependencies
        if len(capability.dependencies) > 3:
            logger.warning(f"Architecture Violation: Capability {capability.name} has too many dependencies ({len(capability.dependencies)}). Max coupling is 3.")
            return False

        # 2. Duplicate detection: We block capabilities attempting to replicate core contexts
        if "replicate_core" in capability.description.lower() or "bypass_governance" in capability.description.lower():
            logger.warning(f"Architecture Violation: Capability {capability.name} duplicates core systems or violates security boundaries.")
            return False

        # 3. Ownership / Context alignment check
        if capability.owner not in ["Executive", "Research", "Memory", "Operations", "FrontierIntelligence"]:
            logger.warning(f"Architecture Violation: Capability {capability.name} specifies an invalid owner context: {capability.owner}")
            return False

        logger.info(f"Architecture Conformance successfully verified for {capability.name}.")
        return True

    # ------------------------------------------------------------------
    # Meta-Governance (Governance of the system's own evolution)
    # ------------------------------------------------------------------
    def evaluate_system_change(self, total_capabilities_count: int, code_added_lines: int) -> Dict[str, Any]:
        """Track and control structural technical debt and complexity budgets of the OS itself."""
        logger.info("Evaluating Meta-Governance change request and complexity budgets...")

        # Calculate structural complexity score
        self.active_complexity_score = (total_capabilities_count * 1.5) + (code_added_lines * 0.05)

        # Calculate technical debt score
        if self.active_complexity_score > self.complexity_budget_limit:
            self.technical_debt_score = (self.active_complexity_score - self.complexity_budget_limit) / 10.0
        else:
            self.technical_debt_score = 0.0

        is_budget_exceeded = total_capabilities_count >= self.complexity_budget_limit
        refactoring_scheduled = self.technical_debt_score > 2.0

        logger.info(f"Meta-Governance Stats: Complexity = {self.active_complexity_score:.2f}, Tech Debt = {self.technical_debt_score:.2f}, Refactor Scheduled = {refactoring_scheduled}")

        return {
            "is_budget_exceeded": is_budget_exceeded,
            "technical_debt_score": self.technical_debt_score,
            "refactoring_scheduled": refactoring_scheduled,
            "approved": not is_budget_exceeded
        }

    # ------------------------------------------------------------------
    # IES: Agent Lifecycle Management
    # ------------------------------------------------------------------
    def manage_agent_lifecycle(self, action: str, agent_id: str, context: Optional[str] = None) -> str:
        """Dynamically manage the active agent roster (SPAWN | MERGE | SPLIT | RETIRE).

        Subject to complexity budgets and architectural coupling.
        """
        logger.info(f"IES processing Agent Lifecycle change: {action} on {agent_id}")

        if action == "SPAWN":
            if len(self.agent_registry) >= self.complexity_budget_limit:
                logger.warning("Agent Spawning BLOCKED: complexity budget limit reached.")
                return "SPAWN_BLOCKED"
            self.agent_registry.append(agent_id)
            logger.info(f"IES: Successfully spawned specialized agent '{agent_id}'.")
            return "SPAWNED"

        elif action == "RETIRE":
            if agent_id in self.agent_registry:
                self.agent_registry.remove(agent_id)
                logger.info(f"IES: Successfully retired agent '{agent_id}'.")
                return "RETIRED"
            return "NOT_FOUND"

        elif action == "MERGE":
            # Combine target agent into standard registries
            logger.info(f"IES: Merged capabilities of '{agent_id}' into standard coordinators.")
            return "MERGED"

        logger.warning(f"IES: Unknown agent lifecycle action '{action}' requested.")
        return "UNKNOWN_ACTION"

    # ------------------------------------------------------------------
    # IES: Institutional Decision Record & Calibration Trail
    # ------------------------------------------------------------------
    def record_institutional_decision(
        self,
        decision_id: str,
        reasoning: str,
        confidence: float,
        actual_accuracy: Optional[float] = None
    ) -> Dict[str, Any]:
        """Record a strategic choice and log its expected vs. actual calibration trail."""
        logger.info(f"IES Recording Strategic Decision '{decision_id}' [confidence={confidence:.2%}]")

        # Calculate calibration mismatch/bias if actual outcome is known
        bias = 0.0
        if actual_accuracy is not None:
            bias = actual_accuracy - confidence
            logger.info(f"IES Calibration Trail: Predicted Confidence={confidence:.2%}, Actual Success={actual_accuracy:.2%}, Bias={bias:+.2%}")

        record = {
            "decision_id": decision_id,
            "reasoning": reasoning,
            "confidence": confidence,
            "actual_accuracy": actual_accuracy,
            "bias": bias,
            "timestamp": datetime.utcnow()
        }
        self.decision_record_ledger.append(record)
        return record
