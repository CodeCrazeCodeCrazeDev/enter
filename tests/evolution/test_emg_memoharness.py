"""
Experience Memory Graph (EMG) and MemoHarness Integration Tests.
Verifies graph building, subgraph pattern extraction, graph-edit repair paths,
similarity-based active memory retrieval, and refined proposal context integration.
"""

from __future__ import annotations

import pytest
import time
from typing import Any, Dict, List

from apodex.memory.emg_engine import EMGEngine, ActionDecisionGraph, EMGNode
from apodex.memory.semantic_memory import SemanticMemory, SQLiteMemoryRepository, EvidenceCard
from apodex.evolution.self_harness.trajectory_areal import AgentTrajectory, EvolutionControlPlane, AReaLDataProxy
from apodex.evolution.self_harness.refiner import HarnessRefiner


def test_emg_graph_building_and_subgraphs():
    # 1. Simulate standard trajectory steps
    steps_1 = [
        {"step_id": "step_101", "node_type": "tool_execution", "tool_name": "web_search", "status": "success", "incoming_edges": []},
        {"step_id": "step_102", "node_type": "tool_execution", "tool_name": "web_fetch", "status": "success", "incoming_edges": ["step_101"]},
        {"step_id": "step_103", "node_type": "tool_execution", "tool_name": "code_executor", "status": "success", "incoming_edges": ["step_102"]}
    ]
    steps_2 = [
        {"step_id": "step_201", "node_type": "tool_execution", "tool_name": "web_search", "status": "success", "incoming_edges": []},
        {"step_id": "step_202", "node_type": "tool_execution", "tool_name": "web_fetch", "status": "success", "incoming_edges": ["step_201"]},
        {"step_id": "step_203", "node_type": "tool_execution", "tool_name": "code_executor", "status": "success", "incoming_edges": ["step_202"]}
    ]

    graph_1 = EMGEngine.build_graph_from_trajectory("traj_1", steps_1)
    graph_2 = EMGEngine.build_graph_from_trajectory("traj_2", steps_2)

    # Verify nodes and edges are populated
    assert len(graph_1.nodes) == 3
    assert len(graph_1.edges) == 2
    assert graph_1.nodes["step_102"].action == "web_fetch"

    # Find common subgraphs (workflows)
    common = EMGEngine.find_common_subgraphs([graph_1, graph_2])
    assert len(common) >= 1
    assert common[0] == ["web_search", "web_fetch", "code_executor"]


def test_emg_graph_edit_paths():
    # Simulate a successful execution sequence
    steps_success = [
        {"step_id": "s1", "node_type": "tool_execution", "tool_name": "web_search", "status": "success", "timestamp": 100},
        {"step_id": "s2", "node_type": "tool_execution", "tool_name": "web_fetch", "status": "success", "timestamp": 101},
        {"step_id": "s3", "node_type": "tool_execution", "tool_name": "code_executor", "status": "success", "timestamp": 102}
    ]
    # Simulate a failed execution sequence (web_fetch was missed, code_executor failed)
    steps_failed = [
        {"step_id": "f1", "node_type": "tool_execution", "tool_name": "web_search", "status": "success", "timestamp": 100},
        {"step_id": "f3", "node_type": "tool_execution", "tool_name": "code_executor", "status": "failed", "timestamp": 101}
    ]

    graph_success = EMGEngine.build_graph_from_trajectory("t_succ", steps_success)
    graph_failed = EMGEngine.build_graph_from_trajectory("t_fail", steps_failed)

    # Compute graph edit corrective path
    edit_ops = EMGEngine.compute_graph_edit_path(graph_failed, graph_success)

    # We expect:
    # 1. ADD_STEP for "web_fetch" before executing "code_executor"
    # 2. REPLACE_STEP on "code_executor" because it failed
    op_types = [op.op_type for op in edit_ops]
    actions = [op.action for op in edit_ops]

    assert "ADD_STEP" in op_types
    assert "web_fetch" in actions
    assert "REPLACE_STEP" in op_types
    assert "code_executor" in actions


def test_memoharness_semantic_search():
    repo = SQLiteMemoryRepository(db_path=":memory:")
    memory = SemanticMemory(repository=repo)

    # Populate evidence card
    card_1 = EvidenceCard(
        evidence_id="e1",
        source_url="source",
        content="web_fetch handles large context tables using chunked scraping parameters."
    )
    card_2 = EvidenceCard(
        evidence_id="e2",
        source_url="source",
        content="code_executor compilation failures require setting strict environment libraries."
    )
    memory.add_evidence(card_1)
    memory.add_evidence(card_2)

    # Retrieve similar evidence (query matches card_1 content)
    matches = memory.retrieve_similar_evidence("web_fetch scraping", limit=1)
    assert len(matches) == 1
    assert matches[0].evidence_id == "e1"

    # Query matches card_2 content
    matches_compilation = memory.retrieve_similar_evidence("compilation failures", limit=1)
    assert len(matches_compilation) == 1
    assert matches_compilation[0].evidence_id == "e2"


def test_harness_refiner_emg_and_memoharness_integration():
    control_plane = EvolutionControlPlane(data_proxy=AReaLDataProxy())
    repo = SQLiteMemoryRepository(db_path=":memory:")
    memory = SemanticMemory(repository=repo)

    # Save historical compilation warning
    memory.add_evidence(EvidenceCard(
        evidence_id="ev_comp",
        source_url="src",
        content="code_executor compilation issues occur when libraries are out of date."
    ))

    # Construct the refiner with active memory
    refiner = HarnessRefiner(control_plane=control_plane, semantic_memory=memory)

    # Simulate a failed trajectory with a tool execution error (on code_executor)
    failed_traj = AgentTrajectory(task_id="task_fail")
    failed_traj.add_step({
        "step_id": "f_1", "node_type": "tool_execution", "tool_name": "web_search", "status": "success", "timestamp": 100
    })
    failed_traj.add_step({
        "step_id": "f_2", "node_type": "tool_execution", "tool_name": "code_executor", "status": "failed", "timestamp": 101, "is_error": True, "tool_result_preview": "Compilation error"
    })

    # Simulate a successful reference trajectory
    success_traj = AgentTrajectory(task_id="task_success")
    success_traj.add_step({
        "step_id": "s_1", "node_type": "tool_execution", "tool_name": "web_search", "status": "success", "timestamp": 100
    })
    success_traj.add_step({
        "step_id": "s_1.5", "node_type": "tool_execution", "tool_name": "web_fetch", "status": "success", "timestamp": 101
    })
    success_traj.add_step({
        "step_id": "s_2", "node_type": "tool_execution", "tool_name": "code_executor", "status": "success", "timestamp": 102
    })

    # Run the upgraded refiner
    proposal = refiner.propose_refinement([failed_traj, success_traj])

    assert proposal is not None
    # Verify that the graph edit path (EMG) is calculated and injected
    assert len(proposal.graph_edit_steps) > 0
    assert any("ADD_STEP" in step for step in proposal.graph_edit_steps)

    # Verify that matching MemoHarness historical evidence was injected into the rationale
    assert "Historical Success Match" in proposal.rationale
    assert "compilation issues occur" in proposal.rationale
