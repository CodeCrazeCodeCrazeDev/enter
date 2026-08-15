"""Comprehensive unit and integration tests for the unified redesigned cognitive brain system."""

from __future__ import annotations
import math
import uuid
import pytest
from datetime import datetime

from apodex.cognition.brain import (
    CognitiveBrain,
    AdvancedPlanner,
    DeepCausalWorldModel,
    SimulationEngine,
    AdvancedMemoryEngine,
    TrajectoryStep,
    MultiAgentOrchestrator,
    ResearchLabOS,
    SelfImprovementEngine,
    LongHorizonExecutor,
    PlanNode
)


def test_phase1_advanced_planner_decomposition_and_mcts() -> None:
    planner = AdvancedPlanner(curiosity_weight=2.0)

    # Test HTN task decomposition
    plan_nodes = planner.decompose_goal("Optimize checkout API performance")
    assert len(plan_nodes) == 4
    assert plan_nodes[0].action_type == "research"
    assert plan_nodes[2].action_type == "engineering"

    # Test MCTS Expected Free Energy minimization branch selection
    # Branch A: Exploratory, high prior entropy, high reduction (high epistemic value)
    branch_a = {
        "name": "exploratory_cache_redesign",
        "prior_entropy": 2.5,
        "post_entropy": 0.5,
        "pragmatic_prob": 0.4,
        "target_pref": 0.9
    }
    # Branch B: Conservative, low prior entropy, low reduction
    branch_b = {
        "name": "minor_heuristic_patch",
        "prior_entropy": 0.6,
        "post_entropy": 0.5,
        "pragmatic_prob": 0.85,
        "target_pref": 0.9
    }

    best_branch = planner.select_optimal_branch_mcts([branch_a, branch_b])
    # With curiosity_weight=2.0, curiosity is highly prioritized, making branch_a (exploratory) optimal
    assert best_branch["name"] == "exploratory_cache_redesign"
    assert best_branch["g_score"] < 0.0


def test_phase2_world_model_causal_do_calculus_and_bayesian_update() -> None:
    wm = DeepCausalWorldModel()
    wm.add_variable("compute_investment", 5.0, 5.0)
    wm.add_variable("model_accuracy", 5.0, 5.0)
    wm.add_variable("revenue_increase", 5.0, 5.0)

    # Establish SCM causal linkages
    wm.add_causal_relation("compute_investment", "model_accuracy", coefficient=0.8)
    wm.add_causal_relation("model_accuracy", "revenue_increase", coefficient=1.5)

    # Intervene: do(compute_investment = 2.0)
    intervened_state = wm.query_do_calculus("compute_investment", 2.0)
    assert intervened_state["compute_investment"] == 2.0
    # model_accuracy = 0.8 * 2.0 = 1.6
    assert pytest.approx(intervened_state["model_accuracy"]) == 1.6
    # revenue_increase = 1.5 * 1.6 = 2.4
    assert pytest.approx(intervened_state["revenue_increase"]) == 2.4

    # Test Bayesian conjugate prior update (Beta-Binomial)
    mean, variance = wm.update_bayesian_belief("model_accuracy", trials=10, successes=8)
    # alpha increased from 5 to 13, beta increased from 5 to 7. Mean = 13 / 20 = 0.65
    assert mean == 0.65
    assert variance > 0.0


def test_phase3_multi_agent_lifecycle_and_debate_sycophancy() -> None:
    orchestrator = MultiAgentOrchestrator()

    # Test lifecycle
    agent = orchestrator.spawn_agent("researcher")
    assert agent.status == "active"
    assert agent.role == "researcher"

    # Test splitting complex agent
    specialized = orchestrator.split_agent(agent.id, ["literature_scanner", "hypothesis_proposer"])
    assert len(specialized) == 2
    assert orchestrator.agents[agent.id].status == "retired"

    # Test debate consensus & sycophancy mitigation
    # 1. Healthy debate (diverse views)
    diverse_evals = {"Bayesian": 0.8, "Causal": 0.4, "Symbolic": 0.9}
    mean_val, std_dev = orchestrator.resolve_debate_consensus(diverse_evals)
    # Average is 0.7. Variance is high enough to not trigger overconfidence penalty
    assert pytest.approx(mean_val) == 0.7
    assert std_dev > 0.05

    # 2. Sycophantic debate (echo chamber where everyone echoes exactly 0.8)
    echo_evals = {"Bayesian": 0.8, "Causal": 0.8, "Symbolic": 0.8}
    echo_val, echo_std = orchestrator.resolve_debate_consensus(echo_evals)
    assert echo_std < 1e-9
    # Consensus is scaled down by overconfidence penalty of 0.82
    assert pytest.approx(echo_val) == 0.8 * 0.82


