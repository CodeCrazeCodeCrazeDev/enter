from __future__ import annotations
import logging
from typing import Any, Dict

logger = logging.getLogger("arcs.capital")


class CapitalAllocationEngine:
    """Constrained optimization capital engine distributing budgets dynamically based on department yields."""

    def __init__(self, initial_reserves_cents: int) -> None:
        self.reserves_cents = initial_reserves_cents

    def optimize_allocations(self, department_scores: Dict[str, float], total_to_allocate_cents: int) -> Dict[str, int]:
        """Distribute a target capital amount across departments proportionally based on performance scores."""
        logger.info(f"Optimizing capital allocation. Reserves: {self.reserves_cents} cents. Allocating: {total_to_allocate_cents} cents.")
        if total_to_allocate_cents > self.reserves_cents:
            logger.warning("Allocation amount exceeds available capital reserves! Capping to available reserves.")
            total_to_allocate_cents = self.reserves_cents

        if not department_scores:
            return {}

        total_score = sum(department_scores.values())
        if total_score <= 0:
            # Equal distribution if all scores are zero/negative
            equal_share = total_to_allocate_cents // len(department_scores)
            return {dept: equal_share for dept in department_scores}

        allocations = {}
        allocated_so_far = 0
        departments = list(department_scores.keys())

        for idx, dept in enumerate(departments):
            if idx == len(departments) - 1:
                # Assign remainder to last department to prevent rounding loss
                allocations[dept] = total_to_allocate_cents - allocated_so_far
            else:
                share_pct = department_scores[dept] / total_score
                dept_share = int(total_to_allocate_cents * share_pct)
                allocations[dept] = dept_share
                allocated_so_far += dept_share

        # Deduct allocated capital from core reserves
        self.reserves_cents -= total_to_allocate_cents
        logger.info(f"Capital allocation optimized: {allocations}. Remaining reserves: {self.reserves_cents} cents.")
        return allocations
