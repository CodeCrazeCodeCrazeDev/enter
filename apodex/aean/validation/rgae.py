"""RGAE — Reality-Grounded Adaptive Engine (AEAN v2, Chapter 8).

The RGAE prevents the *engagement trap*: creative that maximises attention but
destroys profitability. It is a graduated three-layer filtration pipeline where
each layer applies a successively stricter filter against economic value:

* **Layer 1 — TRIBE Simulation Filter.** Every variant is scored by the
  :class:`~apodex.aean.validation.perception.PerceptionPredictor` and ranked by
  a calibrated conversion-propensity value. Only the strongest variants (with
  acceptable cognitive load) survive; nothing else consumes media budget.
* **Layer 2 — Controlled Reality Testing.** Survivors receive a simulated
  micro-budget live test. Observed click-through is drawn around the predicted
  rate with segment noise, catching "in-silico winners that fail in vivo".
* **Layer 3 — Revenue Validation Gate.** Only assets proving positive unit
  economics (LTV/CPA ≥ target) advance. Engagement rate is explicitly rejected
  as a terminal objective.

Every asset that flows through the pipeline produces a
:class:`~apodex.aean.models.ValidationRecord`; the prediction/outcome pair is
fed back into the :class:`CalibrationLayer` so the organism's model of "what
actually converts" improves over time.
"""
from __future__ import annotations

import logging
import math
import random
from typing import List, Optional

from ..models import (
    DemandSignal,
    Narrative,
    PerceptionScore,
    ValidationRecord,
    ValidationStage,
    VisualAsset,
)
from .perception import CalibrationLayer, PerceptionPredictor

logger = logging.getLogger("aean.rgae")


