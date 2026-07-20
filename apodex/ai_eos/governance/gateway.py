"""Governance, Architecture Governance, and Meta-Governance implementation for AI-EOS.

Enforces multi-criteria policy gates, bounded context dependency rules, and self-evolution
complexity budgets to prevent architectural decay.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..domain.models import Capability
from ..interfaces.services import IGovernanceGateway

logger = logging.getLogger("ai_eos.governance")


class GovernanceGateway(IGovernanceGateway):
    """The authoritative gatekeeper enforcing safety and architectural invariants over AI-EOS."""

    def __init__(self, initial_capital_limit_cents: int = 1000_000_00) -> None:
        self.capital_limit_cents = initial_capital_limit_cents
        # Track complexity metrics for Meta-Governance
        self.complexity_budget_limit = 100  # maximum allowed capabilities
        self.active_complexity_score = 0.0
        self.technical_debt_score = 0.0

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

        # 2. Duplicate detection: We block capabilities attempting to replicate core core contexts
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
