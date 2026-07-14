"""Simulation & Pre-Trade Validation Engine — the gate before capital.

Every capital deployment is a bet on a compressed future. Before AEAN commits a
single dollar to a demand signal, this engine asks one dispositive question:
*should we even try this?* It follows the three-part architecture from Ch 10 of
the AEAN v2 spec:

1. **The four-pillar gate** — a hypothesis is screened against four evidence
   pillars (addressable demand size, customer-acquisition-cost efficiency,
   conversion-probability band and competition intensity). A hypothesis missing
   any pillar, or carrying a pillar scored below threshold, is rejected *without
   simulation* — cheap rejection first, expensive simulation only for survivors.
2. **Synthetic testing** — survivors are run through a Monte-Carlo simulation of
   the unit economics. A hypothesis passes only if its 5th-percentile outcome
   clears the minimum-return threshold, forecast variance is acceptable, and no
   draw implies an unrecoverable loss.
3. **Counterfactual evaluation** — three what-if probes: *pillar removal* (does
   the thesis collapse without any single pillar?), *condition perturbation*
   (do ±20% shocks surface hidden convexities?) and *opposite-narrative
   injection* (does the thesis have discriminatory power at all?).

The engine is deliberately conservative but not paralysing: strong, cheap,
uncontested demand clears easily, while weak/expensive/crowded opportunities are
filtered before they can consume capital.
"""
from __future__ import annotations

import logging
import random
import statistics
from typing import List, Optional

from ..models import DemandSignal, EvidencePillar, PreTradeAssessment

logger = logging.getLogger("aean.pretrade")

_TAM_REFERENCE_CENTS = 100_000_000.0  # $1M — normalisation anchor for demand size.


