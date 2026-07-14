"""Epistemic firewall — reality validation for inbound demand signals.

Unconstrained ingestion of external signal is a lethal vulnerability: belief
contamination propagates through decision chains at the speed of inference. The
:class:`EpistemicFirewall` implements the three-layer reality-validation system
from the AEAN v2 architecture, filtering every demand signal before it is
allowed to enter the reasoning pipeline (and the EKG):

1. **Oracle verification** — the signal is checked against known priors: is its
   strength, price elasticity and addressable-market estimate within physically
   plausible ranges?
2. **Cross-source consensus** — the raw source readings must corroborate. A
   single hot source is not a signal; independent sources must agree.
3. **Adversarial red-teaming** — the firewall probes for manipulation, e.g. an
   extreme headline strength that is not backed by consensus (a classic
   pump/astroturf pattern), or banned promotional language in the keywords.

The three layers combine with a temporal-decay factor into a single
``credibility`` score; a signal passes only if all layers clear and credibility
meets the threshold.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional, Sequence

from ..governance import ConstitutionalFilter
from ..models import DemandSignal, SignalValidation

logger = logging.getLogger("aean.epistemic")


class EpistemicFirewall:
    """Three-layer reality validation of demand signals."""

    def __init__(
        self,
        *,
        governance: Optional[ConstitutionalFilter] = None,
        min_consensus_sources: int = 2,
        consensus_threshold: float = 0.35,
        min_credibility: float = 0.45,
        max_staleness_seconds: float = 3600.0,
    ) -> None:
        self.governance = governance
        self.min_consensus_sources = min_consensus_sources
        self.consensus_threshold = consensus_threshold
        self.min_credibility = min_credibility
        self.max_staleness_seconds = max_staleness_seconds
        self.rejected = 0

    # ------------------------------------------------------------------
    def validate(
        self,
        signal: DemandSignal,
        readings: Sequence[float],
        *,
        now: Optional[datetime] = None,
    ) -> SignalValidation:
        notes: List[str] = []

        oracle_ok, oracle_score = self._oracle(signal, notes)
        consensus_ok, corroborating, consensus_score = self._consensus(readings, notes)
        red_team_ok, red_team_score = self._red_team(signal, readings, corroborating, notes)
        decay = self._temporal_decay(signal, now, notes)

        credibility = round(
            decay * (0.35 * oracle_score + 0.35 * consensus_score + 0.30 * red_team_score), 4
        )
        passed = oracle_ok and consensus_ok and red_team_ok and credibility >= self.min_credibility
        if not passed:
            self.rejected += 1

        return SignalValidation(
            signal_id=signal.signal_id,
            passed=passed,
            credibility=credibility,
            oracle_ok=oracle_ok,
            consensus_ok=consensus_ok,
            red_team_ok=red_team_ok,
            corroborating_sources=corroborating,
            notes=notes,
        )

    # ------------------------------------------------------------------
    def _oracle(self, signal: DemandSignal, notes: List[str]) -> tuple[bool, float]:
        problems: List[str] = []
        if not (0.0 <= signal.strength <= 1.0):
            problems.append("strength outside [0,1]")
        # Demand curves slope down: elasticity must be negative and finite.
        if not (-5.0 <= signal.elasticity < 0.0):
            problems.append(f"implausible elasticity {signal.elasticity}")
        if signal.estimated_tam_cents <= 0:
            problems.append("non-positive TAM")
        ok = not problems
        if ok:
            notes.append("Oracle: priors consistent.")
        else:
            notes.append("Oracle: " + "; ".join(problems))
        return ok, 1.0 if ok else 0.0

    def _consensus(self, readings: Sequence[float], notes: List[str]) -> tuple[bool, int, float]:
        corroborating = sum(1 for r in readings if r >= self.consensus_threshold)
        ok = corroborating >= self.min_consensus_sources
        score = corroborating / len(readings) if readings else 0.0
        notes.append(
            f"Consensus: {corroborating}/{len(readings)} sources above {self.consensus_threshold:.2f}"
            + (" — corroborated." if ok else " — insufficient.")
        )
        return ok, corroborating, round(score, 4)

    def _red_team(
        self,
        signal: DemandSignal,
        readings: Sequence[float],
        corroborating: int,
        notes: List[str],
    ) -> tuple[bool, float]:
        suspicious: List[str] = []
        # Pump/astroturf: a very strong headline unsupported by broad consensus.
        if signal.strength >= 0.85 and corroborating < max(self.min_consensus_sources, len(readings) // 2 + 1):
            suspicious.append("high strength without broad corroboration (possible astroturf)")
        # Dispersion attack: one source spikes while the rest are silent.
        if readings and (max(readings) - min(readings)) > 0.8 and corroborating <= 1:
            suspicious.append("single-source spike (possible manipulation)")
        # Brand-safety on keywords, if a constitution is available.
        if self.governance is not None and signal.keywords:
            verdict = self.governance.review_content(" ".join(signal.keywords))
            if not verdict.approved:
                suspicious.append("keywords tripped brand-safety filter")
        ok = not suspicious
        if ok:
            notes.append("Red-team: no manipulation detected.")
        else:
            notes.append("Red-team: " + "; ".join(suspicious))
        return ok, 1.0 if ok else 0.0

    def _temporal_decay(self, signal: DemandSignal, now: Optional[datetime], notes: List[str]) -> float:
        now = now or datetime.utcnow()
        age = max(0.0, (now - signal.detected_at).total_seconds())
        if self.max_staleness_seconds <= 0:
            return 1.0
        decay = max(0.0, 1.0 - age / self.max_staleness_seconds)
        if decay < 1.0:
            notes.append(f"Temporal decay: signal age {age:.0f}s → factor {decay:.2f}.")
        return decay
