"""PAEAN — Portfolio and Economic Allocation Network.

PAEAN is the organism's financial brain. It uses Thompson Sampling
(a Bayesian multi-armed bandit) as the *universal allocation logic*: each
demand signal is an "arm" whose payoff distribution is learned from realised
ROI. PAEAN samples from every arm's posterior, allocates bounded capital to the
most promising arms by spawning micro-cells, and then continuously reallocates —
killing losers below the ROI floor and scaling winners above the ROI ceiling.

All allocation decisions are checked against the :class:`ConstitutionalFilter`
before capital moves, and every write is persisted to the Economic Knowledge
Graph so the rest of the organism can read PAEAN's decisions in real time.
"""
from __future__ import annotations

import logging
import random
from typing import Dict, List, Optional

from ..ekg import EconomicKnowledgeGraph
from ..governance import ConstitutionalFilter
from ..models import DemandSignal, EngineName, MicroCell, MicroCellStatus
from ..validation.critics import ThreeCriticStack

logger = logging.getLogger("aean.paean")


class ThompsonBandit:
    """A Beta-Bernoulli Thompson Sampling bandit over named arms.

    Each arm tracks a Beta(alpha, beta) posterior over its "success"
    probability. ``sample`` draws a value per arm; ``update`` folds an observed
    reward in ``[0, 1]`` into the posterior. This is the classic
    exploration/exploitation-optimal Bayesian approach referenced throughout the
    AEAN spec.
    """

    def __init__(self, prior_alpha: float = 1.0, prior_beta: float = 1.0, rng: Optional[random.Random] = None) -> None:
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        self._rng = rng or random.Random()
        self.alpha: Dict[str, float] = {}
        self.beta: Dict[str, float] = {}

    def register(self, arm: str) -> None:
        self.alpha.setdefault(arm, self.prior_alpha)
        self.beta.setdefault(arm, self.prior_beta)

    def sample(self, arm: str) -> float:
        self.register(arm)
        return self._rng.betavariate(self.alpha[arm], self.beta[arm])

    def rank(self, arms: List[str]) -> List[str]:
        """Return arms ordered by a fresh posterior sample (best first)."""
        return sorted(arms, key=self.sample, reverse=True)

    def update(self, arm: str, reward: float) -> None:
        """Fold a reward in [0, 1] into the arm's posterior."""
        self.register(arm)
        reward = max(0.0, min(1.0, reward))
        self.alpha[arm] += reward
        self.beta[arm] += 1.0 - reward

    def expected_value(self, arm: str) -> float:
        self.register(arm)
        return self.alpha[arm] / (self.alpha[arm] + self.beta[arm])


