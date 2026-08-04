"""Unit and integration tests for the Active Learning engine."""

from __future__ import annotations

import pytest
from apodex.reasoning.active_learning import ActiveLearningEngine


def test_active_learning_loop():
    engine = ActiveLearningEngine(confidence_threshold=0.75)

    # 1. Low uncertainty (high confidence)
    entropy_low = engine.calculate_uncertainty_entropy([0.9, 0.8, 0.95])
    assert entropy_low < 0.2

    # 2. High uncertainty (low confidence)
    entropy_high = engine.calculate_uncertainty_entropy([0.3, 0.4, 0.5])
    assert entropy_high > 0.5

    # 3. Probe generation
    beliefs = [
        {"belief_id": "b1", "hypothesis": "The catalyst is platinum", "strength": 0.9},
        {"belief_id": "b2", "hypothesis": "The reaction temperature is exactly 120C", "strength": 0.4},
    ]

    probes = engine.generate_probe_queries(beliefs)
    assert len(probes) == 1
    assert "b2" in probes[0]
    assert "120C" in probes[0]
