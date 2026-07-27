"""Entrepreneurial Intelligence System (EIS) implementation for SERO v2.

Resolves structural meta-economic decisions (venture, license, open-source, publish)
and executes recursive scientific organizational modifications.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from ...ai_eos.domain.models import Theory

logger = logging.getLogger("sero.eis")


class EntrepreneurialIntelligenceSystem:
    """The formal, strategic decision and organizational architect of SERO v2."""

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Meta-Economic Decision Framework
    # ------------------------------------------------------------------
    def evaluate_opportunity_form(self, theory: Theory, available_capital_cents: int) -> str:
        """Analyze a promoted Theory node and select its optimal economic form.

        Forms: BUILD_VENTURE | LICENSE_IP | OPEN_SOURCE | PUBLISH_RESEARCH | HOLD_PLATFORM
        """
        logger.info(f"EIS executing Meta-Economic Decision Framework over Theory node: {theory.theory_id}")

        # High capital (> $10k) and high confidence (> 0.8) -> Build Venture
        if available_capital_cents >= 10000_00 and theory.confidence >= 0.80:
            logger.info("EIS Decided: BUILD_VENTURE (Capital and Confidence support full venture lifecycle).")
            return "BUILD_VENTURE"

        # Low capital (< $10k) but high confidence -> License IP
        if available_capital_cents < 10000_00 and theory.confidence >= 0.80:
            logger.info("EIS Decided: LICENSE_IP (High confidence, but constrained capital limits physical launch).")
            return "LICENSE_IP"

        # Moderate confidence, high predictive scope -> Open Source to build ecosystem
        if theory.confidence >= 0.60 and len(theory.predictive_scope) >= 1:
            logger.info("EIS Decided: OPEN_SOURCE (Promotes ecosystem-wide standard and feedback loop).")
            return "OPEN_SOURCE"

        # Else default to Publish
        logger.info("EIS Decided: PUBLISH_RESEARCH (Low commercial viability/confidence; export as pure knowledge).")
        return "PUBLISH_RESEARCH"

    # ------------------------------------------------------------------
    # Recursive Scientific Organization
    # ------------------------------------------------------------------
    def recommend_capability_refinements(self, forecasting_errors_ratio: float) -> List[str]:
        """Examine forecast calibration errors and suggest standing up specialized agent disciplines."""
        logger.info(f"EIS analyzing forecasting error calibration ratio: {forecasting_errors_ratio:.2%}")

        proposals = []
        if forecasting_errors_ratio > 0.15:
            # Significant forecast errors in pricing/elasticity -> propose pricing specialist
            proposals.append("SPAWN_PRICING_SPECIALIST_AGENT")
            logger.info("EIS Proposal: Spawn specialized PricingEconometricsAgent to stabilize conversion forecasts.")

        if forecasting_errors_ratio > 0.30:
            # Extreme general errors -> propose multi-agent splitter
            proposals.append("SPLIT_GENERALIST_INTO_PEER_REVIEW_TRIAD")
            logger.info("EIS Proposal: Split overloaded generalist into a Peer-Review Chairman triad.")

        return proposals