class PAEAN:
    """Capital allocation and market intelligence engine."""

    def __init__(
        self,
        ekg: EconomicKnowledgeGraph,
        governance: ConstitutionalFilter,
        *,
        rng: Optional[random.Random] = None,
        max_cells_per_cycle: int = 3,
        base_allocation_pct: float = 0.15,
        max_scales: int = 3,
        max_active_cells: int = 12,
        critics: Optional[ThreeCriticStack] = None,
    ) -> None:
        self.ekg = ekg
        self.governance = governance
        self.critics = critics
        self._rng = rng or random.Random()
        self.bandit = ThompsonBandit(rng=self._rng)
        self.max_cells_per_cycle = max_cells_per_cycle
        self.base_allocation_pct = base_allocation_pct
        self.max_scales = max_scales
        self.max_active_cells = max_active_cells

    # ------------------------------------------------------------------
    def _arm_key(self, signal: DemandSignal) -> str:
        return f"{signal.market}:{signal.segment}"

    def spawn_cells(self, treasury_cents: int) -> List[MicroCell]:
        """Spawn micro-cells against the most promising open demand signals.

        ``treasury_cents`` is the *live* capital pool. Each approved allocation
        is a commitment carved out of that pool, so the running balance shrinks
        as cells are funded — the governance reserve/deploy limits therefore
        cap the number of cells that can be funded in one cycle. The caller is
        responsible for subtracting :attr:`MicroCell.allocated_cents` (summed)
        from its treasury.
        """
        open_signals = self.ekg.open_signals()
        if not open_signals:
            return []

        # Respect the portfolio-size ceiling: only fund up to the number of
        # free slots, forcing PAEAN to back its highest-conviction arms.
        free_slots = self.max_active_cells - len(self.ekg.active_cells())
        if free_slots <= 0:
            return []

        # Rank signals by a Thompson sample of their arm, weighted by strength.
        for sig in open_signals:
            self.bandit.register(self._arm_key(sig))

        scored = sorted(
            open_signals,
            key=lambda s: self.bandit.sample(self._arm_key(s)) * (0.5 + 0.5 * s.strength),
            reverse=True,
        )

        spawned: List[MicroCell] = []
        committed = 0
        for sig in scored[: min(self.max_cells_per_cycle, free_slots)]:
            ev = self.bandit.expected_value(self._arm_key(sig))
            # Allocation scales with posterior EV and signal strength.
            amount = int(treasury_cents * self.base_allocation_pct * (0.5 + ev) * (0.5 + 0.5 * sig.strength))
            amount = max(amount, 0)
            cell = MicroCell(
                signal_id=sig.signal_id,
                market=sig.market,
                segment=sig.segment,
                status=MicroCellStatus.ACTIVE,
                allocated_cents=amount,
            )
            # Every allocation passes through the Three-Critic Stack when it is
            # attached (Truth/Policy/Strategy); otherwise the raw constitution.
            if self.critics is not None:
                verdict = self.critics.review_allocation(
                    cell,
                    treasury_cents=treasury_cents,
                    deployed_cents=committed,
                    expected_value=ev,
                    signal=sig,
                )
                self.ekg.record_critic_verdict(verdict)
                approved = verdict.approved
                reasons = [r.rationale for r in verdict.reviews if not r.passed]
            else:
                pol = self.governance.review_allocation(amount, treasury_cents, committed)
                approved = pol.approved
                reasons = pol.reasons
            if not approved:
                logger.info("PAEAN allocation blocked for %s: %s", sig.market, reasons)
                continue
            self.ekg.record_cell(cell)
            committed += amount
            spawned.append(cell)
        return spawned

    # ------------------------------------------------------------------
    def learn_from_outcomes(self) -> None:
        """Update bandit posteriors from realised micro-cell ROI."""
        for cell in self.ekg.cells.values():
            if cell.deployed_cents <= 0:
                continue
            # Map ROI onto a bounded reward via a logistic-style squash.
            reward = 1.0 / (1.0 + pow(2.718281828, -cell.roi))
            self.bandit.update(f"{cell.market}:{cell.segment}", reward)

    def rebalance(self, treasury_cents: int) -> Dict[str, int]:
        """Kill under-performers and scale winners against live treasury.

        Returns counts plus the net treasury delta: ``refund_cents`` (unspent
        capital returned by killed cells) minus ``extra_commit_cents`` (fresh
        capital committed to scaled winners).
        """
        killed = 0
        scaled = 0
        refund = 0
        extra_commit = 0
        available = treasury_cents
        for cell in self.ekg.active_cells():
            if cell.cycles_run < 1:
                continue  # Give every cell at least one cycle before judging.
            if cell.roi <= cell.kill_threshold_roi:
                unspent = max(0, cell.allocated_cents - cell.deployed_cents)
                cell.status = MicroCellStatus.KILLED
                self.ekg.record_cell(cell)
                refund += unspent
                available += unspent
                killed += 1
                self.governance.note_decision(EngineName.PAEAN, success=False)
            elif cell.roi >= cell.scale_threshold_roi and cell.scale_count < self.max_scales:
                verdict = self.governance.review_scale(cell)
                injection = int(cell.allocated_cents * 0.5)
                if verdict.approved and self.governance.review_allocation(injection, max(available, 1), 0).approved:
                    cell.allocated_cents += injection
                    cell.status = MicroCellStatus.SCALED
                    cell.scale_count += 1
                    self.ekg.record_cell(cell)
                    extra_commit += injection
                    available -= injection
                    scaled += 1
                    self.governance.note_decision(EngineName.PAEAN, success=True)
        return {"killed": killed, "scaled": scaled, "refund_cents": refund, "extra_commit_cents": extra_commit}
