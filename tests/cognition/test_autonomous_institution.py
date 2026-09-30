from __future__ import annotations
import pytest
import time
from uuid import uuid4

from apodex.cognition.research.autonomous_institution import (
    ResearchHypothesis,
    BeliefState,
    ExpectedFreeEnergyPlanner,
    StructuralCausalModel,
    EbbinghausMemoryConsolidator,
    ConsensAgentEngine
)


def test_expected_free_energy_planner() -> None:
    planner = ExpectedFreeEnergyPlanner(curiosity_weight=2.0)

    # Policy 1: High curiosity / exploratory path (high expected posterior entropy reduction)
    policy_1 = {
        "name": "deep_exploratory_experiment",
        "prior_entropy": 2.0,
        "post_entropy": 0.5,       # high reduction (epistemic value = 1.5)
        "predicted_prob": 0.5,      # low pragmatic probability of success
        "target_pref": 0.9
    }

    # Policy 2: Conservative path (low entropy reduction, high predictability)
    policy_2 = {
        "name": "conservative_replication",
        "prior_entropy": 0.6,
        "post_entropy": 0.5,       # low reduction (epistemic value = 0.1)
        "predicted_prob": 0.85,     # high pragmatic probability of success
        "target_pref": 0.9
    }

    best, efe = planner.select_optimal_policy([policy_1, policy_2])

    # Assert that Policy 1 is selected because curiosity_weight=2.0 makes exploration extremely valuable
    assert best["name"] == "deep_exploratory_experiment"
    assert efe < 0.0


def test_structural_causal_model() -> None:
    scm = StructuralCausalModel()

    # Define variables: Learning Rate -> Model Accuracy -> Business Revenue
    scm.add_causal_link("learning_rate", "model_accuracy", weight=0.8)
    scm.add_causal_link("model_accuracy", "business_revenue", weight=1.5)

    # Run do-calculus intervention (do(learning_rate = 0.1))
    post_interventional_state = scm.intervene_do("learning_rate", 0.1)

    assert post_interventional_state["learning_rate"] == 0.1
    # model_accuracy = 0.8 * 0.1 = 0.08
    assert pytest.approx(post_interventional_state["model_accuracy"]) == 0.08
    # business_revenue = 1.5 * 0.08 = 0.12
    assert pytest.approx(post_interventional_state["business_revenue"]) == 0.12


def test_ebbinghaus_memory_consolidator() -> None:
    consolidator = EbbinghausMemoryConsolidator(decay_rate=0.1)

    initial_belief = BeliefState(
        alpha=5.0,  # 4 successes excess above flat baseline
        beta=5.0,   # 4 failures excess
        last_updated_timestamp=100.0
    )

    # Consolidate after delta_t = 10.0 seconds. Decay factor = e^(-0.1 * 10) = e^(-1) ≈ 0.3678
    # Decayed alpha excess = 4.0 * 0.3678 ≈ 1.471
    # New trial outcomes: 10 trials, 8 successes, 2 failures
    updated = consolidator.consolidate_belief(
        current_belief=initial_belief,
        trials=10,
        successes=8,
        current_timestamp=110.0
    )

    expected_alpha = 1.0 + (4.0 * 0.367879) + 8.0  # ≈ 10.4715
    expected_beta = 1.0 + (4.0 * 0.367879) + 2.0   # ≈ 4.4715

    assert pytest.approx(updated.alpha, abs=1e-3) == expected_alpha
    assert pytest.approx(updated.beta, abs=1e-3) == expected_beta
    assert updated.last_updated_timestamp == 110.0


def test_consens_agent_engine() -> None:
    engine = ConsensAgentEngine()
    hyp = ResearchHypothesis(name="test_hyp", description="testing sycophancy mitigation")

    # 1. Healthy debate (high cognitive diversity)
    healthy_evals = {
        "Bayesian": 0.8,
        "Symbolic": 0.4,
        "Causal": 0.9,
        "Economic": 0.6,
        "Game-Theoretic": 0.5,
        "Mechanistic": 0.7
    }
    score, std_dev = engine.resolve_debate_consensus(hyp, healthy_evals)
    # Average is 0.65. Standard deviation is ~0.17 (no sycophancy penalty)
    assert pytest.approx(score) == 0.65
    assert std_dev > 0.1

    # 2. Sycophantic debate (low cognitive diversity, everyone echoes 0.8)
    sycophantic_evals = {
        "Bayesian": 0.8,
        "Symbolic": 0.8,
        "Causal": 0.8,
        "Economic": 0.8,
        "Game-Theoretic": 0.8,
        "Mechanistic": 0.8
    }
    s_score, s_std_dev = engine.resolve_debate_consensus(hyp, sycophantic_evals)
    # Average is 0.8, but std_dev is 0.0, triggering sycophancy penalty of 0.8x
    assert s_std_dev < 1e-9
    assert pytest.approx(s_score) == 0.64  # 0.8 * 0.8


def test_red_team_ucb1_mcts_convergence() -> None:
    """Test our newly added Phase 10 exact UCB-1 MCTS convergence choosing exploration vs exploitation."""
    from apodex.cognition.planning.unified_planner import UnifiedPlanner

    planner = UnifiedPlanner()

    policy_high_visits = {
        "name": "policy_frequent_exploitation",
        "visits": 100,
        "probability_of_success": 0.9,
        "expected_business_value": 0.8
    }
    policy_low_visits = {
        "name": "policy_unexplored_curiosity",
        "visits": 1,
        "probability_of_success": 0.5,
        "expected_business_value": 0.4
    }

    # Total visits = 101. Exploring highly curious path with curiosity_weight = 2.0
    best, ucb = planner.run_mcts_rollout(
        starting_state={},
        policies=[policy_high_visits, policy_low_visits],
        curiosity_weight=2.0
    )

    # Low visits node should get selected because of UCB-1 exploration bonus
    assert best["name"] == "policy_unexplored_curiosity"


def test_red_team_spawning_inflation_limit() -> None:
    """Test dynamic agent capacity limits protecting against inflation/starvation."""
    from apodex.cognition.research.autonomous_institution import ConsensAgentEngine

    # Safe hard maximum capacity of 3 active agents
    engine = ConsensAgentEngine(max_agent_capacity=3)

    a1 = engine.spawn_agent("Researcher_1", "Research", [])
    a2 = engine.spawn_agent("Researcher_2", "Research", [])
    a3 = engine.spawn_agent("Researcher_3", "Research", [])

    assert sum(1 for a in engine.active_agents.values() if a.is_active) == 3

    # Spawning a fourth agent must trigger auto-retirement of a1 to respect capacity limits
    a4 = engine.spawn_agent("Researcher_4", "Research", [])

    assert engine.active_agents[a1.agent_id].is_active is False
    assert sum(1 for a in engine.active_agents.values() if a.is_active) == 3


def test_red_team_memory_recall_reinforcement() -> None:
    """Test our active recall memory reinforcement offsetting Ebbinghaus forgetting curves."""
    from apodex.cognition.memory.unified_memory import UnifiedMemory
    from apodex.cognition.shared.schemas import EvidenceCard

    memory = UnifiedMemory()
    ev = EvidenceCard(source="Laboratory", description="Causal evidence statement of caching performance.", reliability=0.5)
    memory.add_evidence(ev)

    # Retrieval should trigger memory recall reinforcement and boost reliability/confidence
    retrieved = memory.retrieve_similar_evidence("caching performance")
    assert len(retrieved) == 1
    assert retrieved[0].reliability > 0.5
    assert retrieved[0].reliability == pytest.approx(0.65)
