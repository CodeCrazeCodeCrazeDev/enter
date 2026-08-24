# -*- coding: utf-8 -*-
"""
test_research_integration.py: Verification and integration test suite covering
the high-fidelity transferable engineering integration layer.
"""

from __future__ import annotations
import os
import pytest
import tempfile
from typing import Dict, Any
from uuid import UUID

from apodex.ai_eos.research.integration import (
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    RewriteProposal,
    ProgramGenome,
    TrajectoryStep,
    SpecializedAgentProfile,
)


def test_code_rewrite_engine_security_and_sandbox() -> None:
    """Verifies that CodeRewriteEngine safely rewrites code while vetoing GRC and security failures."""
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = CodeRewriteEngine(allowed_paths=[tmpdir])
        target_file = os.path.join(tmpdir, "test_self_ref.py")

        # 1. Create a dummy initial file
        with open(target_file, "w") as f:
            f.write("def compute_val():\n    return 10\n")

        # 2. Propose a clean rewrite
        prop = engine.propose_rewrite(
            filepath=target_file,
            original_snippet="return 10",
            proposed_snippet="return 20",
            rationale="Update logic to return optimized coefficient."
        )

        # 3. Verify dry run and compilation
        assert engine.dry_run_simulation(prop) is True

        # 4. Commit the rewrite
        success = engine.commit_rewrite(prop)
        assert success is True

        # Verify content has updated
        with open(target_file, "r") as f:
            content = f.read()
        assert "return 20" in content
        assert "return 10" not in content

        # 5. Propose a dangerous rewrite violating GRC security rules (using eval)
        dangerous_prop = engine.propose_rewrite(
            filepath=target_file,
            original_snippet="return 20",
            proposed_snippet="return eval('30')",
            rationale="Unsafe eval usage."
        )
        assert engine.verify_proposal_ast(dangerous_prop) is False
        assert engine.commit_rewrite(dangerous_prop) is False


def test_genetic_workflow_optimizer() -> None:
    """Verifies that GeneticWorkflowOptimizer initializes diverse populations and mutates workflows."""
    optimizer = GeneticWorkflowOptimizer(population_size=6, mutation_rate=0.5)
    base_template = "Execute standard task step with outcome evaluation."
    base_params = {"learning_rate": 0.01, "use_verification": True}

    # Initialize diverse population
    optimizer.initialize_population(base_template, base_params)
    assert len(optimizer.population) == 6

    # Top elite is unchanged
    assert optimizer.population[0].prompt_template == base_template
    assert optimizer.population[0].parameters["learning_rate"] == 0.01

    # Mutants have differences or added template snippets
    mutant = optimizer.population[3]
    assert isinstance(mutant.parameters["learning_rate"], float)

    # Simulated scoring function evaluating performance based on parameters
    def mock_scoring_fn(genome: ProgramGenome) -> float:
        # Better fitness if verification is True and learning_rate is close to 0.02
        lr = genome.parameters.get("learning_rate", 0.01)
        ver = genome.parameters.get("use_verification", False)
        score = 1.0 - abs(0.02 - lr)
        if ver:
            score += 0.5
        return float(score)

    # Evaluate generation
    optimizer.evaluate_generation(mock_scoring_fn)
    assert optimizer.population[0].fitness_score >= optimizer.population[-1].fitness_score

    # Perform crossover and mutation
    original_best_fitness = optimizer.population[0].fitness_score
    optimizer.perform_crossover_and_mutation()
    assert len(optimizer.population) == 6
    # Elite retains generation 0, while offspring are generation 1
    assert optimizer.population[0].generation == 0
    assert any(g.generation == 1 for g in optimizer.population)


