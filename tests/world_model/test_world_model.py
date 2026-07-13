"""Unit and integration tests for the World Model subsystem."""

from __future__ import annotations

import pytest
from uuid import uuid4
from apodex.world_model.domain.entities import Entity
from apodex.world_model.domain.relationships import Relationship
from apodex.world_model.domain.beliefs import Belief
from apodex.world_model.graph.world_graph import WorldGraphManager
from apodex.world_model.graph.traversal import GraphTraversalService


@pytest.mark.asyncio
async def test_world_model_graph_integration():
    # Create states and events as Entities
    node_a = Entity(name="event_a", entity_type="event", properties={"desc": "A heavy spark"})
    node_b = Entity(name="event_b", entity_type="event", properties={"desc": "An explosion"})
    node_c = Entity(name="state_c", entity_type="state", properties={"desc": "System shutdown"})

    entities = {
        node_a.entity_id: node_a,
        node_b.entity_id: node_b,
        node_c.entity_id: node_c,
    }

    # Assert causal links as Relationships
    edge_ab = Relationship(source_id=node_a.entity_id, target_id=node_b.entity_id, relation_type="causal", weight=0.95)
    edge_bc = Relationship(source_id=node_b.entity_id, target_id=node_c.entity_id, relation_type="causal", weight=1.0)

    relationships = [edge_ab, edge_bc]

    # Create world graph manager
    wm = WorldGraphManager(entities=entities, relationships=relationships)

    # Verify query links
    rels_from_a = await wm.get_relationships(timeline_id=uuid4(), entity_id=node_a.entity_id)
    assert len(rels_from_a) == 1
    assert rels_from_a[0].target_id == node_b.entity_id

    rels_to_c = await wm.get_relationships(timeline_id=uuid4(), entity_id=node_c.entity_id)
    assert len(rels_to_c) == 1
    assert rels_to_c[0].source_id == node_b.entity_id

    # Path finding validation using Traversal Service
    traversal = GraphTraversalService(graph_manager=wm)
    path = await traversal.find_shortest_path(timeline_id=uuid4(), start_id=node_a.entity_id, end_id=node_c.entity_id)
    assert path == [node_a.entity_id, node_c.entity_id]
