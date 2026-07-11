"""Unit and integration tests for the World Model subsystem."""

from __future__ import annotations

import pytest
from agent_harness.core.memory.world_model import CausalNode, RelationEdge, WorldModel


def test_world_model_graph():
    wm = WorldModel()

    # Create states and events
    node_a = CausalNode(node_id="event_a", node_type="event", properties={"desc": "A heavy spark"})
    node_b = CausalNode(node_id="event_b", node_type="event", properties={"desc": "An explosion"})
    node_c = CausalNode(node_id="state_c", node_type="state", properties={"desc": "System shutdown"})

    wm.add_node(node_a)
    wm.add_node(node_b)
    wm.add_node(node_c)

    # Assert causal links
    edge_ab = RelationEdge(source_id="event_a", target_id="event_b", relation_type="causal", weight=0.95)
    edge_bc = RelationEdge(source_id="event_b", target_id="state_c", relation_type="causal", weight=1.0)

    wm.add_relation(edge_ab)
    wm.add_relation(edge_bc)

    # Verify query links
    relations_from_a = wm.get_relations_from("event_a")
    assert len(relations_from_a) == 1
    assert relations_from_a[0].target_id == "event_b"

    relations_to_c = wm.get_relations_to("state_c")
    assert len(relations_to_c) == 1
    assert relations_to_c[0].source_id == "event_b"

    # Path finding validation
    path = wm.find_path("event_a", "state_c")
    assert path == ["event_a", "event_b", "state_c"]

    # Negative path finding validation
    no_path = wm.find_path("state_c", "event_a")
    assert no_path is None
