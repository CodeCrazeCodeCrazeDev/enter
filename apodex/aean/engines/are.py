"""ARE — Autonomous Revenue Engine.

ARE closes the loop from attention to revenue. For each active micro-cell it:

1. selects the best-performing creative asset in the EKG,
2. deploys the cell's remaining capital as channel spend,
3. runs a funnel (impressions -> clicks -> conversions) using the asset's
   predicted CTR and a resonance/price-aware conversion model, and
4. prices each conversion via a demand-elasticity optimiser.

Realised revenue and newly deployed spend are written back onto the micro-cell
so PAEAN can compute ROI and reallocate capital on the next cycle.
"""
from __future__ import annotations

import logging
import random
from typing import Optional

from ..ekg import EconomicKnowledgeGraph
from ..governance import ConstitutionalFilter
from ..models import (
    EngineName,
    MicroCell,
    Offer,
    CustomerGraphEntry,
    LeadScore,
    Lead,
    WinningPattern,
)

logger = logging.getLogger("aean.are")

CPM_CENTS = 800  # $8.00 cost per 1,000 impressions.
BASE_UNIT_COST_CENTS = 1500  # Marginal cost of goods per conversion.


class AutonomousRevenueEngine:
    """Revenue optimisation, funnels and dynamic pricing (ARE) — Layers 0-7."""

    def __init__(
        self,
        ekg: EconomicKnowledgeGraph,
        governance: ConstitutionalFilter,
        *,
        rng: Optional[random.Random] = None,
        spend_fraction: float = 0.5,
    ) -> None:
        self.ekg = ekg
        self.governance = governance
        self._rng = rng or random.Random()
        self.spend_fraction = spend_fraction
        # Latent, unobservable "true quality" of each market:segment arm. This
        # is what PAEAN's Thompson Sampling must *learn* from realised ROI; some
        # arms are structurally unprofitable (< ~0.6) and should be killed.
        self._arm_quality: dict[str, float] = {}

    def _quality(self, arm: str) -> float:
        if arm not in self._arm_quality:
            self._arm_quality[arm] = self._rng.uniform(0.35, 1.45)
        return self._arm_quality[arm]

    # ------------------------------------------------------------------
    def compute_optimal_price_cents(self, base_cost_cents: int, elasticity: float) -> int:
        """Elasticity-optimal price via the standard monopoly markup rule (Layer 1).

        For constant-elasticity demand the profit-maximising price is
        ``p = c * e / (e + 1)`` where ``e`` is the (negative) elasticity. Falls
        back to a bounded markup when demand is inelastic (``|e| <= 1``).
        """
        if elasticity < -1.0:
            markup = elasticity / (elasticity + 1.0)  # > 1 for e < -1.
            price = int(base_cost_cents * markup)
        else:
            price = int(base_cost_cents * 2.0)
        return max(price, base_cost_cents + 1)

    def run_funnel(self, cell: MicroCell) -> int:
        """Deploy spend for one cycle and return the revenue realised (cents)."""
        signal = self.ekg.signals.get(cell.signal_id)
        if signal is None:
            return 0

        # Layer 0 & 1: Offer & Pricing Intelligence
        # Look up or build a new Offer and customer profile for this opportunity
        customer_profile = None
        if self.ekg.customer_profiles:
            customer_profile = list(self.ekg.customer_profiles.values())[0]
        else:
            customer_profile = CustomerGraphEntry(
                problem=f"Overhead problems in {cell.market}",
                desire="Automate workflows",
                objection="Pricing compliance",
                buying_trigger="None",
                preferred_channel="LinkedIn",
                confidence=0.8
            )
            self.ekg.record_customer_profile(customer_profile)

        # Baseline pricing bounds
        base_optimal = self.compute_optimal_price_cents(BASE_UNIT_COST_CENTS, signal.elasticity)
        price_floor = int(base_optimal * 0.8)
        price_ceiling = int(base_optimal * 1.5)

        # Offer Architect Agent
        offer_statement = f"Reduce Support Cost in {signal.market} for {signal.segment} by 40% in 30 Days."
        offer = Offer(
            offer_statement=offer_statement,
            bundle_options=["Standard Platform", "Premium SLA Access"],
            price_floor=price_floor,
            price_ceiling=price_ceiling,
            guarantee="Full money-back guarantee."
        )
        self.ekg.record_offer(offer)

        # Layer 2: Product Creation Factory
        product_type = self._rng.choice(["MVP Builder", "Content Product", "Service Automation"])
        self.ekg.upsert_node(
            cell.cell_id,
            "product_creation_factory",
            product_type=product_type,
            status="experiment"
        )

        # Pick the highest-CTR asset attached to this signal's narratives.
        best_ctr = 0.0
        best_resonance = 0.5
        best_narrative_id = None
        for narrative in self.ekg.narratives_for(cell.signal_id):
            best_resonance = max(best_resonance, narrative.predicted_resonance)
            best_narrative_id = narrative.narrative_id
            validated = self.ekg.validated_assets_for(narrative.narrative_id)
            screened = any(
                a.asset_id in self.ekg.validations
                for a in self.ekg.assets_for(narrative.narrative_id)
            )
            eligible = validated if screened else self.ekg.assets_for(narrative.narrative_id)
            for asset in eligible:
                best_ctr = max(best_ctr, asset.predicted_ctr)
        if best_ctr <= 0:
            return 0

        remaining = max(0, cell.allocated_cents - cell.deployed_cents)
        spend = int(remaining * self.spend_fraction)
        if spend <= 0:
            return 0

        # Dynamic Pricing (optimized per cycle within floor/ceiling bounds)
        dynamic_price = int(base_optimal * self._rng.uniform(0.9, 1.2))
        price = max(price_floor, min(price_ceiling, dynamic_price))

        impressions = (spend / CPM_CENTS) * 1000.0
        clicks = impressions * best_ctr

        # Conversion rate rises with narrative resonance and falls as price
        # climbs above the marginal cost, scaled by latent quality.
        arm = f"{cell.market}:{cell.segment}"
        price_pressure = min(1.0, BASE_UNIT_COST_CENTS / price)
        conv_rate = 0.010 * (0.5 + best_resonance) * (0.4 + 0.6 * price_pressure) * self._quality(arm)

        # Market saturation
        tam = max(1, signal.estimated_tam_cents)
        saturation = tam / (tam + cell.revenue_cents)
        conversions = clicks * conv_rate * saturation * self._rng.uniform(0.7, 1.3)

        # Layer 4: Autonomous Sales Engine (generating Leads & checking compliance)
        if conversions > 0 and best_narrative_id:
            lead_score = LeadScore(
                intent=self._rng.uniform(0.6, 1.0),
                need=self._rng.uniform(0.5, 1.0),
                budget=self._rng.uniform(0.5, 1.0),
                timing=self._rng.uniform(0.5, 1.0),
                fit=self._rng.uniform(0.7, 1.0)
            )
            # Route to Conversation / Sales Agent if qualified
            if lead_score.total_score >= 0.7:
                lead = Lead(
                    lead_score=lead_score,
                    customer_id=customer_profile.customer_id,
                    narrative_id=best_narrative_id,
                    visual_id=list(self.ekg.assets.keys())[0] if self.ekg.assets else "default_asset"
                )
                self.ekg.record_lead(lead)

                # Deal Agent contracts route through Governance
                gov_verdict = self.governance.review_allocation(
                    amount_cents=price,
                    treasury_cents=100_000_00,
                    currently_deployed_cents=0
                )
                if not gov_verdict.approved:
                    logger.debug("Deal terms flagged by Governance!")

        # Only the contribution margin (price minus marginal cost) is revenue.
        margin = max(0, price - BASE_UNIT_COST_CENTS)
        net_revenue = int(conversions * margin)

        # Layer 5: Customer Success Engine (Retention/Expansion behavior)
        if net_revenue >= spend:
            # Expansion uplift
            expansion_uplift = self._rng.uniform(0.01, 0.12)
            net_revenue += int(net_revenue * expansion_uplift)
            customer_profile.confidence = min(1.0, customer_profile.confidence + 0.04)
        else:
            # Usage decay & churn risk
            customer_profile.confidence = max(0.0, customer_profile.confidence - 0.05)

        self.ekg.record_customer_profile(customer_profile)

        # Layer 7: Write patterns to shared RMG (Revenue Memory Graph)
        pattern = WinningPattern(
            pattern_type="pricing_optimization",
            segment=cell.segment,
            channel=customer_profile.preferred_channel,
            feature_set={"price": price, "resonance": best_resonance, "product_type": product_type},
            outcome_metric=net_revenue / max(1, spend),
            sample_size=int(conversions),
            confidence=0.85
        )
        self.ekg.record_winning_pattern(pattern)

        cell.deployed_cents += spend
        cell.revenue_cents += net_revenue
        cell.cycles_run += 1
        self.ekg.record_cell(cell)
        self.governance.note_decision(EngineName.ARE, success=net_revenue >= spend)
        logger.debug(
            "ARE funnel cell=%s spend=%d rev=%d conv=%.1f price=%d", cell.cell_id, spend, net_revenue, conversions, price
        )
        return net_revenue
