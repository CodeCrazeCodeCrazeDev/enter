# -*- coding: utf-8 -*-
"""
test_unified_cognitive_os_e2e.py: End-to-end multi-layer integration tests for the
Unified Cognitive Operating System (Research OS + EIOS/EOS + AEAN + APODEX).
"""

import os
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    TrajectoryStep,
    ResearchToSystemBridge,
)
from apodex.arcs.kernel.kernel import EIOSKernel
from apodex.ai_eos.intelligence.eos_engine import EOSEngine
from apodex.aean.coordination.hive_mind import HiveMind
from apodex.world_model.world_model import WorldModel


def test_research_to_system_bridge_e2e():
    """Validates joint cross-layer state handoffs across Layer 1 to Layer 4."""
    eios_kernel = EIOSKernel()
    eos_engine = EOSEngine()
    hive_mind = HiveMind()
    world_model = WorldModel()

    bridge = ResearchToSystemBridge(
        eios_kernel=eios_kernel,
        eos_engine=eos_engine,
        hive_mind=hive_mind,
        world_model=world_model,
    )

    # 1. Promote Hypothesis from Layer 1 to Layer 2
    hypothesis = {
        "hypothesis_id": "hyp-alpha-101",
        "title": "Autonomous Active Inference Optimization",
        "p_value": 0.001,
        "confidence": 0.99,
    }
    rec1 = bridge.promote_hypothesis_to_kernel(hypothesis)
    assert rec1["target_layer"] == "Layer 2: EIOS Kernel / EOS Engine"
    assert len(eos_engine.active_hypotheses) >= 1

    # 2. Dispatch DAG task from Layer 2 to Layer 3
    rec2 = bridge.dispatch_dag_to_hivemind(
        task_id="dag-task-202",
        task_description="Execute active inference parameter tuning",
        budget_tokens=500.0,
    )
    assert rec2["target_layer"] == "Layer 3: AEAN HiveMind"

    # 3. Update Layer 4 World Model state post execution
    rec3 = bridge.update_world_model_state(
        entity_id="agent-worker-01",
        action="optimize_prompt_weights",
        outcome=0.94,
        belief_confidence=0.98,
    )
    assert rec3["target_layer"] == "Layer 4: APODEX WorldModel"
    assert len(bridge.handoff_history) == 3


def test_budget_bounded_routing_gate():
    """Validates LearnableRoutingGateDispatcher budget bounds and EFE task dispatch."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=1.00)

    fast_cheap_agent = SpecializedAgentProfile(
        agent_id="fast_cheap_node",
        domain_specialty="general",
        cost_per_token=0.0001,
        historical_success_rate=0.8,
    )
    expensive_expert = SpecializedAgentProfile(
        agent_id="expert_node",
        domain_specialty="quantum_research",
        cost_per_token=0.05,
        historical_success_rate=0.95,
    )

    dispatcher.register_subagent(fast_cheap_agent)
    dispatcher.register_subagent(expensive_expert)

    # Route task matching specialty within budget
    selected = dispatcher.route_task(task_complexity=10.0, domain="quantum_research")
    assert selected in ["expert_node", "fast_cheap_node"]

    # Update parameters
    dispatcher.update_routing_parameters(agent_id=selected, success=True, cost_incurred=0.10)
    assert dispatcher.budget_spent == 0.10


def test_code_rewrite_ast_verification(tmp_path):
    """Validates CodeRewriteEngine static analysis security linting."""
    test_file = tmp_path / "research_module.py"
    test_file.write_text("def run_calc():\n    return 42\n")

    engine = CodeRewriteEngine(allowed_paths=[str(tmp_path)])

    # Safe rewrite proposal
    proposal_safe = engine.propose_rewrite(
        filepath=str(test_file),
        original_snippet="return 42",
        proposed_snippet="return 42 + 10",
        rationale="Update calculation logic",
    )
    assert engine.verify_proposal_ast(proposal_safe) is True
    assert engine.commit_rewrite(proposal_safe) is True
    assert "return 42 + 10" in test_file.read_text()

    # Unsafe proposal with eval call
    proposal_unsafe = engine.propose_rewrite(
        filepath=str(test_file),
        original_snippet="return 42 + 10",
        proposed_snippet="return eval('42 + 10')",
        rationale="Unsafe eval execution",
    )
    assert engine.verify_proposal_ast(proposal_unsafe) is False
    assert engine.commit_rewrite(proposal_unsafe) is False
