"""Constitutional governance + tiered autonomy for safe economic action.

Every economic action (spawning a cell, deploying capital, scaling a winner)
passes through the :class:`ConstitutionalFilter` before it executes. The filter
enforces hard invariants — capital-preservation limits, brand-safety checks and
per-engine autonomy tiers — and returns a structured verdict. This mirrors the
"Constitutional AI + tiered autonomy" design decision from the AEAN spec: no
engine acts unsupervised until it has earned independence through demonstrated
reliability.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from pydantic import BaseModel, Field

from .models import EngineName, MicroCell

logger = logging.getLogger("aean.governance")


class ConstitutionalRules(BaseModel):
    """Invariant boundaries the organism may never cross."""

    # Capital preservation.
    max_single_allocation_pct: float = 0.35  # No cell may take >35% of treasury.
    min_treasury_reserve_pct: float = 0.10   # Always keep >=10% of capital as reserve.
    max_total_deployed_pct: float = 0.90     # Never deploy more than 90% of treasury at once.

    # Brand safety — narratives/assets containing these are rejected.
    banned_terms: List[str] = Field(
        default_factory=lambda: ["guaranteed returns", "get rich quick", "miracle cure", "risk-free"]
    )

    # Autonomy: engines earn unsupervised operation after a track record.
    min_decisions_for_autonomy: int = 25
    min_accuracy_for_autonomy: float = 0.90


class Verdict(BaseModel):
    approved: bool
    reasons: List[str] = Field(default_factory=list)


class EngineTrackRecord(BaseModel):
    engine: EngineName
    decisions: int = 0
    successes: int = 0

    @property
    def accuracy(self) -> float:
        return self.successes / self.decisions if self.decisions else 0.0


class ConstitutionalFilter:
    """Enforces the AEAN constitution before any economic action executes."""

    def __init__(self, rules: Optional[ConstitutionalRules] = None) -> None:
        self.rules = rules or ConstitutionalRules()
        self.records: dict[EngineName, EngineTrackRecord] = {}
        self.blocks = 0

    # ------------------------------------------------------------------
    def _record(self, engine: EngineName) -> EngineTrackRecord:
        return self.records.setdefault(engine, EngineTrackRecord(engine=engine))

    def note_decision(self, engine: EngineName, success: bool) -> None:
        rec = self._record(engine)
        rec.decisions += 1
        if success:
            rec.successes += 1

    def is_autonomous(self, engine: EngineName) -> bool:
        rec = self._record(engine)
        return (
            rec.decisions >= self.rules.min_decisions_for_autonomy
            and rec.accuracy >= self.rules.min_accuracy_for_autonomy
        )

    # ------------------------------------------------------------------
    def review_allocation(self, amount_cents: int, treasury_cents: int, currently_deployed_cents: int) -> Verdict:
        reasons: List[str] = []
        if treasury_cents <= 0:
            return self._deny(["Treasury is empty; no capital to allocate."])
        if amount_cents <= 0:
            return self._deny(["Allocation must be positive."])
        if amount_cents > treasury_cents * self.rules.max_single_allocation_pct:
            reasons.append(
                f"Allocation {amount_cents} exceeds {self.rules.max_single_allocation_pct:.0%} single-cell cap."
            )
        reserve = int(treasury_cents * self.rules.min_treasury_reserve_pct)
        if treasury_cents - currently_deployed_cents - amount_cents < reserve:
            reasons.append("Allocation would breach the minimum treasury reserve.")
        if currently_deployed_cents + amount_cents > treasury_cents * self.rules.max_total_deployed_pct:
            reasons.append("Allocation would exceed the maximum total-deployed limit.")
        if reasons:
            return self._deny(reasons)
        return Verdict(approved=True)

    def review_content(self, text: str) -> Verdict:
        lowered = text.lower()
        hits = [term for term in self.rules.banned_terms if term in lowered]
        if hits:
            return self._deny([f"Content contains banned term(s): {', '.join(hits)}"])
        return Verdict(approved=True)

    def review_scale(self, cell: MicroCell) -> Verdict:
        if cell.roi < cell.scale_threshold_roi:
            return self._deny(["Cell ROI below scale threshold; scaling denied."])
        return Verdict(approved=True)

    def _deny(self, reasons: List[str]) -> Verdict:
        self.blocks += 1
        logger.info("Constitutional block: %s", "; ".join(reasons))
        return Verdict(approved=False, reasons=reasons)
