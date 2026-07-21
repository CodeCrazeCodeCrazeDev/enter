"""Portfolio Operating System (POS) implementation for SERO v2.

Manages risk-adjusted capital distribution across both the Venture Portfolio
(ROI-driven) and the Research Portfolio (Expected Discovery Value-driven).
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from ...ai_eos.domain.models import VentureCell

logger = logging.getLogger("sero.pos")


class PortfolioOperatingSystem:
    """Manages multi-asset investment distribution over commercial and knowledge-exploration signals."""

    def __init__(self, initial_reserves_cents: int = 100000_00) -> None:
        self.reserves_cents = initial_reserves_cents

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

        logger.info(f"POS Allocation Results: Venture Portfolio = ${venture_cents/100:.2f} ({venture_ratio:.1%}), Research Portfolio = ${research_cents/100:.2f} ({research_ratio:.1%})")
        return {
            "venture_portfolio_cents": venture_cents,
            "research_portfolio_cents": research_cents,
            "remaining_reserves_cents": self.reserves_cents
        }
