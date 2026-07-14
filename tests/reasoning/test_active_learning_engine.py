from __future__ import annotations

from apodex.reasoning.active_learning import ActiveLearningEngine


def test_default_confidence_threshold():
    assert ActiveLearningEngine().confidence_threshold == 0.75


def test_calculate_uncertainty_entropy_empty_list():
    assert ActiveLearningEngine().calculate_uncertainty_entropy([]) == 0.0


def test_calculate_uncertainty_entropy_average_of_complements():
    engine = ActiveLearningEngine()
    # (1-0.2 + 1-0.8) / 2 = (0.8 + 0.2) / 2 = 0.5
    assert engine.calculate_uncertainty_entropy([0.2, 0.8]) == 0.5


def test_calculate_uncertainty_entropy_all_certain():
    assert ActiveLearningEngine().calculate_uncertainty_entropy([1.0, 1.0]) == 0.0


def test_generate_probe_queries_only_for_uncertain_beliefs():
    engine = ActiveLearningEngine(confidence_threshold=0.75)
    beliefs = [
        {"belief_id": "b1", "hypothesis": "uncertain thing", "strength": 0.3},
        {"belief_id": "b2", "hypothesis": "confident thing", "strength": 0.9},
    ]
    probes = engine.generate_probe_queries(beliefs)
    assert len(probes) == 1
    assert "b1" in probes[0]
    assert "uncertain thing" in probes[0]


def test_generate_probe_queries_uses_default_strength():
    # strength defaults to 0.5 which is below 0.75 -> considered uncertain
    engine = ActiveLearningEngine()
    probes = engine.generate_probe_queries([{"belief_id": "b1", "hypothesis": "h"}])
    assert len(probes) == 1


def test_generate_probe_queries_empty_input():
    assert ActiveLearningEngine().generate_probe_queries([]) == []
