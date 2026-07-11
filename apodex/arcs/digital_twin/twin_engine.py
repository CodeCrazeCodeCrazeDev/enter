from __future__ import annotations
import logging
from typing import Any, Dict

logger = logging.getLogger("arcs.digital_twin")


class EconomicDigitalTwin:
    """Immersive simulation environment modeling company unit economics and customer behavior."""

    def __init__(self, baseline_mrr_cents: int, baseline_churn_rate: float) -> None:
        self.mrr_cents = baseline_mrr_cents
        self.churn_rate = baseline_churn_rate

    def simulate_price_change(self, proposed_price_pct_change: float, elasticity: float = -1.5) -> Dict[str, Any]:
        """Simulate the financial impact of a price change using price-elasticity models.

        Args:
            proposed_price_pct_change: Float representing price change (e.g. 0.20 for +20%).
            elasticity: Price elasticity of demand (typically negative).
        """
        logger.info(f"[Digital Twin] Simulating price change of {proposed_price_pct_change:.1%} with elasticity {elasticity}")

        # Demand change % = price change % * elasticity
        demand_pct_change = proposed_price_pct_change * elasticity
        new_customer_ratio = 1.0 + demand_pct_change
        new_price_ratio = 1.0 + proposed_price_pct_change

        # Project resulting MRR = baseline * customer ratio * price ratio
        projected_mrr_cents = int(self.mrr_cents * new_customer_ratio * new_price_ratio)
        yield_pct_change = (projected_mrr_cents - self.mrr_cents) / self.mrr_cents

        decision = "approve" if yield_pct_change > 0 else "reject"
        logger.info(f"[Digital Twin] Simulation results: Projected MRR change of {yield_pct_change:.2%}. Recommendation: {decision}")

        return {
            "original_mrr_cents": self.mrr_cents,
            "projected_mrr_cents": projected_mrr_cents,
            "mrr_change_pct": yield_pct_change,
            "demand_change_pct": demand_pct_change,
            "recommendation": decision
        }

    def simulate_marketing_campaign(self, budget_cents: int, est_cac_cents: int, projected_arpu_cents: int) -> Dict[str, Any]:
        """Simulate dynamic campaign acquisitions."""
        logger.info(f"[Digital Twin] Simulating marketing campaign with budget {budget_cents} cents.")
        projected_acquisitions = budget_cents // est_cac_cents if est_cac_cents > 0 else 0
        added_mrr_cents = projected_acquisitions * projected_arpu_cents
        expected_roi = (added_mrr_cents / budget_cents) if budget_cents > 0 else 0.0

        return {
            "budget_cents": budget_cents,
            "projected_acquisitions": projected_acquisitions,
            "added_mrr_cents": added_mrr_cents,
            "expected_roi": expected_roi,
            "recommendation": "approve" if expected_roi > 1.2 else "reject"
        }
