"""
test_unified_cognitive_os_subsystems.py: Integration test suite for UnifiedCognitiveOS across 5 subsystem layers.
"""

import pytest
from apodex.orchestration.unified_cognitive_os import UnifiedCognitiveOS


def test_unified_cognitive_os_initialization():
    system = UnifiedCognitiveOS()
    assert system.research_os is not None
    assert system.eios_kernel is not None
    assert system.eos_engine is not None
    assert system.fourteen_layer_engine is not None
    assert system.hive_mind is not None
    assert system.world_model is not None


def test_ingest_and_bridge_hypothesis():
    system = UnifiedCognitiveOS()
    res = system.ingest_and_bridge_hypothesis(
        statement="EFE minimization drives active inference across multi-agent systems.",
        domain="cognitive_architecture",
        target_subsystem="eios"
    )
    assert "hypothesis_id" in res
    assert res["bridge_status"] == "bridged"
    assert res["world_model_node_id"].startswith("hyp_")
    assert len(system.world_model.nodes) == 1


def test_dispatch_hive_mind_task_bidding():
    system = UnifiedCognitiveOS()
    tasks = [
        {"task": "sense_anomalies", "priority": 0.9, "expected_value": 0.8, "token_cost": 20},
        {"task": "execute_counterfactual", "priority": 0.7, "expected_value": 0.6, "token_cost": 30}
    ]
    grants = system.dispatch_hive_mind_task_bidding(tasks)
    assert len(grants) == 2
    assert grants[0].granted is True
    assert grants[1].granted is True


def test_update_world_model_beliefs():
    system = UnifiedCognitiveOS()
    system.update_world_model_beliefs("system_stability", 0.98, source_subsystem="test_suite")
    assert "system_stability" in system.world_model.beliefs
    assert system.world_model.beliefs["system_stability"]["value"] == 0.98


def test_closed_loop_active_inference_cycle():
    system = UnifiedCognitiveOS()
    cycle_input = {
        "title": "Unified Closed-Loop Active Inference Cycle",
        "domain": "cognitive_architecture",
        "hypothesis_statement": "Joint multi-layer active inference reduces variational free energy.",
        "keywords": ["active_inference", "causal_scm", "hive_mind"],
        "tam_cents": 250000000,
        "total_budget_cents": 10000000
    }
    res = system.run_closed_loop_active_inference_cycle(cycle_input)

    assert res["status"] == "success"
    assert res["research_os_hypothesis"]["bridge_status"] == "bridged"
    assert res["fourteen_layer_engine_result"]["status"] == "completed"
    assert res["hive_mind_grants"] == 3
    assert res["world_model_nodes"] >= 2
    assert res["world_model_edges"] >= 1
    assert "cycle_success_confidence" in res["world_model_beliefs"]
