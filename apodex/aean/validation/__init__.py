"""Reality & validation systems for AEAN v2 (Part II of the architecture).

This package implements the subsystems that sit between raw generation and
economic action, ensuring the organism spends capital only on outputs that are
grounded in reality:

* :class:`~apodex.aean.validation.perception.PerceptionPredictor` — a TRIBEv2
  stand-in predicting the four dimensions of audience response, plus a
  :class:`~apodex.aean.validation.perception.CalibrationLayer` that learns which
  perception signals actually convert.
* :class:`~apodex.aean.validation.rgae.RealityGroundedAdaptiveEngine` — the
  three-layer creative-validation pipeline (simulation filter → controlled
  reality test → revenue gate).
* :class:`~apodex.aean.validation.critics.ThreeCriticStack` — the Truth / Policy
  / Strategy critics that review every economic action before execution.
* :class:`~apodex.aean.validation.epistemic.EpistemicFirewall` — reality
  validation of inbound demand signals via oracle verification, cross-source
  consensus and adversarial red-teaming.
"""
from __future__ import annotations

from .critics import ThreeCriticStack
from .epistemic import EpistemicFirewall
from .perception import CalibrationLayer, PerceptionPredictor
from .rgae import RealityGroundedAdaptiveEngine

__all__ = [
    "PerceptionPredictor",
    "CalibrationLayer",
    "RealityGroundedAdaptiveEngine",
    "ThreeCriticStack",
    "EpistemicFirewall",
]