def test_phase4_memory_consolidation_and_ebbinghaus_forgetting() -> None:
    memory = AdvancedMemoryEngine(forgetting_rate=0.1)

    # Test multi-tier memory storing
    memory.store_working("active_task", "review_papers")
    assert memory.retrieve_working("active_task") == "review_papers"

    fact1 = memory.assert_fact(
        name="edge_caching_performance",
        concept_type="fact",
        attributes={"hit_rate": 0.92},
        confidence=1.0
    )
    # Set historical timestamp
    fact1.last_updated = datetime.utcnow().timestamp() - 10.0

    # Test Ebbinghaus forgetting decay: C(t) = 1.0 * e^(-0.1 * 10) = e^(-1) ≈ 0.3678
    memory.apply_ebbinghaus_forgetting(datetime.utcnow().timestamp())
    assert pytest.approx(memory.semantic_memory[fact1.id].confidence, abs=1e-3) == math.exp(-1.0)

    # Test episodic logging and memory consolidation sweep
    step = TrajectoryStep(action="run_benchmark", outcome={"success": True}, duration_sec=1.5, cost_cents=10)
    memory.log_episode(step)
    assert len(memory.episodic_memory) == 1

    report = memory.consolidate_memories()
    assert report["consolidated_episodes"] == 1
    assert report["extracted_lessons"] == 1
    assert len(memory.episodic_memory) == 0
    assert len(memory.long_term_memory) == 1


def test_phase5_simulation_engine_probabilistic_monte_carlo() -> None:
    wm = DeepCausalWorldModel()
    wm.add_causal_relation("marketing_budget", "conversion_rate", coefficient=0.5)

    simulator = SimulationEngine(world_model=wm)
    # Simulate outcome under intervention do(marketing_budget = 4.0)
    sim_report = simulator.simulate_rollout(
        strategy_var="marketing_budget",
        intervention_val=4.0,
        target_var="conversion_rate",
        num_trials=50
    )

    # Expected mean conversion rate should be around 2.0 (0.5 * 4.0)
    assert pytest.approx(sim_report["mean"], abs=0.5) == 2.0
    assert sim_report["std_dev"] > 0.0
    assert sim_report["value_at_risk_95"] < sim_report["mean"]


def test_phase6_research_lab_os() -> None:
    lab = ResearchLabOS()

    papers = lab.search_literature("reinforcement learning")
    assert len(papers) == 1
    assert papers[0]["citation_key"] == "smith2026advances"

    # Test claim verification
    claim_verified = lab.verify_claim(
        claim="High temperature increases conversion rates by 12%",
        experimental_results={"conversion_increase": 0.15}
    )
    assert claim_verified is True


def test_phase7_self_improvement_optimization_and_gates() -> None:
    engine = SelfImprovementEngine()

    original_prompt = "Process astro tasks"
    optimized = engine.textgrad_optimize_prompt(original_prompt, failures=["ast parser unhandled float token error"])
    assert optimized != original_prompt
    assert "Rule" in optimized

    # Test promotion evaluation gate
    assert engine.evaluate_gate(0.72, 0.85) is True
    assert engine.evaluate_gate(0.85, 0.80) is False


def test_phase8_long_horizon_execution_and_failover() -> None:
    executor = LongHorizonExecutor(resource_budget_cents=1000)

    # Test task queues & checkpoints
    task_id = uuid.uuid4()
    executor.create_checkpoint(task_id, {"step_completed": 2, "state_snapshot": "checkpoint_ok"})

    recovered = executor.recover_from_checkpoint(task_id)
    assert recovered["state"]["step_completed"] == 2

    # Test resource scheduling
    assert executor.allocate_resources(400) is True
    assert executor.allocate_resources(800) is False  # Exceeds total budget of 1000


def test_phase9_cognitive_brain_unified_cycle_integration() -> None:
    brain = CognitiveBrain()

    result = brain.run_strategic_cycle("SaaS checkout conversion micro-testing")
    assert result["goal"] == "SaaS checkout conversion micro-testing"
    assert result["plan_length"] == 4
    assert "sim_results" in result
    assert result["claim_verified"] is True
    assert result["optimized_prompt"] != ""
    assert result["fact_id"] != ""
