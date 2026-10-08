# -*- coding: utf-8 -*-
"""
test_unified_cognitive_os_subsystems.py

Comprehensive multi-layer integration tests validating closed-loop interactions
across Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, and APODEX WorldModel
via ResearchToSystemBridge.
"""

import pytest
from apodex.ai_eos.research.integration import ResearchToSystemBridge
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel


def test_research_to_system_bridge_initialization():
    bridge = ResearchToSystemBridge()
    assert bridge.research_os is not None
    assert bridge.eos_engine is not None
    assert bridge.eios_kernel is not None
    assert bridge.hive_mind is not None
    assert bridge.world_model is not None


def test_cross_layer_handoff_validated_hypothesis():
    ros = ResearchOS()
    eos = EOSEngine()
    eios = EIOSKernel()
    hive = HiveMind(token_budget=100)
    wm = WorldModel()

    bridge = ResearchToSystemBridge(
        research_os=ros,
        eos_engine=eos,
        eios_kernel=eios,
        hive_mind=hive,
        world_model=wm
    )

    # 1. Register and validate hypothesis in Research OS
    hyp = ros.register_hypothesis(
        title="Hawkes Hawkes non-Gaussian Stability",
        description="Non-Gaussian Hawkes process controls recursive call depth volatility.",
        null_hypothesis="Call depth volatility is invariant to Hawkes process control.",
        target_metric="recursion_depth_volatility"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status == "validated"

    # 2. Perform cross-layer handoff
    report = bridge.handoff_validated_hypothesis(hyp.hypothesis_id)

    assert report["hypothesis_id"] == str(hyp.hypothesis_id)
    assert report["layer_1_research_status"] == "validated"
    assert report["layer_3_grants_count"] > 0
    assert report["layer_4_world_model_nodes"] >= 2
    assert report["layer_4_world_model_edges"] >= 1
    assert report["layer_4_belief"]["validated"] is True

    # Confirm EOS Engine hypothesis engine received hypothesis
    assert len(eos.hypothesis_engine.hypotheses) == 1

    # Confirm EIOS Kernel registered active DAG
    assert len(eios.active_processes) == 1

    # Confirm WorldModel node and edge insertion
    hyp_node_id = f"hyp_{hyp.hypothesis_id}"
    metric_node_id = f"metric_{hyp.target_metric}"
    assert hyp_node_id in wm.nodes
    assert metric_node_id in wm.nodes


def test_closed_loop_active_inference():
    bridge = ResearchToSystemBridge()

    result = bridge.execute_closed_loop_active_inference(
        title="MAP-Elites Parameter Diversity",
        description="MAP-Elites island migration gates increase parameter search space coverage.",
        null_hypothesis="MAP-Elites migration gates do not affect parameter coverage.",
        target_metric="parameter_coverage",
        ground_truth_yield=3.0
    )

    assert "hypothesis" in result
    assert result["hypothesis"]["is_statistically_significant"] is True
    assert "cross_layer_handoff" in result
    assert "eos_sensing" in result
    assert result["eos_sensing"]["market_uncertainty"] >= 0.0
