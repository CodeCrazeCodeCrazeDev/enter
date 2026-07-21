"""Portfolio Operating System (POS) implementation for SERO v2.1.

Manages risk-adjusted capital distribution across both the Venture Portfolio
(ROI-driven) and the Research Portfolio (Expected Discovery Value-driven),
and tracks strict Knowledge ROI metrics.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from ...ai_eos.domain.models import VentureCell, KnowledgeROI

logger = logging.getLogger("sero.pos")


class PortfolioOperatingSystem:
    """Manages multi-asset investment distribution over commercial and knowledge-exploration signals."""

    def __init__(self, initial_reserves_cents: int = 100000_00) -> None:
        self.reserves_cents = initial_reserves_cents
        self.total_spent_cents = 0

    def allocate_portfolio_capital(
        self,
        cells: List[VentureCell],
        unresolved_uncertainty_score: float,
        total_allocation_cents: int
    ) -> Dict[str, int]:
        """Proportionally split capital between Venture Execution and Research Portfolios.

        If unresolved uncertainty is high, POS allocates higher ratio to the Research Portfolio
        to generate Expected Discovery Value, which de-risks future ventures.
        """
        logger.info(f"POS executing portfolio allocation over ${total_allocation_cents/100:.2f} total capital...")

        if total_allocation_cents > self.reserves_cents:
            total_allocation_cents = self.reserves_cents

        # Research ratio increases with uncertainty
        # research_ratio maps linearly to uncertainty (clamped between 10% and 50%)
        research_ratio = max(0.10, min(0.50, unresolved_uncertainty_score))
        venture_ratio = 1.0 - research_ratio

        research_cents = int(total_allocation_cents * research_ratio)
        venture_cents = total_allocation_cents - research_cents

        # Deduct from central reserves
        self.reserves_cents -= total_allocation_cents
        self.total_spent_cents += total_allocation_cents

        logger.info(f"POS Allocation Results: Venture Portfolio = ${venture_cents/100:.2f} ({venture_ratio:.1%}), Research Portfolio = ${research_cents/100:.2f} ({research_ratio:.1%})")
        return {
            "venture_portfolio_cents": venture_cents,
            "research_portfolio_cents": research_cents,
            "remaining_reserves_cents": self.reserves_cents
        }

    # ------------------------------------------------------------------
    # Research Economics & Knowledge ROI
    # ------------------------------------------------------------------
    def calculate_knowledge_roi(
        self,
        validated_theories_count: int,
        total_entropy_reduction: float,
        reusable_insights_count: int,
        future_ventures_count: int
    ) -> KnowledgeROI:
        """Compute the research economics metric card."""
        # Total research capital spent is simulated as a fraction of overall spend
        simulated_research_spend_cents = int(self.total_spent_cents * 0.3)
        spend_usd = float(simulated_research_spend_cents / 100.0)

        cost_per_theory = spend_usd / max(1, validated_theories_count)
        cost_per_entropy = spend_usd / max(1e-5, total_entropy_reduction)
        cost_per_insight = spend_usd / max(1, reusable_insights_count)
        cost_per_venture = spend_usd / max(1, future_ventures_count)

        logger.info(f"POS calculated Knowledge ROI: Cost/Theory = ${cost_per_theory:.2f}, Cost/EntropyRed = ${cost_per_entropy:.2f}")

        return KnowledgeROI(
            cost_per_validated_theory=cost_per_theory,
            cost_per_uncertainty_reduction=cost_per_entropy,
            cost_per_reusable_insight=cost_per_insight,
            cost_per_future_venture_unlocked=cost_per_venture
        )
