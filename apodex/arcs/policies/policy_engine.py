from __future__ import annotations
import logging
from typing import Any, Dict, List
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.policies.policy_engine")


class DeclarativePolicy(BaseModel):
    policy_id: str
    max_discount_pct: float = 0.35
    max_risk_score_allowed: float = 0.85
    min_onboard_budget_cents: int = 50000


class DeclarativePolicyEngine:
    """Enterprise-grade Policy-as-Code gate evaluating declarative organizational safety gates."""

    def __init__(self) -> None:
        self.active_policies: Dict[str, DeclarativePolicy] = {
            "default": DeclarativePolicy(policy_id="default")
        }

    def register_policy(self, policy: DeclarativePolicy) -> None:
        self.active_policies[policy.policy_id] = policy
        logger.info(f"[PolicyEngine] Registered policy: {policy.policy_id}")

    def evaluate_compliance(self, policy_id: str, action_context: Dict[str, Any]) -> bool:
        """Evaluate an active command or transaction context against a declarative policy.

        Returns:
            bool: True if context is fully compliant, False otherwise.
        """
        policy = self.active_policies.get(policy_id, self.active_policies["default"])
        logger.info(f"[PolicyEngine] Evaluating compliance against policy: {policy.policy_id}")

        # Check discount constraint
        proposed_discount = action_context.get("proposed_discount_pct", 0.0)
        if proposed_discount > policy.max_discount_pct:
            logger.warning(f"[Policy-Fail] Proposed discount {proposed_discount:.2%} exceeds max permitted {policy.max_discount_pct:.2%}")
            return False

        # Check risk boundary
        proposed_risk = action_context.get("proposed_risk_score", 0.0)
        if proposed_risk > policy.max_risk_score_allowed:
            logger.warning(f"[Policy-Fail] Proposed action risk {proposed_risk:.2f} exceeds cap of {policy.max_risk_score_allowed:.2f}")
            return False

        # Check budget limits
        proposed_budget = action_context.get("proposed_budget_cents", 0)
        if proposed_budget < policy.min_onboard_budget_cents:
            logger.warning(f"[Policy-Fail] Budget {proposed_budget} cents is below minimum requirement of {policy.min_onboard_budget_cents} cents.")
            return False

        logger.info("[PolicyEngine] Context evaluated as FULLY COMPLIANT.")
        return True