def test_sft_preference_collector() -> None:
    """Verifies that SFTPreferenceCollector correctly estimates advantage and synthesizes DPO pairs."""
    collector = SFTPreferenceCollector(discount_factor=0.9)

    # Construct Trajectory A (Excellent outcome)
    traj_a = [
        TrajectoryStep(action="query_database", predicted_expectation=0.5, actual_outcome=0.6, reward=0.6),
        TrajectoryStep(action="validate_provenance", predicted_expectation=0.6, actual_outcome=0.9, reward=0.9)
    ]
    # Construct Trajectory B (Sub-optimal outcome/errors)
    traj_b = [
        TrajectoryStep(action="query_database", predicted_expectation=0.5, actual_outcome=0.3, reward=0.2),
        TrajectoryStep(action="fallback_rule", predicted_expectation=0.3, actual_outcome=0.4, reward=0.4)
    ]

    # Compute advantages
    advantages_a = collector.compute_advantages(traj_a)
    advantages_b = collector.compute_advantages(traj_b)

    # Cum advantages of A must be higher than B
    assert sum(advantages_a) > sum(advantages_b)

    # Compile preference DPO pair
    dpo_pair = collector.compile_dpo_preference_pair(
        prompt="Verify and trace database records.",
        steps_run_a=traj_a,
        steps_run_b=traj_b
    )

    assert dpo_pair["prompt"] == "Verify and trace database records."
    assert "validate_provenance" in dpo_pair["chosen"]
    assert "fallback_rule" in dpo_pair["rejected"]
    assert dpo_pair["margin"] > 0.0


def test_learnable_routing_gate_dispatcher() -> None:
    """Verifies that LearnableRoutingGateDispatcher optimalizes agent selection based on EFE and budget."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=1.50)

    # Register sub-agents
    agent_science = SpecializedAgentProfile(
        agent_id="agent_science",
        domain_specialty="AI Research",
        cost_per_token=0.005,
        historical_success_rate=0.85,
        epistemic_curiosity=0.60
    )
    agent_finance = SpecializedAgentProfile(
        agent_id="agent_finance",
        domain_specialty="Quantitative Finance",
        cost_per_token=0.010,
        historical_success_rate=0.90,
        epistemic_curiosity=0.40
    )
    agent_cheap = SpecializedAgentProfile(
        agent_id="agent_cheap",
        domain_specialty="General Operations",
        cost_per_token=0.001,
        historical_success_rate=0.50,
        epistemic_curiosity=0.20
    )

    dispatcher.register_subagent(agent_science)
    dispatcher.register_subagent(agent_finance)
    dispatcher.register_subagent(agent_cheap)

    # Route AI Research task (task complexity = 50 tokens)
    selected_id_1 = dispatcher.route_task(task_complexity=50, domain="AI Research")
    assert selected_id_1 == "agent_science"

    # Route task when budget is severely constrained
    # Spend up the budget to leave only tiny amount
    dispatcher.budget_spent = 1.48
    # Complexity of 10 tokens on agent_science would cost 10 * 0.005 = 0.05, exceeding limit
    # The cheap agent costs 10 * 0.001 = 0.01, which fits remaining budget
    selected_id_2 = dispatcher.route_task(task_complexity=10, domain="AI Research")
    assert selected_id_2 == "agent_cheap"

    # Update success params
    dispatcher.budget_spent = 0.0
    dispatcher.update_routing_parameters(agent_id="agent_cheap", success=True, cost_incurred=0.01)
    assert dispatcher.agents["agent_cheap"].historical_success_rate > 0.50
    assert dispatcher.agents["agent_cheap"].epistemic_curiosity < 0.20


def test_200_paper_corpus_principles_registration_and_query() -> None:
    """Verifies indexing and querying of transferable engineering principles from the 200-paper corpus."""
    from apodex.ai_eos.research.integration import (
        register_200_paper_corpus_principles,
        query_transferable_principles,
    )
    from apodex.ai_eos.research.research_os import ResearchOS

    # 1. Register corpus principles
    registry = register_200_paper_corpus_principles()
    assert len(registry) == 200
    assert 1 in registry
    assert 200 in registry

    # Check structure of Paper #1
    paper1 = registry[1]
    assert paper1["id"] == 1
    assert "Awesome-Agent-Papers" in paper1["title"]

    # 2. Query transferable principles for Active Inference
    matches = query_transferable_principles("Active Inference", top_k=5)
    assert len(matches) > 0
    assert any("active inference" in str(m).lower() or "inference" in str(m).lower() for m in matches)

    # 3. Test ResearchOS integration conducting literature review
    ros = ResearchOS()
    lit_review = ros.conduct_literature_review("Active Inference")
    assert lit_review["reviewed_citations_count"] == 200
    assert lit_review["matching_principles_count"] > 0
    assert len(lit_review["synthesized_trends"]) > 0
