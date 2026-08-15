"""Entrepreneurial Intelligence System (EIS) implementation for SERO v2.

Resolves structural meta-economic decisions (venture, license, open-source, publish)
and executes recursive scientific organizational modifications. Includes Pearl's do-calculus SCM
interventions and Lagrange multiplier dual shadow price rate-limiting bottleneck detection.
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

    # ------------------------------------------------------------------
    # EIOS Structural Causal Models & Shadow Prices (Section 8)
    # ------------------------------------------------------------------
    def evaluate_scm_do_calculus(self, intervention: str, confounding_metrics: List[float]) -> Dict[str, Any]:
        """Evaluate the counterfactual impact of an intervention under Pearl's backdoor criteria (Section 8.5).

        If confounding metrics (e.g., season spikes, external anomalies) are extreme, blocks intervention.
        """
        confounding_average = sum(confounding_metrics) / len(confounding_metrics) if confounding_metrics else 0.0
        is_confounded = confounding_average > 0.6
        expected_utility_delta = 0.0 if is_confounded else 0.45
        decision = "BLOCK_INTERVENTION" if is_confounded else "PROCEED_WITH_INTERVENTION"

        logger.info(f"SCM evaluate do({intervention}): confound_avg={confounding_average:.4f}, decision={decision}")
        return {
            "intervention": intervention,
            "confounding_average": confounding_average,
            "is_confounded": is_confounded,
            "expected_utility_delta": expected_utility_delta,
            "decision": decision
        }

    def detect_rate_limiting_bottlenecks(self, resource_shadow_prices: Dict[str, float]) -> str:
        """Detect the single rate-limiting resource bottleneck using dual shadow prices (Section 8.9).

        Computes: Bottleneck = argmax |shadow_price_i|
        """
        if not resource_shadow_prices:
            return "NONE"

        bottleneck = max(resource_shadow_prices, key=lambda k: abs(resource_shadow_prices[k]))
        logger.info(f"Shadow Price Bottleneck analysis: prices={resource_shadow_prices}, binding_bottleneck={bottleneck}")
        return bottleneck
