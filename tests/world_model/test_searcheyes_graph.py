from __future__ import annotations
import pytest
from uuid import uuid4
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge
from apodex.world_model.graph.searcheyes_models import (
    PerceptionKnowledgeChain,
    PKCHop,
    FileNodePayload,
    FunctionNodePayload,
    SearchEyesTestNodePayload,
    EdgeMetadata
)

def test_searcheyes_typed_knowledge_graph():
    wm = WorldModel()

    # Create typed node payloads
    file_payload = FileNodePayload(file_path="apodex/world_model/world_model.py", loc=50)
    func_payload = FunctionNodePayload(function_name="register_pkc_trace", file_path="apodex/world_model/world_model.py")
    test_payload = SearchEyesTestNodePayload(test_name="test_searcheyes_typed_knowledge_graph", file_path="tests/world_model/test_searcheyes_graph.py")

    # Wrap them into CausalNodes compatible with existing interfaces
    node_file = CausalNode(node_id="file:world_model.py", node_type="file", properties=file_payload.model_dump())
    node_func = CausalNode(node_id="func:register_pkc_trace", node_type="function", properties=func_payload.model_dump())
    node_test = CausalNode(node_id="test:test_searcheyes_typed_knowledge_graph", node_type="test", properties=test_payload.model_dump())

    wm.add_node(node_file)
    wm.add_node(node_func)
    wm.add_node(node_test)

    # Establish relations
    edge_calls = RelationEdge(
        source_id="func:register_pkc_trace",
        target_id="file:world_model.py",
        relation_type="calls",
        weight=1.0,
        properties=EdgeMetadata(provenance="static_analysis", confidence=0.9).model_dump()
    )
    edge_tests = RelationEdge(
        source_id="test:test_searcheyes_typed_knowledge_graph",
        target_id="func:register_pkc_trace",
        relation_type="tests",
        weight=1.0,
        properties=EdgeMetadata(provenance="test_runner", confidence=1.0).model_dump()
    )

    wm.add_relation(edge_calls)
    wm.add_relation(edge_tests)

    # Path finding: test -> function -> file
    path = wm.find_path("test:test_searcheyes_typed_knowledge_graph", "file:world_model.py")
    assert path == [
        "test:test_searcheyes_typed_knowledge_graph",
        "func:register_pkc_trace",
        "file:world_model.py"
    ]

    # Verify edge metadata
    rels = wm.get_relations_from("test:test_searcheyes_typed_knowledge_graph")
    assert len(rels) == 1
    assert rels[0].relation_type == "tests"
    assert rels[0].properties["provenance"] == "test_runner"


def test_perception_knowledge_chain():
    wm = WorldModel()
    trace = PerceptionKnowledgeChain()

    hop1 = PKCHop(
        step_index=1,
        node_id="file:world_model.py",
        node_type="file",
        anchors_hit=["ANCHOR_FOUND_RELEVANT_FILES"],
        cost_usd=0.01,
        timestamp="2023-10-01T00:00:01"
    )
    hop2 = PKCHop(
        step_index=2,
        node_id="test:test_searcheyes_typed_knowledge_graph",
        node_type="test",
        edge_id="tests",
        anchors_hit=["ANCHOR_RAN_TESTS"],
        cost_usd=0.02,
        timestamp="2023-10-01T00:00:02"
    )

    trace.add_hop(hop1)
    trace.add_hop(hop2)

    wm.register_pkc_trace(trace)

    assert len(wm.pkc_traces) == 1
    retrieved_trace = wm.pkc_traces[str(trace.trace_id)]
    assert len(retrieved_trace.hops) == 2
    assert retrieved_trace.cumulative_cost_usd == 0.03
    assert retrieved_trace.hops[0].anchors_hit == ["ANCHOR_FOUND_RELEVANT_FILES"]
    assert retrieved_trace.hops[1].anchors_hit == ["ANCHOR_RAN_TESTS"]
