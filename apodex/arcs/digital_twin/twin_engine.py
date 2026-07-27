from __future__ import annotations
import logging
from typing import Any, Dict, List

logger = logging.getLogger("arcs.digital_twin")


class EconomicDigitalTwin:
    """Immersive simulation environment modeling company unit economics and customer behavior.

    Models:
    - Customers: demand, willingness to pay, churn, adoption, satisfaction, referrals.
    - Competitors: pricing, features, advertising, market entry, reactions.
    - Market: macro trends, regulation, seasonality, supply constraints.
    - Business: cash flow, CAC, LTV, burn, runway, capacity.
    """

    def __init__(
        self,
        baseline_mrr_cents: int,
        baseline_churn_rate: float,
        initial_cash_cents: int = 10_000_000, # $100k
        monthly_fixed_burn_cents: int = 500_000 # $5k
    ) -> None:
        self.mrr_cents = baseline_mrr_cents
        self.churn_rate = baseline_churn_rate
        self.cash_cents = initial_cash_cents
        self.fixed_burn_cents = monthly_fixed_burn_cents

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

    def simulate_full_rehearsal(
        self,
        months: int = 12,
        marketing_monthly_spend_cents: int = 1_000_000,
        est_cac_cents: int = 20_000, # $200
        arpu_cents: int = 10_000,     # $100
        competitor_reaction: str = "none",  # pricing_undercut, feature_copy, heavy_ads, none
        market_macro_multiplier: float = 1.0,  # e.g., 0.8 for recession, 1.2 for boom
        regulatory_headwind_pct: float = 0.0,   # churn modifier
        referral_rate: float = 0.05             # customer referrals
    ) -> Dict[str, Any]:
        """Simulate multi-month decision rehearsal under Customer, Competitor, Market, and Business dynamics."""
        current_cash = self.cash_cents
        current_mrr = self.mrr_cents
        historical_stats: List[Dict[str, Any]] = []

        # Customer & Competitor reaction dynamics
        adjusted_churn = self.churn_rate
        adjusted_cac = est_cac_cents

        if competitor_reaction == "pricing_undercut":
            # Undercutting increases our churn and increases our CAC
            adjusted_churn += 0.02
            adjusted_cac = int(adjusted_cac * 1.2)
        elif competitor_reaction == "heavy_ads":
            # Higher ad spend by competitors increases our CAC
            adjusted_cac = int(adjusted_cac * 1.3)

        # Market macro trends and regulatory headwinds
        adjusted_churn += regulatory_headwind_pct
        adjusted_churn = max(0.01, adjusted_churn)

        # Multi-month step loop
        for m in range(1, months + 1):
            # 1. Customer Acquisition (Inflow)
            acquisitions = int((marketing_monthly_spend_cents // adjusted_cac) * market_macro_multiplier)
            new_mrr_added = acquisitions * arpu_cents

            # Churn (Outflow)
            churned_mrr = int(current_mrr * adjusted_churn)
            current_mrr = max(0, current_mrr + new_mrr_added - churned_mrr)

            # Customer referral boost
            referrals = int(acquisitions * referral_rate)
            current_mrr += referrals * arpu_cents

            # 2. Financials & Cash flow
            gross_revenue = current_mrr  # assume monthly MRR realized as cash
            total_expenses = self.fixed_burn_cents + marketing_monthly_spend_cents
            cash_flow = gross_revenue - total_expenses
            current_cash += cash_flow

            # Metrics
            runway_months = (current_cash // max(1, -cash_flow)) if cash_flow < 0 else float("inf")
            ltv_cents = int((arpu_cents) / max(0.001, adjusted_churn))
            ltv_cac_ratio = ltv_cents / adjusted_cac if adjusted_cac > 0 else 0.0

            historical_stats.append({
                "month": m,
                "cash_cents": current_cash,
                "mrr_cents": current_mrr,
                "acquisitions": acquisitions,
                "churned_mrr_cents": churned_mrr,
                "cash_flow_cents": cash_flow,
                "runway_months": runway_months if runway_months != float("inf") else -1
            })

        # Final verdict
        is_viable = current_cash > 0 and current_mrr > self.mrr_cents
        recommendation = "scale" if is_viable and (current_cash > self.cash_cents) else "pivot_or_hold"

        return {
            "viable": is_viable,
            "final_cash_cents": current_cash,
            "final_mrr_cents": current_mrr,
            "ltv_cac_ratio": ltv_cac_ratio,
            "recommendation": recommendation,
            "monthly_history": historical_stats
        }
