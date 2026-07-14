"""The Three-Critic Stack — output governance for every economic action.

Every action the organism is about to take (spawning a micro-cell, committing
capital, scaling a winner) passes through three independent critics before
execution, as specified in the AEAN v2 architecture:

* **Truth Critic** — factual correctness. Are the projections grounded? Is the
  allocation internally consistent (positive, within the opportunity's TAM,
  expected value in a plausible range)?
* **Policy Critic** — constraint alignment. Does the action satisfy the
  immutable constitution (capital-preservation limits, reserves, brand safety)?
  This critic defers to the :class:`ConstitutionalFilter`.
* **Strategy Critic** — objective optimality. Is this the *best* use of capital
  right now, given the arm's expected value and the portfolio's opportunity
  cost?

An action is approved only if all three critics pass. Conflicts (e.g. Strategy
favours a high-EV bet the Policy critic rejects on reserve grounds) surface as
structured trade-off analysis rather than being buried in optimisation.
"""
from __future__ import annotations

import logging
import time
from typing import List, Optional

from ..governance import ConstitutionalFilter
from ..models import CriticName, CriticReview, CriticVerdict, DemandSignal, MicroCell

logger = logging.getLogger("aean.critics")


class ThreeCriticStack:
    """Truth / Policy / Strategy review stack."""

    def __init__(
        self,
        governance: ConstitutionalFilter,
        *,
        min_strategy_ev: float = 0.25,
        max_tam_fraction: float = 0.6,
    ) -> None:
        self.governance = governance
        self.min_strategy_ev = min_strategy_ev
        self.max_tam_fraction = max_tam_fraction
        self.verdicts: List[CriticVerdict] = []
        self.blocks = 0

    # ------------------------------------------------------------------
    def review_allocation(
        self,
        cell: MicroCell,
        *,
        treasury_cents: int,
        deployed_cents: int,
        expected_value: float,
        signal: Optional[DemandSignal] = None,
    ) -> CriticVerdict:
        """Review a proposed capital allocation with all three critics."""
        started = time.perf_counter()
        reviews = [
            self._truth(cell, expected_value, signal),
            self._policy(cell, treasury_cents, deployed_cents),
            self._strategy(expected_value),
        ]
        latency_ms = (time.perf_counter() - started) * 1000.0
        approved = all(r.passed for r in reviews)
        verdict = CriticVerdict(
            action=f"allocate:{cell.market}:{cell.segment}",
            approved=approved,
            reviews=reviews,
            latency_ms=round(latency_ms, 4),
        )
        self.verdicts.append(verdict)
        if not approved:
            self.blocks += 1
            logger.info(
                "Three-Critic block on %s: %s",
                verdict.action,
                "; ".join(r.rationale for r in reviews if not r.passed),
            )
        return verdict

    # ------------------------------------------------------------------
    def _truth(self, cell: MicroCell, expected_value: float, signal: Optional[DemandSignal]) -> CriticReview:
        problems: List[str] = []
        if cell.allocated_cents <= 0:
            problems.append("allocation is non-positive")
        if not (0.0 <= expected_value <= 1.0):
            problems.append(f"expected value {expected_value:.2f} outside [0,1]")
        if signal is not None and signal.estimated_tam_cents > 0:
            frac = cell.allocated_cents / signal.estimated_tam_cents
            if frac > self.max_tam_fraction:
                problems.append(
                    f"allocation is {frac:.0%} of estimated TAM (> {self.max_tam_fraction:.0%})"
                )
        passed = not problems
        score = 1.0 if passed else max(0.0, 1.0 - 0.4 * len(problems))
        return CriticReview(
            critic=CriticName.TRUTH,
            passed=passed,
            score=round(score, 4),
            rationale="grounded projection" if passed else "; ".join(problems),
        )

    def _policy(self, cell: MicroCell, treasury_cents: int, deployed_cents: int) -> CriticReview:
        verdict = self.governance.review_allocation(
            amount_cents=cell.allocated_cents,
            treasury_cents=treasury_cents,
            currently_deployed_cents=deployed_cents,
        )
        return CriticReview(
            critic=CriticName.POLICY,
            passed=verdict.approved,
            score=1.0 if verdict.approved else 0.0,
            rationale="constitution satisfied" if verdict.approved else "; ".join(verdict.reasons),
        )

    def _strategy(self, expected_value: float) -> CriticReview:
        passed = expected_value >= self.min_strategy_ev
        return CriticReview(
            critic=CriticName.STRATEGY,
            passed=passed,
            score=round(max(0.0, min(1.0, expected_value)), 4),
            rationale=(
                f"EV {expected_value:.2f} clears bar {self.min_strategy_ev:.2f}"
                if passed
                else f"EV {expected_value:.2f} below opportunity-cost bar {self.min_strategy_ev:.2f}"
            ),
        )

    # ------------------------------------------------------------------
    def stats(self) -> dict:
        total = len(self.verdicts)
        approved = sum(1 for v in self.verdicts if v.approved)
        avg_latency = sum(v.latency_ms for v in self.verdicts) / total if total else 0.0
        return {
            "reviews": total,
            "approved": approved,
            "blocked": self.blocks,
            "avg_latency_ms": round(avg_latency, 4),
        }
