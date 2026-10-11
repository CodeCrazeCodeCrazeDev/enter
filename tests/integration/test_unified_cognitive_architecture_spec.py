# -*- coding: utf-8 -*-
"""
test_unified_cognitive_architecture_spec.py
Integration test suite for the Unified 4-Layer Cognitive Operating System Taxonomy:
- Layer 1: Research OS (Scientific Research & Hypothesis Engine Layer)
- Layer 2: EIOS / EOS (Execution, Orchestration & Venture Engine Layer)
- Layer 3: AEAN (Autonomous Economic Agent Network Layer)
- Layer 4: APODEX (World Model & Decision Substrate Layer)
"""

import pytest
import uuid
from apodex.orchestration.unified_cognitive_os import UnifiedCognitiveOS, CognitiveOSState
from apodex.cognition.brain import CognitiveBrain, DeepCausalWorldModel, AdvancedMemoryEngine


def test_unified_cognitive_os_initialization():
    """Verifies default initialization of the Unified Cognitive OS."""
    cognitive_os = UnifiedCognitiveOS()
    assert cognitive_os.brain is not None
    assert cognitive_os.state is not None
    assert isinstance(cognitive_os.state.session_id, uuid.UUID)
    assert cognitive_os.state.active_layer == "Layer 4 Substrate"


def test_closed_loop_active_inference_execution():
    """
    Tests end-to-end Active Inference state handoffs across all 4 layers:
    Layer 1 (Research OS) -> Layer 2 (EIOS/EOS) -> Layer 3 (AEAN) -> Layer 4 (APODEX).
    """
    cognitive_os = UnifiedCognitiveOS()
    goal = "Autonomous Quantum Enterprise Optimization"

    result = cognitive_os.execute_active_inference_loop(goal_title=goal, target_variable="market_penetration")

    # Check return structure across all 4 layers
    assert result["goal_title"] == goal
    assert result["active_layer"] == "Layer 4 APODEX Substrate"

    # Layer 1 Verification
    assert "hypothesis_id" in result["layer_1_research"]
    assert result["layer_1_research"]["status"] == "validated"
    assert result["layer_1_research"]["lit_count"] >= 1

    # Layer 2 Verification
    assert result["layer_2_eios_eos"]["plan_steps_count"] == 4
    assert isinstance(result["layer_2_eios_eos"]["efe_score"], float)
    assert result["layer_2_eios_eos"]["efe_score"] < 0  # Expected Free Energy G is minimized

    # Layer 3 Verification
    assert result["layer_3_aean"]["winning_agent"] is not None
    assert result["layer_3_aean"]["consensus_score"] > 0.5
    assert result["layer_3_aean"]["echo_penalty"] > 0

    # Layer 4 Verification
    assert result["layer_4_apodex"]["do_calculus_target_val"] > 0
    assert result["layer_4_apodex"]["posterior_mean"] == 0.75  # (1+8)/(1+8+1+2) = 9/12 = 0.75
    assert "fact_id" in result["layer_4_apodex"]
    assert result["layer_4_apodex"]["consolidated_lessons"] == 1


def test_layer_4_scm_do_calculus_interventions():
    """Verifies Judea Pearl SCM do-calculus query execution in Layer 4 (APODEX)."""
    brain = CognitiveBrain()
    brain.world_model.add_variable("r_and_d_spending", alpha=1.0, beta=1.0)
    brain.world_model.add_causal_relation("r_and_d_spending", "product_quality", coefficient=0.9)

    # Execute do(X = x) intervention
    do_outcomes = brain.world_model.query_do_calculus("r_and_d_spending", intervention_val=10.0)

    assert do_outcomes["r_and_d_spending"] == 10.0
    assert do_outcomes["product_quality"] == 9.0  # 0.9 * 10.0


def test_layer_3_sycophancy_mitigation_penalty():
    """Verifies sycophancy echo-trap detection and correction factor in Layer 3 (AEAN)."""
    brain = CognitiveBrain()

    # Low variance scores among agents (echo chamber)
    echo_scores = {"agent_1": 0.85, "agent_2": 0.851, "agent_3": 0.849}
    consensus, penalty = brain.orchestrator.resolve_debate_consensus(echo_scores)

    # Standard deviation is < 0.03, triggering 0.82x sycophancy correction
    std_dev = penalty
    assert std_dev < 0.03  # Low variance echo chamber
    assert consensus < 0.85  # Downweighted consensus score (0.85 * 0.82 ~ 0.697)


def test_layer_4_ebbinghaus_forgetting_and_memory_consolidation():
    """Verifies memory consolidation and Ebbinghaus forgetting decay in Layer 4 (APODEX)."""
    memory = AdvancedMemoryEngine()

    # Assert a fact
    fact = memory.assert_fact("transient_insight", "hypothesis", {"depth": 1}, confidence=1.0)

    # Log episode
    from apodex.cognition.brain import TrajectoryStep
    step = TrajectoryStep(action="execute_test", outcome={"success": True})
    memory.log_episode(step)

    assert len(memory.episodic_memory) == 1

    # Consolidate memory
    report = memory.consolidate_memories()
    assert report["consolidated_episodes"] == 1
    assert report["extracted_lessons"] == 1
    assert len(memory.episodic_memory) == 0  # Cleared after consolidation
    assert len(memory.long_term_memory) == 1
