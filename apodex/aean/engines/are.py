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
from ..models import EngineName, MicroCell

logger = logging.getLogger("aean.are")

CPM_CENTS = 800  # $8.00 cost per 1,000 impressions.
BASE_UNIT_COST_CENTS = 1500  # Marginal cost of goods per conversion.


class AutonomousRevenueEngine:
    """Revenue optimisation, funnels and dynamic pricing (ARE)."""

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
        """Elasticity-optimal price via the standard monopoly markup rule.

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

        # Pick the highest-CTR asset attached to this signal's narratives. When
        # the RGAE has screened a narrative's assets, only creatives that
        # cleared the revenue gate are eligible for spend; otherwise fall back
        # to all assets (RGAE not attached).
        best_ctr = 0.0
        best_resonance = 0.5
        for narrative in self.ekg.narratives_for(cell.signal_id):
            best_resonance = max(best_resonance, narrative.predicted_resonance)
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

        price = self.compute_optimal_price_cents(BASE_UNIT_COST_CENTS, signal.elasticity)
        impressions = (spend / CPM_CENTS) * 1000.0
        clicks = impressions * best_ctr
        # Conversion rate rises with narrative resonance and falls as price
        # climbs above the marginal cost (a soft elasticity penalty), scaled by
        # the arm's latent quality and multiplicative market noise.
        arm = f"{cell.market}:{cell.segment}"
        price_pressure = min(1.0, BASE_UNIT_COST_CENTS / price)
        conv_rate = 0.010 * (0.5 + best_resonance) * (0.4 + 0.6 * price_pressure) * self._quality(arm)
        # Market saturation: returns diminish as cumulative revenue approaches
        # the signal's total addressable market, so no cell compounds forever.
        tam = max(1, signal.estimated_tam_cents)
        saturation = tam / (tam + cell.revenue_cents)
        conversions = clicks * conv_rate * saturation * self._rng.uniform(0.7, 1.3)
        # Only the contribution margin (price minus marginal cost) is revenue.
        margin = max(0, price - BASE_UNIT_COST_CENTS)
        net_revenue = int(conversions * margin)

        cell.deployed_cents += spend
        cell.revenue_cents += net_revenue
        cell.cycles_run += 1
        self.ekg.record_cell(cell)
        self.governance.note_decision(EngineName.ARE, success=net_revenue >= spend)
        logger.debug(
            "ARE funnel cell=%s spend=%d rev=%d conv=%.1f price=%d", cell.cell_id, spend, net_revenue, conversions, price
        )
        return net_revenue
