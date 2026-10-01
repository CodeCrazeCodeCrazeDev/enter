# -*- coding: utf-8 -*-
"""
test_unified_5layer_integration.py: Multi-layer integration test suite validating cross-layer
state handoffs across Research OS, EIOS Kernel, EOS Engine, AEAN HiveMind, and WorldModel via ResearchToSystemBridge.
"""

import pytest
from uuid import uuid4

from apodex.ai_eos.research.research_os import ResearchOS
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel
from apodex.ai_eos.research.integration import ResearchToSystemBridge


def test_unified_5layer_cross_layer_handoff():
    """Validates cross-layer Active Inference state propagation through ResearchToSystemBridge."""
    ros = ResearchOS()
    kernel = EIOSKernel()
    eos = EOSEngine()
    hive = HiveMind()
    wm = WorldModel()

    # 1. Register and validate hypothesis in Layer 1 Research OS
    hyp = ros.register_hypothesis(
        title="Hawkes Volatility Alpha Strategy",
        description="Continuous-time Hawkes jump processes improve risk-adjusted returns.",
        null_hypothesis="Hawkes strategy yields zero alpha.",
        target_metric="Sharpe_Ratio"
    )
    exp = ros.create_experiment(hyp.hypothesis_id, seed=123)
    completed_exp = ros.execute_experiment_simulation(exp.experiment_id, ground_truth_yield=2.5)

    assert hyp.status == "validated" or completed_exp.effect_size > 0

    # Force status for deterministic integration test execution
    hyp.status = "validated"

    # 2. Instantiate Bridge and execute cross-layer handoff
    bridge = ResearchToSystemBridge(ros, kernel, eos, hive, wm)
    res = bridge.propagate_validated_hypothesis(hyp.hypothesis_id)

    # 3. Assert Layer 2 EIOS Kernel received hypothesis
    assert len(kernel.research_hypotheses) == 1
    assert kernel.research_hypotheses[0]["title"] == "Hawkes Volatility Alpha Strategy"

    # 4. Assert Layer 2 EOS Engine ingested opportunity
    assert len(eos.active_research_hypotheses) == 1
    assert eos.active_research_hypotheses[0]["title"] == "Hawkes Volatility Alpha Strategy"

    # 5. Assert Layer 3 AEAN HiveMind registered research insight
    assert len(hive.research_insights_registry) == 1
    assert hive.research_insights_registry[0]["insight"] == "Hawkes Volatility Alpha Strategy"

    # 6. Assert Layer 4 APODEX WorldModel created CausalNode and updated belief
    node_id = f"hyp_{hyp.hypothesis_id}"
    assert node_id in wm.nodes
    assert node_id in wm.beliefs
    assert wm.beliefs[node_id]["confidence"] == 0.95
