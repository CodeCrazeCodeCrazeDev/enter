"""Governed Cognitive Evolution System (Ch 11 + 15).

The three-layer evolution framework that turns AEAN from a static architecture
into a *governed* self-improving organism:

* **Layer 1 — Capability Evolution** (:class:`CapabilityEvolution`): fast,
  lightweight evolution of behavioural strategy parameters within the fixed
  architecture (variation → measurement → selection → recombination).
* **Layer 2 — Architecture Evolution** (:class:`ArchitectureEvolution`): slow,
  heavyweight structural change through a mandatory seven-stage governance
  pipeline (sandbox → benchmark → stress → security → economic → canary →
  scale/kill).
* **Layer 3 — Objective Stability** (:class:`ObjectiveStability`): the invariant
  constitutional parameters that never evolve automatically, enforcing the five
  categorical prohibitions before any candidate is evaluated.
"""
from __future__ import annotations

from .three_layer import (
    ArchitectureEvolution,
    CapabilityEvolution,
    GovernedCognitiveEvolutionSystem,
    ObjectiveStability,
)

__all__ = [
    "ObjectiveStability",
    "CapabilityEvolution",
    "ArchitectureEvolution",
    "GovernedCognitiveEvolutionSystem",
]
