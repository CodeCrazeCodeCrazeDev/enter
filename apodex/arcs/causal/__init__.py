"""Causal Intelligence core for ARCS / AEAN OS.

Provides structural causal graph representation, Wright path propagation,
counterfactual reasoning, and active inference.
"""

from __future__ import annotations

from .causal_engine import CausalIntelligenceEngine
from .active_inference import ActiveInferenceEngine

__all__ = ["CausalIntelligenceEngine", "ActiveInferenceEngine"]
