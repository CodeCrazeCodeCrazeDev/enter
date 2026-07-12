from __future__ import annotations
import logging
from typing import Any, Dict
from pydantic import BaseModel, Field

logger = logging.getLogger("arcs.investment.manager")


class InvestmentPortfolio(BaseModel):
    total_yield_earned_cents: int = 0
    allocations: Dict[str, int] = Field(default_factory=dict)


class InvestmentManager:
    """Investment Division stashing corporate reserves and planning yield optimization."""

    def __init__(self, reserve_account_cents: int = 0) -> None:
        self.reserve_account_cents = reserve_account_cents
        self.portfolio = InvestmentPortfolio()

    def allocate_yield_reserves(self, amount_cents: int) -> Dict[str, int]:
        """Deploy idle treasury capital into dynamic, risk-gated yield pools."""
        if amount_cents > self.reserve_account_cents:
            raise ValueError("Insufficient investment reserves.")

        # Split 60% low-risk stablecoin yield, 40% automated treasury yields
        stablecoin_allocation = int(amount_cents * 0.60)
        yield_pool_allocation = amount_cents - stablecoin_allocation

        allocs = {
            "stablecoin_yield_pool": stablecoin_allocation,
            "automated_treasury_yield": yield_pool_allocation
        }

        self.reserve_account_cents -= amount_cents
        for pool, cents in allocs.items():
            self.portfolio.allocations[pool] = self.portfolio.allocations.get(pool, 0) + cents

        logger.info(f"[Investment] Deployed surplus yield reserves: {allocs}")
        return allocs

    def credit_earned_yield(self, pool: str, interest_cents: int) -> None:
        """Accrue capital earnings back into corporate portfolio reserves."""
        if pool not in self.portfolio.allocations:
            raise KeyError("Target yield pool is not initialized.")

        self.portfolio.total_yield_earned_cents += interest_cents
        self.reserve_account_cents += interest_cents
        logger.info(f"[Investment] Accrued yield interest from {pool}: +{interest_cents} cents.")
