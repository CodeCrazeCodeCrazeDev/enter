"""
HarnessCritic
Verifies if proposed harness modifications are safe, useful, and aligned with AEAN's objectives.
"""

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel

from apodex.evolution.self_harness.refiner import HarnessProposal


class VerificationAudit(BaseModel):
    is_safe: bool = True
    is_useful: bool = True
    is_aligned: bool = True
    justification: str = ""


class HarnessCritic:
    """
    Acts as a safety/utility gate to evaluate proposed harness config changes
    before sandboxed validation.
    """

    def check_alignment(self, proposal: HarnessProposal) -> VerificationAudit:
        """Checks if proposal meets alignment standards, avoiding risky modifications."""
        target = proposal.target_parameter
        new_val = proposal.new_value

        # Enforce strict bounds
        if target == "max_llm_retries":
            if not isinstance(new_val, int) or new_val > 15:
                return VerificationAudit(
                    is_safe=False,
                    is_useful=False,
                    is_aligned=False,
                    justification="Unsafe retry threshold! Retries above 15 may exhaust API budget and trigger model refusal loops."
                )
        elif target == "clamping_threshold":
            if not isinstance(new_val, int) or new_val < 2000:
                return VerificationAudit(
                    is_safe=False,
                    is_useful=False,
                    is_aligned=False,
                    justification="Clamping threshold below 2,000 tokens may severely damage context window and agent performance."
                )

        return VerificationAudit(
            is_safe=True,
            is_useful=True,
            is_aligned=True,
            justification=f"Proposal '{proposal.proposal_id}' satisfies budget/safety constraints and aligns with positive-yield objectives."
        )
