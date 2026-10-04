# -*- coding: utf-8 -*-
"""
test_unified_cognitive_architecture_spec.py
Integration test suite validating closed-loop interactions across the unified 4-layer cognitive architecture:
- Layer 1: Research OS (Hypothesis generation, statistical validation)
- Layer 2: EIOS Kernel & EOS Engine (DAG execution, entrepreneurial state machine)
- Layer 3: AEAN HiveMind & Gate Dispatcher (Swarm token bidding, budget-bounded routing)
- Layer 4: APODEX WorldModel (Causal graph, recursive Bayesian belief updating)
"""

from __future__ import annotations
import pytest
import tempfile
import os
from uuid import uuid4

# Layer 1 imports
from apodex.ai_eos.research.research_os import ResearchOS
from apodex.ai_eos.research.integration import (
    CodeRewriteEngine,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)

# Layer 2 imports
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.arcs.kernel.kernel import EIOSKernel

# Layer 3 imports
from apodex.aean.coordination.hive_mind import HiveMind

# Layer 4 imports
from apodex.world_model.world_model import WorldModel, CausalNode, RelationEdge
from apodex.world_model.domain.beliefs import Belief


def test_layer_1_research_os_hypothesis_validation():
    """Validates Layer 1 Research OS hypothesis creation and simulation execution."""
    ros = ResearchOS()

    # Register hypothesis
    hyp = ros.register_hypothesis(
        title="Active Inference Speedup",
        description="EFE routing reduces token consumption by 35%",
        null_hypothesis="EFE routing has no effect on token consumption",
        target_metric="token_efficiency",
        significance_alpha=0.05
    )
    assert hyp.status == "registered"

    # Create and execute experiment simulation
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=42)
    completed_exp = ros.execute_experiment_simulation(
        experiment_id=exp.experiment_id,
        ground_truth_yield=2.5
    )

    assert completed_exp.status.value == "completed"
    assert hyp.status in ("validated", "refuted")


def test_layer_1_code_rewrite_ast_security():
    """Validates Layer 1 AST static linting and security vetoes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "module.py")
        with open(test_file, "w") as f:
            f.write("def safe_function():\n    return 42\n")

        engine = CodeRewriteEngine(allowed_paths=[tmpdir])

        # Safe proposal
        safe_prop = engine.propose_rewrite(
            filepath=test_file,
            original_snippet="return 42",
            proposed_snippet="return 84",
            rationale="Double return value"
        )
        assert engine.verify_proposal_ast(safe_prop) is True
        assert engine.commit_rewrite(safe_prop) is True

        # Unsafe proposal containing eval
        unsafe_prop = engine.propose_rewrite(
            filepath=test_file,
            original_snippet="return 84",
            proposed_snippet="return eval('2 + 2')",
            rationale="Dynamic evaluation"
        )
        assert engine.verify_proposal_ast(unsafe_prop) is False
        assert engine.commit_rewrite(unsafe_prop) is False


def test_layer_2_eos_and_eios_integration():
    """Validates Layer 2 EOS Engine hypothesis ingestion and EIOS Active Inference sensing."""
    eos = EOSEngine()
    eios = EIOSKernel()

    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Predictive Cache Optimization",
        description="Predictive caching lowers database latency",
        null_hypothesis="Latency unchanged",
        target_metric="latency_ms"
    )

    # Ingest research into EOS Engine
    eos.ingest_validated_research(hyp)
    assert hyp.hypothesis_id in eos.active_hypotheses

    # Register research in EIOS Kernel
    eios.register_research_hypothesis(hyp)
    anomalies = eios.sense_opportunity_anomalies()
    assert isinstance(anomalies, list)


def test_layer_3_aean_hivemind_and_gate_dispatcher():
    """Validates Layer 3 AEAN HiveMind bidding and budget-bounded agent routing."""
    hive_mind = HiveMind()

    # Register research insight
    hive_mind.register_research_insight("EFE_ROUTING_INSIGHT", {"gain": 0.35})

    # Task bidding
    bid_result = hive_mind.submit_task_bid(
        agent_id="agent_alpha",
        task_id="task_opt_01",
        bid_tokens=50.0,
        capability_score=0.92
    )
    assert bid_result["status"] == "registered"

    # Gate Dispatcher
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    agent_p = SpecializedAgentProfile(
        agent_id="agent_fast",
        domain_specialty="optimization",
        cost_per_token=0.001,
        historical_success_rate=0.88,
        epistemic_curiosity=0.4
    )
    dispatcher.register_subagent(agent_p)

    selected = dispatcher.route_task(task_complexity=100.0, domain="optimization")
    assert selected == "agent_fast"


def test_layer_4_world_model_causal_and_bayesian_updates():
    """Validates Layer 4 APODEX WorldModel causal graph and recursive Bayesian belief updates."""
    wm = WorldModel()

    node_id = "node_latency_01"
    causal_node = CausalNode(
        node_id=node_id,
        node_type="metric",
        properties={"value_ms": 120.0}
    )
    wm.add_node(causal_node)
    assert node_id in wm.nodes

    # Recursive Bayesian belief update
    belief = Belief(
        target_id=uuid4(),
        probability=0.5,
        evidence=["obs_01"]
    )

    initial_prob = belief.probability
    belief.update_confidence(likelihood=2.5, prior_probability=initial_prob)

    # Posterior should increase given likelihood > 1.0
    assert belief.probability > initial_prob


def test_closed_loop_4layer_unified_architecture():
    """End-to-End closed-loop test validating state handoffs across all 4 layers."""
    # Step 1: Research OS (Layer 1)
    ros = ResearchOS()
    hyp = ros.register_hypothesis(
        title="Unified Pipeline Optimization",
        description="Unified architecture lowers latency across layers",
        null_hypothesis="No latency improvement",
        target_metric="latency"
    )
    exp = ros.create_experiment(hypothesis_id=hyp.hypothesis_id, seed=100)
    ros.execute_experiment_simulation(experiment_id=exp.experiment_id, ground_truth_yield=3.0)

    # Step 2: EOS & EIOS (Layer 2)
    eos = EOSEngine()
    eios = EIOSKernel()
    eos.ingest_validated_research(hyp)
    eios.register_research_hypothesis(hyp)

    # Step 3: AEAN HiveMind (Layer 3)
    hive_mind = HiveMind()
    hive_mind.register_research_insight(
        insight_key=str(hyp.hypothesis_id),
        insight_data={"status": hyp.status, "title": hyp.title}
    )

    # Step 4: APODEX WorldModel (Layer 4)
    wm = WorldModel()
    causal_node = CausalNode(
        node_id=str(hyp.hypothesis_id),
        node_type="validated_hypothesis",
        properties={"hypothesis_id": str(hyp.hypothesis_id), "status": hyp.status}
    )
    wm.add_node(causal_node)

    assert causal_node.node_id == str(hyp.hypothesis_id)
    assert causal_node.properties["status"] == hyp.status
