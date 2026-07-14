"""TRIBEv2 perception prediction and the reality-gap calibration layer.

The :class:`PerceptionPredictor` is a lightweight, fully-offline stand-in for
Meta's TRIBEv2 tri-modal neural-simulation model described in Chapter 8 of the
AEAN v2 architecture. It maps a creative asset to four interdependent
dimensions of predicted audience response:

* **attention** — will they look? (salience-network simulation)
* **valence / arousal** — will they feel? (multimodal affective computing)
* **cognitive_load** — will they understand? (working-memory load)
* **engagement_likelihood** — will they act? (behavioural response probability)

The central risk of any simulation-based system is the *reality gap*: TRIBEv2
is trained on neural-response data, not purchase data, so it is biased toward
attention maximisation. The :class:`CalibrationLayer` closes this gap by
learning, per audience segment, which perception signals are genuinely
predictive of revenue and progressively discounting attention "decoys".
"""
from __future__ import annotations

import hashlib
import random
from typing import Dict, List, Optional

from ..models import Narrative, PerceptionScore, VisualAsset

# Relative appeal of each visual concept along (attention, arousal, load).
_CONCEPT_PROFILE: Dict[str, Dict[str, float]] = {
    "bold_typographic": {"attention": 0.80, "arousal": 0.55, "load": 0.35},
    "product_hero": {"attention": 0.72, "arousal": 0.60, "load": 0.30},
    "lifestyle_scene": {"attention": 0.65, "arousal": 0.70, "load": 0.45},
    "data_visual": {"attention": 0.55, "arousal": 0.35, "load": 0.75},
    "minimal_brand": {"attention": 0.60, "arousal": 0.40, "load": 0.20},
}
_FORMAT_ATTENTION: Dict[str, float] = {
    "social_square": 0.62,
    "story_vertical": 0.75,
    "banner_wide": 0.45,
    "thumbnail": 0.55,
}


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


class PerceptionPredictor:
    """Deterministic four-dimension perception model (TRIBEv2 stand-in)."""

    def predict(
        self,
        narrative: Narrative,
        asset: VisualAsset,
        *,
        rng: Optional[random.Random] = None,
    ) -> PerceptionScore:
        rng = rng or random.Random()
        concept = _CONCEPT_PROFILE.get(asset.concept, _CONCEPT_PROFILE["minimal_brand"])
        fmt_attn = _FORMAT_ATTENTION.get(asset.format, 0.55)

        # Attention blends concept salience, format and predicted CTR.
        attention = _clamp(
            0.5 * concept["attention"] + 0.3 * fmt_attn + 0.2 * min(1.0, asset.predicted_ctr * 8)
            + rng.uniform(-0.05, 0.05)
        )
        # Emotional response is driven by narrative resonance.
        valence = _clamp(0.35 + 0.5 * narrative.predicted_resonance + rng.uniform(-0.05, 0.05))
        arousal = _clamp(0.4 * concept["arousal"] + 0.4 * narrative.predicted_resonance + rng.uniform(-0.05, 0.1))
        # Cognitive load rises with prompt complexity; lower is better.
        prompt_penalty = min(0.3, len(asset.prompt) / 600.0)
        cognitive_load = _clamp(concept["load"] + prompt_penalty + rng.uniform(-0.05, 0.05))
        # Engagement synthesises the preceding signals, penalising overload.
        engagement = _clamp(
            0.35 * attention + 0.3 * valence + 0.2 * arousal - 0.25 * max(0.0, cognitive_load - 0.6)
            + rng.uniform(-0.04, 0.04)
        )
        return PerceptionScore(
            attention=round(attention, 4),
            valence=round(valence, 4),
            arousal=round(arousal, 4),
            cognitive_load=round(cognitive_load, 4),
            engagement_likelihood=round(engagement, 4),
        )


class CalibrationLayer:
    """Per-segment regression from perception signals to conversion propensity.

    The layer maintains a weight vector over the four perception dimensions for
    each audience segment. The prior deliberately discounts raw attention and
    over-arousal (attention decoys) and rewards positive valence, comprehension
    (low cognitive load) and engagement. Each observed prediction/outcome pair
    nudges the weights toward whatever actually correlated with revenue, so the
    model becomes "less surprised by reality" over time.
    """

    _DIMS = ("attention", "valence", "arousal", "cognitive_load", "engagement_likelihood")
    _PRIOR = {
        "attention": 0.15,
        "valence": 0.30,
        "arousal": 0.10,
        "cognitive_load": -0.35,  # High load hurts conversion.
        "engagement_likelihood": 0.45,
    }

    def __init__(self, *, learning_rate: float = 0.05) -> None:
        self.learning_rate = learning_rate
        self._weights: Dict[str, Dict[str, float]] = {}
        self.updates = 0

    def _segment_weights(self, segment: str) -> Dict[str, float]:
        return self._weights.setdefault(segment, dict(self._PRIOR))

    def value(self, perception: PerceptionScore, segment: str) -> float:
        """Calibrated conversion-propensity estimate in ``[0, 1]``."""
        w = self._segment_weights(segment)
        raw = sum(w[d] * getattr(perception, d) for d in self._DIMS)
        # Squash into [0, 1] with a logistic so weights stay interpretable.
        return _clamp(0.5 + 0.5 * _tanh(raw))

    def update(self, perception: PerceptionScore, segment: str, observed_reward: float) -> None:
        """Online gradient step toward ``observed_reward`` (a ``[0, 1]`` signal)."""
        w = self._segment_weights(segment)
        predicted = self.value(perception, segment)
        error = _clamp(observed_reward) - predicted
        for d in self._DIMS:
            w[d] += self.learning_rate * error * getattr(perception, d)
        self.updates += 1

    def weights(self, segment: str) -> Dict[str, float]:
        return dict(self._segment_weights(segment))


def _tanh(x: float) -> float:
    # Bounded, avoids importing math into hot paths for a single call.
    if x > 20:
        return 1.0
    if x < -20:
        return -1.0
    e = 2.718281828459045 ** (2 * x)
    return (e - 1) / (e + 1)


def deterministic_seed(*parts: str) -> int:
    """Stable integer seed derived from string parts (for reproducible tests)."""
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


__all__: List[str] = ["PerceptionPredictor", "CalibrationLayer", "deterministic_seed"]
