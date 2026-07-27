"""Unit tests for Phase 3 Memory, Knowledge Infrastructure & Institutional Knowledge Graph (IKG)."""

import pytest
from apodex.ai_eos.memory.knowledge_infrastructure import KnowledgeInfrastructure


def test_ikg_temporal_versioning():
    """Verify that updates to IKG nodes create new temporal versions and archive old ones."""
    ki = KnowledgeInfrastructure()

    ki.record_node("model_v1", "model", {"accuracy": 0.85})
    ki.record_node("model_v1", "model", {"accuracy": 0.91})

    node = ki.nodes.get("model_v1")
    assert node.version == 2
    assert node.properties["accuracy"] == 0.91

    history = ki.historical_nodes.get("model_v1")
    assert len(history) == 1
    assert history[0].version == 1
    assert history[0].properties["accuracy"] == 0.85


def test_ikg_provenance_lineage():
    """Verify that upstream graph queries successfully trace capability origin networks."""
    ki = KnowledgeInfrastructure()

    # Create the graph structure representing capability origins:
    # capability_alpha -> DEPENDS_ON -> experiment_gamma -> ORIGINATES_FROM -> paper_omega
    ki.record_node("paper_omega", "paper", {"title": "SEKI arXiv:2502.20422"})
    ki.record_node("experiment_gamma", "experiment", {"p_value": 0.004})
    ki.record_node("capability_alpha", "capability", {"name": "Adaptive Bidding"})

    ki.record_edge("capability_alpha", "experiment_gamma", "DEPENDS_ON")
    ki.record_edge("experiment_gamma", "paper_omega", "ORIGINATES_FROM")

    lineage = ki.get_provenance_lineage("capability_alpha")

    # Order of traversal: capability_alpha, experiment_gamma, paper_omega
    assert len(lineage) == 3
    assert lineage[0]["node_id"] == "capability_alpha"
    assert lineage[1]["node_id"] == "experiment_gamma"
    assert lineage[2]["node_id"] == "paper_omega"


def test_confidence_propagation():
    """Verify that decreasing confidence of dependencies propagates recursively downstream."""
    ki = KnowledgeInfrastructure()

    # Construct dependency chain:
    # feature_X DEPENDS_ON model_Y DEPENDS_ON dataset_Z
    ki.record_node("feature_X", "feature", {})
    ki.record_node("model_Y", "model", {})
    ki.record_node("dataset_Z", "dataset", {})

    ki.record_edge("feature_X", "model_Y", "DEPENDS_ON", weight=0.90)
    ki.record_edge("model_Y", "dataset_Z", "DEPENDS_ON", weight=0.80)

    # Initially, confidence of all nodes is 1.0
    assert ki.nodes.get("feature_X").confidence == 1.0
    assert ki.nodes.get("model_Y").confidence == 1.0

    # Modify root dependency confidence (dataset_Z)
    z_node = ki.nodes.get("dataset_Z")
    z_node.confidence = 0.50
    ki.nodes.save("dataset_Z", z_node)

    # Propagate from root dataset_Z
    ki.propagate_confidence("dataset_Z")

    # model_Y should decay: min(1.0, 0.50 * 0.80) = 0.40
    assert ki.nodes.get("model_Y").confidence == pytest.approx(0.40)

    # feature_X should recursively decay: min(1.0, 0.40 * 0.90) = 0.36
    assert ki.nodes.get("feature_X").confidence == pytest.approx(0.36)