class RealityGroundedAdaptiveEngine:
    """Three-layer creative validation gating spend on economic reality."""

    def __init__(
        self,
        *,
        rng: Optional[random.Random] = None,
        predictor: Optional[PerceptionPredictor] = None,
        calibration: Optional[CalibrationLayer] = None,
        keep_fraction: float = 0.5,
        max_cognitive_load: float = 0.80,
        min_calibrated_value: float = 0.40,
        min_reality_ctr_ratio: float = 0.80,
        target_ltv_cpa: float = 3.0,
        cpm_cents: float = 800.0,
        base_margin_cents: float = 1800.0,
    ) -> None:
        self._rng = rng or random.Random()
        self.predictor = predictor or PerceptionPredictor()
        self.calibration = calibration or CalibrationLayer()
        self.keep_fraction = keep_fraction
        self.max_cognitive_load = max_cognitive_load
        self.min_calibrated_value = min_calibrated_value
        self.min_reality_ctr_ratio = min_reality_ctr_ratio
        self.target_ltv_cpa = target_ltv_cpa
        self.cpm_cents = cpm_cents
        self.base_margin_cents = base_margin_cents

    # ------------------------------------------------------------------
    def screen(
        self,
        narrative: Narrative,
        assets: List[VisualAsset],
        signal: DemandSignal,
    ) -> List[ValidationRecord]:
        """Run ``assets`` through all three layers, returning one record each."""
        if not assets:
            return []
        segment = signal.segment

        scored: List[tuple[VisualAsset, PerceptionScore, float]] = []
        for asset in assets:
            perception = self.predictor.predict(narrative, asset, rng=self._rng)
            value = self.calibration.value(perception, segment)
            scored.append((asset, perception, value))
        scored.sort(key=lambda t: t[2], reverse=True)

        # Layer 1 keeps the top slice by calibrated value.
        keep_n = max(1, math.ceil(len(scored) * self.keep_fraction))
        records: List[ValidationRecord] = []
        for rank, (asset, perception, value) in enumerate(scored):
            record = ValidationRecord(
                asset_id=asset.asset_id,
                narrative_id=narrative.narrative_id,
                segment=segment,
                perception=perception,
                calibrated_value=round(value, 4),
                predicted_ctr=asset.predicted_ctr,
                stage_reached=ValidationStage.SIMULATION,
            )
            survives_l1 = (
                rank < keep_n
                and perception.cognitive_load <= self.max_cognitive_load
                and value >= self.min_calibrated_value
            )
            if not survives_l1:
                record.stage_reached = ValidationStage.REJECTED
                record.notes.append(
                    f"Layer 1: value={value:.2f} load={perception.cognitive_load:.2f} rank={rank} — rejected."
                )
                records.append(record)
                continue

            # Layer 2: controlled reality test.
            record.stage_reached = ValidationStage.REALITY_TEST
            observed = self._reality_test(asset, perception, segment)
            record.observed_ctr = round(observed, 5)
            # Feed the prediction/reality pair back into calibration.
            reward = min(1.0, observed / max(asset.predicted_ctr, 1e-6))
            self.calibration.update(perception, segment, min(1.0, reward))
            if observed < asset.predicted_ctr * self.min_reality_ctr_ratio:
                record.stage_reached = ValidationStage.REJECTED
                record.notes.append(
                    f"Layer 2: observed CTR {observed:.4f} < {self.min_reality_ctr_ratio:.0%} of predicted — false positive."
                )
                records.append(record)
                continue

            # Layer 3: revenue validation gate (unit economics).
            ltv_cpa = self._ltv_cpa(observed, perception, signal)
            record.ltv_cpa_ratio = round(ltv_cpa, 3)
            record.stage_reached = ValidationStage.REVENUE_GATE
            if ltv_cpa < self.target_ltv_cpa:
                record.stage_reached = ValidationStage.REJECTED
                record.notes.append(
                    f"Layer 3: LTV/CPA {ltv_cpa:.2f} < target {self.target_ltv_cpa:.1f} — value-destroying, terminated."
                )
                records.append(record)
                continue

            record.stage_reached = ValidationStage.PASSED
            record.passed = True
            record.notes.append(f"Passed all layers: value={value:.2f} obs_ctr={observed:.4f} ltv/cpa={ltv_cpa:.2f}.")
            records.append(record)

        passed = sum(1 for r in records if r.passed)
        logger.debug("RGAE screened %d assets for %s: %d passed", len(assets), segment, passed)
        return records

    # ------------------------------------------------------------------
    def _reality_test(self, asset: VisualAsset, perception: PerceptionScore, segment: str) -> float:
        """Simulate a micro-budget live test, returning an observed CTR.

        The observed rate is centred on the predicted CTR for genuine creatives
        but decays for *attention decoys* — assets whose attention far exceeds
        their engagement likelihood. This reproduces the reality gap in which
        content that "predicted well in silico fails in vivo".
        """
        decoy_penalty = perception.engagement_likelihood - perception.attention  # <=0 for decoys
        realism = max(0.4, min(1.1, 1.0 + 0.6 * decoy_penalty))
        noise = self._rng.uniform(0.9, 1.1)
        return max(0.0, asset.predicted_ctr * realism * noise)

    def _conversion_rate(self, perception: PerceptionScore, segment: str) -> float:
        """Click→conversion rate, driven by calibrated conversion propensity."""
        value = self.calibration.value(perception, segment)
        return 0.02 + 0.15 * value  # 2%–17%.

    def _ltv_cpa(self, observed_ctr: float, perception: PerceptionScore, signal: DemandSignal) -> float:
        """Lifetime-value-to-acquisition-cost ratio from unit economics.

        ``CPA`` is the media cost to win one customer given the funnel
        ``impression → click → conversion``; ``LTV`` is the contribution margin
        per customer, lifted by demand strength (higher-intent markets convert
        to more valuable customers). The ratio must clear ``target_ltv_cpa``.
        """
        cvr = self._conversion_rate(perception, signal.segment)
        conv_per_impression = max(1e-6, observed_ctr * cvr)
        cost_per_impression = self.cpm_cents / 1000.0
        cpa = cost_per_impression / conv_per_impression
        ltv = self.base_margin_cents * (0.6 + 1.4 * signal.strength)
        return ltv / cpa if cpa > 0 else 0.0