class PreTradeValidationEngine:
    """Four-pillar gate + Monte-Carlo synthetic test + counterfactual probes."""

    def __init__(
        self,
        *,
        rng: Optional[random.Random] = None,
        min_tam_cents: int = 15_000_000,
        min_ltv_cac: float = 1.05,
        min_conversion_strength: float = 0.40,
        max_competition: float = 0.85,
        n_sims: int = 256,
        min_sim_p05: float = -0.60,
        max_sim_cv: float = 1.5,
        ruin_floor: float = -0.95,
        max_fragility: float = 0.60,
        min_divergence: float = 0.05,
    ) -> None:
        self._rng = rng or random.Random()
        self.min_tam_cents = min_tam_cents
        self.min_ltv_cac = min_ltv_cac
        self.min_conversion_strength = min_conversion_strength
        self.max_competition = max_competition
        self.n_sims = n_sims
        self.min_sim_p05 = min_sim_p05
        self.max_sim_cv = max_sim_cv
        self.ruin_floor = ruin_floor
        self.max_fragility = max_fragility
        self.min_divergence = min_divergence

        self.assessed = 0
        self.rejected = 0
        self.gate_rejections = 0
        self.sim_rejections = 0
        self.counterfactual_rejections = 0

    # ------------------------------------------------------------------
    def assess(self, signal: DemandSignal) -> PreTradeAssessment:
        self.assessed += 1
        notes: List[str] = []
        competition = self._competition(signal)
        pillars = self._pillars(signal, competition, notes)
        gate_passed = all(p.passed for p in pillars)

        assessment = PreTradeAssessment(
            signal_id=signal.signal_id,
            market=signal.market,
            segment=signal.segment,
            pillars=pillars,
            gate_passed=gate_passed,
        )

        if not gate_passed:
            failed = [p.name for p in pillars if not p.passed]
            notes.append(f"Gate: rejected without simulation (pillars failed: {', '.join(failed)}).")
            self.gate_rejections += 1
            self.rejected += 1
            assessment.notes = notes
            return assessment

        notes.append("Gate: all four evidence pillars cleared.")

        # Layer 2 — synthetic testing via Monte-Carlo unit economics.
        mean_return = self._expected_return(signal, competition)
        sigma = self._return_sigma(signal, competition)
        outcomes = [
            max(-1.0, self._rng.gauss(mean_return, sigma)) for _ in range(self.n_sims)
        ]
        sim_mean = statistics.fmean(outcomes)
        sim_std = statistics.pstdev(outcomes)
        p05 = self._percentile(outcomes, 0.05)
        cv = sim_std / abs(sim_mean) if abs(sim_mean) > 1e-9 else float("inf")
        worst = min(outcomes)
        sim_passed = (
            p05 >= self.min_sim_p05 and cv <= self.max_sim_cv and worst > self.ruin_floor
        )
        assessment.sim_p05 = round(p05, 4)
        assessment.sim_mean = round(sim_mean, 4)
        assessment.sim_cv = round(cv, 4) if cv != float("inf") else 999.0
        assessment.sim_passed = sim_passed
        notes.append(
            f"Synthetic test: mean {sim_mean:+.3f}, p05 {p05:+.3f}, CV {assessment.sim_cv:.2f}, worst {worst:+.3f}."
        )
        if not sim_passed:
            notes.append("Synthetic test: failed (tail risk or variance too high).")
            self.sim_rejections += 1
            self.rejected += 1
            assessment.notes = notes
            return assessment

        # Layer 3 — counterfactual evaluation.
        fragility, discriminatory, perturbation_ok = self._counterfactual(
            signal, competition, pillars, mean_return, notes
        )
        cf_passed = (
            fragility <= self.max_fragility and discriminatory and perturbation_ok
        )
        assessment.fragility_index = round(fragility, 4)
        assessment.discriminatory = discriminatory
        assessment.counterfactual_passed = cf_passed
        if not cf_passed:
            self.counterfactual_rejections += 1
            self.rejected += 1

        assessment.passed = gate_passed and sim_passed and cf_passed
        assessment.notes = notes
        return assessment

    # ------------------------------------------------------------------
    def _competition(self, signal: DemandSignal) -> float:
        """Heuristic competition-intensity score in ``[0, 1]`` (higher = worse)."""
        comp = 0.20
        if "competitor_move" in signal.keywords:
            comp += 0.30
        comp += 0.15 * min(1.0, signal.estimated_tam_cents / 250_000_000.0)  # bigger = contested.
        comp += 0.20 * (1.0 - signal.strength)  # undifferentiated demand is crowded.
        return max(0.0, min(1.0, comp))

    def _ltv_index(self, signal: DemandSignal) -> float:
        return 0.30 + 0.70 * signal.strength

    def _cac_index(self, competition: float) -> float:
        return 0.30 + 0.60 * competition

    def _pillars(
        self, signal: DemandSignal, competition: float, notes: List[str]
    ) -> List[EvidencePillar]:
        # 1. Addressable demand size.
        demand_score = min(1.0, signal.estimated_tam_cents / _TAM_REFERENCE_CENTS)
        demand = EvidencePillar(
            name="demand_size",
            score=round(demand_score, 4),
            passed=signal.estimated_tam_cents >= self.min_tam_cents,
            detail=f"TAM ${signal.estimated_tam_cents / 100:,.0f}",
        )
        # 2. CAC efficiency (LTV/CAC).
        ltv_cac = self._ltv_index(signal) / self._cac_index(competition)
        cac = EvidencePillar(
            name="cac_efficiency",
            score=round(min(1.0, ltv_cac / 2.0), 4),
            passed=ltv_cac >= self.min_ltv_cac,
            detail=f"LTV/CAC {ltv_cac:.2f}",
        )
        # 3. Conversion-probability band (demand conviction).
        conv = EvidencePillar(
            name="conversion_band",
            score=round(signal.strength, 4),
            passed=signal.strength >= self.min_conversion_strength,
            detail=f"conviction {signal.strength:.2f}",
        )
        # 4. Competition intensity (lower is better).
        comp_pillar = EvidencePillar(
            name="competition_intensity",
            score=round(1.0 - competition, 4),
            passed=competition <= self.max_competition,
            detail=f"intensity {competition:.2f}",
        )
        return [demand, cac, conv, comp_pillar]

    def _expected_return(self, signal: DemandSignal, competition: float) -> float:
        """Expected unit-economics return, net of competition drag."""
        ltv_cac = self._ltv_index(signal) / self._cac_index(competition)
        return (ltv_cac - 1.0) * (1.0 - 0.5 * competition)

    def _return_sigma(self, signal: DemandSignal, competition: float) -> float:
        """Forecast dispersion — wider for weak conviction and crowded markets."""
        return 0.18 + 0.30 * (1.0 - signal.strength) + 0.20 * competition

    def _counterfactual(
        self,
        signal: DemandSignal,
        competition: float,
        pillars: List[EvidencePillar],
        mean_return: float,
        notes: List[str],
    ) -> tuple[float, bool, bool]:
        scores = [p.score for p in pillars]
        base_viability = sum(scores) / len(scores)

        # Pillar removal — the thesis should not hinge on a single pillar.
        max_drop = 0.0
        for i in range(len(scores)):
            reduced = (sum(scores) - scores[i]) / len(scores)
            max_drop = max(max_drop, base_viability - reduced)
        fragility = max_drop / base_viability if base_viability > 1e-9 else 1.0

        # Condition perturbation — ±20% shocks must not imply unrecoverable loss.
        perturbation_ok = True
        for factor in (0.8, 1.2):
            shocked = DemandSignal(
                market=signal.market,
                segment=signal.segment,
                strength=max(0.0, min(1.0, signal.strength * factor)),
                estimated_tam_cents=signal.estimated_tam_cents,
                elasticity=signal.elasticity * factor,
                keywords=signal.keywords,
            )
            shocked_return = self._expected_return(shocked, self._competition(shocked))
            if shocked_return <= self.ruin_floor:
                perturbation_ok = False
        if not perturbation_ok:
            notes.append("Counterfactual: ±20% shock implies unrecoverable loss.")

        # Opposite-narrative injection — invert conviction, require divergence.
        inverse = DemandSignal(
            market=signal.market,
            segment=signal.segment,
            strength=max(0.0, min(1.0, 1.0 - signal.strength)),
            estimated_tam_cents=signal.estimated_tam_cents,
            elasticity=signal.elasticity,
            keywords=signal.keywords,
        )
        inverse_return = self._expected_return(inverse, self._competition(inverse))
        divergence = abs(mean_return - inverse_return)
        discriminatory = divergence >= self.min_divergence

        notes.append(
            f"Counterfactual: fragility {fragility:.2f}, opposite-narrative divergence {divergence:.3f}"
            + ("" if discriminatory else " — lacks discriminatory power.")
        )
        return fragility, discriminatory, perturbation_ok

    @staticmethod
    def _percentile(values: List[float], q: float) -> float:
        if not values:
            return 0.0
        ordered = sorted(values)
        idx = max(0, min(len(ordered) - 1, int(q * (len(ordered) - 1))))
        return ordered[idx]

    # ------------------------------------------------------------------
    def stats(self) -> dict:
        return {
            "assessed": self.assessed,
            "rejected": self.rejected,
            "approved": self.assessed - self.rejected,
            "gate_rejections": self.gate_rejections,
            "sim_rejections": self.sim_rejections,
            "counterfactual_rejections": self.counterfactual_rejections,
        }
