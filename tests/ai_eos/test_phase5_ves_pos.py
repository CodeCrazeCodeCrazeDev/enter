"""Unit tests for Phase 5 Venture Execution System (VES) & Portfolio Operating System (POS)."""

import pytest
from uuid import uuid4
from apodex.ai_eos.domain.models import VentureCell
from apodex.ai_eos.portfolio.manager import PortfolioOperatingSystem
from apodex.ai_eos.orchestration.backend import VentureExecutionSystem


def test_pos_capital_distribution():
    """Verify POS splits capital proportionally between Venture and Research based on uncertainty."""
    pos = PortfolioOperatingSystem(initial_reserves_cents=1000_000_00)  # $100k

    cell = VentureCell(name="VentureV", namespace="ns_v")

    # 1. Low uncertainty (0.15) -> Low research ratio (15%) -> Mostly Venture
    alloc_low = pos.allocate_portfolio_capital([cell], unresolved_uncertainty_score=0.15, total_allocation_cents=50000_00)
    assert alloc_low["research_portfolio_cents"] == 7500_00
    assert alloc_low["venture_portfolio_cents"] == 42500_00

    # 2. High uncertainty (0.45) -> High research ratio (45%) -> Substantial Research allocation
    alloc_high = pos.allocate_portfolio_capital([cell], unresolved_uncertainty_score=0.45, total_allocation_cents=10000_00)
    assert alloc_high["research_portfolio_cents"] == 4500_00
    assert alloc_high["venture_portfolio_cents"] == 5500_00


def test_ves_multi_timescale_planning():
    """Verify that hierarchical planning generates correct tactical/strategic scopes."""
    ves = VentureExecutionSystem()

    assert ves.plan_multi_timescale(horizon_days=1) == "EXECUTE_EXPERIMENTS"
    assert ves.plan_multi_timescale(horizon_days=10) == "GT_SPRINTS"
    assert ves.plan_multi_timescale(horizon_days=60) == "GO_NO_GO_PROGRESSION"
    assert ves.plan_multi_timescale(horizon_days=300) == "PORTFOLIO_REBALANCE"
    assert ves.plan_multi_timescale(horizon_days=720) == "STRATEGIC_DISCIPLINE"
