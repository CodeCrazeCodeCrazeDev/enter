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
    # Pearl's do-Calculus Structural Causal Model Interventions
    # ------------------------------------------------------------------
    def evaluate_scm_do_calculus(
        self,
        variable_name: str,
        intervention_value: float,
        causal_links: Dict[str, Dict[str, float]]
    ) -> Dict[str, float]:
        """Simulate a do-intervention (do(variable = value)) on a Structural Causal Model.

        causal_links is of form: {parent_variable: {child_variable: weight_multiplier}}
        Returns the full post-interventional state of all downstream variables.
        """
        logger.info(f"EIS evaluating do-calculus intervention do({variable_name} = {intervention_value})")

        state: Dict[str, float] = {variable_name: intervention_value}

        # Build topological update sequence or simple iterative propagation
        # Collect all unique variable names
        all_vars = set(causal_links.keys())
        for children in causal_links.values():
            all_vars.update(children.keys())

        # Simple iterative propagation (since graphs are DAGs, we iterate to convergence)
        for _ in range(len(all_vars) + 1):
            updated = False
            for parent, children in causal_links.items():
                if parent in state:
                    for child, weight in children.items():
                        # If child is the target of the do-intervention, its value is fixed
                        if child == variable_name:
                            continue
                        new_val = state[parent] * weight
                        if state.get(child) != new_val:
                            state[child] = new_val
                            updated = True
            if not updated:
                break

        return state

    # ------------------------------------------------------------------
    # Lagrange Multiplier Dual Shadow Prices (Bottleneck Detection)
    # ------------------------------------------------------------------
    def detect_rate_limiting_bottlenecks(
        self,
        resource_capacities: Dict[str, float],
        demand_vectors: Dict[str, List[float]],
        weights: List[float]
    ) -> Dict[str, float]:
        """Compute dual shadow prices for multiple resource constraints.

        resource_capacities: {resource_name: capacity_limit}
        demand_vectors: {resource_name: [demand_coefficient_for_activity_i]}
        weights: [priority_weight_for_activity_i]

        Returns shadow prices for each resource. Positive shadow prices indicate binding constraints (bottlenecks).
        """
        logger.info("EIS detecting rate-limiting bottlenecks using dual shadow price analysis")

        shadow_prices: Dict[str, float] = {}

        for resource, demand_list in demand_vectors.items():
            capacity = resource_capacities.get(resource, 1e-5)
            if capacity <= 0:
                capacity = 1e-5

            # Calculate total weighted demand
            total_weighted_demand = 0.0
            for i, demand_val in enumerate(demand_list):
                weight = weights[i] if i < len(weights) else 1.0
                total_weighted_demand += demand_val * weight

            # Shadow price represents marginal value of capacity expansion.
            # Here modeled as normalized excess demand ratio when constraint is binding.
            excess = total_weighted_demand - capacity
            if excess > 0:
                # Sensitivity is proportional to excess scaled by the average of active weights
                avg_weight = sum(weights) / max(1, len(weights)) if weights else 1.0
                shadow_price = (excess / capacity) * avg_weight
            else:
                shadow_price = 0.0

            shadow_prices[resource] = shadow_price
            logger.info(f"Resource {resource}: Capacity = {capacity}, Demand = {total_weighted_demand}, Shadow Price = {shadow_price:.4f}")

        return shadow_prices
