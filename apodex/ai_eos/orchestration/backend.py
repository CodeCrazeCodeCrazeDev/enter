"""Execution Subsystem Orchestration Adapters and Venture Execution System (VES) for SERO v2.

Wires the existing AEAN Organism and ARCS systems behind stable decoupled interfaces,
and manages hierarchical multi-timescale planning.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, Optional, List
from uuid import UUID

from ..interfaces.services import IExecutionBackend
from ...aean.flywheel import Organism

logger = logging.getLogger("sero.ves")


class ExecutionBackendAdapter(IExecutionBackend):
    """Adapter to orchestrate the existing AEAN Organism flywheel as a replaceable backend."""

    def __init__(self, organism: Optional[Organism] = None) -> None:
        # Lazy initialize or accept pre-built Organism
        self._organism = organism or Organism(initial_capital_cents=100_000_00)

    def run_cycle(self, cell_id: UUID, capital_cents: int) -> Dict[str, Any]:
        """Drive a physical or simulated flywheel execution run of the AEAN Organism."""
        logger.info(f"Dispatching execution run to AEAN Organism backend for cell {cell_id} with budget ${capital_cents/100:.2f}")

        # Sync capital allocations configurationally if needed
        self._organism.treasury_cents = max(self._organism.treasury_cents, capital_cents)

        # Run a cycle step of the compounding flywheel
        cycle_result = self._organism.step()

        # Translate cycle results to clean AI-EOS metrics
        translated_metrics = {
            "cell_id": cell_id,
            "cycle_number": cycle_result.cycle,
            "capital_deployed_cents": cycle_result.capital_deployed_cents,
            "earned_revenue_cents": cycle_result.revenue_cents,
            "signals_detected": cycle_result.signals_detected,
            "active_cells": cycle_result.active_cells,
            "cells_killed": cycle_result.cells_killed,
            "cells_scaled": cycle_result.cells_scaled
        }

        logger.info(f"AEAN Organism step completed: Deploy = ${cycle_result.capital_deployed_cents/100:.2f}, Rev = ${cycle_result.revenue_cents/100:.2f}")
        return translated_metrics


class VentureExecutionSystem:
    """Consumes KOS theories and manages hierarchical multi-timescale venture planning."""

    def __init__(self) -> None:
        pass

    def plan_multi_timescale(self, horizon_days: int) -> str:
        """Resolve planning task types according to explicit timescale hierarchies."""
        logger.info(f"VES generating hierarchical plans for horizon: {horizon_days} days")

        if horizon_days <= 2:
            logger.info("Timescale: Hours-Days -> Active experimental execution and ad-bid adjustment.")
            return "EXECUTE_EXPERIMENTS"

        if horizon_days <= 14:
            logger.info("Timescale: Weeks -> Sprint-level product iterations and GTM optimizations.")
            return "GT_SPRINTS"

        if horizon_days <= 90:
            logger.info("Timescale: Months -> Venture cell go/no-go progression and capital adjustments.")
            return "GO_NO_GO_PROGRESSION"

        if horizon_days <= 365:
            logger.info("Timescale: Years -> Portfolio rebalancing and macro-geography sequencing.")
            return "PORTFOLIO_REBALANCE"

        logger.info("Timescale: Multi-year -> Organizational capability and research discipline updates.")
        return "STRATEGIC_DISCIPLINE"
