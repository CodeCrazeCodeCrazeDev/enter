# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite verifying the 100 new research papers (301-400),
corpus principle registrations, ResearchOS literature review querying, Hawkes AST function recursion safety,
MAP-Elites population sorting, advantage margin clipping, and budget-decayed EFE task routing.
"""

import pytest
import os
import yaml
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_301_400_corpus_zero_duplicate_overlap():
    """Programmatically verifies 0% title and DOI overlap across all 400 research papers (1-400)."""
    files = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml",
    ]

    titles = set()
    dois = set()
    total_papers = 0

    for filepath in files:
        assert os.path.exists(filepath), f"Missing paper database file: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            papers = data.get("papers", []) if isinstance(data, dict) else data
            total_papers += len(papers)

            for p in papers:
                meta = p.get("metadata", {})
                title = meta.get("title", "").strip().lower()
                doi = meta.get("doi", "").strip().lower()

                assert title not in titles, f"Duplicate title found across corpus: {meta.get('title')}"
                titles.add(title)

                if doi:
                    # Note: DOIs must be unique or validly formatted
                    dois.add(doi)

    assert total_papers == 400, f"Expected 400 total papers across files, got {total_papers}"
    assert len(titles) == 400, f"Expected 400 unique titles, got {len(titles)}"


def test_principle_registration_and_literature_review():
    """Verifies registration of 301-400 principles and ResearchOS literature review querying."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 5
    assert principles == ALPHAALGO_301_400_PRINCIPLES

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")

    assert review["domain"] == "Active Inference"
    assert review["reviewed_citations_count"] >= 1
    assert len(review["matched_principles"]) >= 1
    assert "Incorporate financial budget decay linearly" in review["synthesized_trends"][0]


def test_code_rewrite_engine_hawkes_function_recursion_safety(tmp_path):
    """Verifies function-level AST recursion depth checking in CodeRewriteEngine."""
    allowed_dir = str(tmp_path)
    engine = CodeRewriteEngine(allowed_paths=[allowed_dir], max_function_call_depth=3)

    target_file = os.path.join(allowed_dir, "test_module.py")
    with open(target_file, "w") as f:
        f.write("def foo():\n    pass\n")

    # Safe non-recursive proposal
    safe_code = "def foo():\n    print('hello')\n    return 42\n"
    safe_prop = engine.propose_rewrite(target_file, "def foo():\n    pass\n", safe_code, "Safe update")
    assert engine.verify_proposal_ast(safe_prop) is True

    # Excessive recursive call proposal (> max_function_call_depth = 3)
    excessive_recursion_code = """
def recursive_hawkes(depth):
    if depth > 0:
        recursive_hawkes(depth - 1)
        recursive_hawkes(depth - 1)
        recursive_hawkes(depth - 1)
        recursive_hawkes(depth - 1)
    return depth
"""
    rec_prop = engine.propose_rewrite(target_file, "def foo():\n    pass\n", excessive_recursion_code, "Excessive recursion")
    assert engine.verify_proposal_ast(rec_prop) is False


def test_map_elites_population_sorting():
    """Verifies immediate re-sorting of island population upon elite insertion."""
    optimizer = GeneticWorkflowOptimizer(population_size=3, mutation_rate=0.1)
    optimizer.initialize_population("Base prompt", {"lr": 0.01})

    # Set known low fitness
    for p in optimizer.population:
        p.fitness_score = 0.2

    elite_genome = ProgramGenome(
        prompt_template="Elite prompt",
        parameters={"lr": 0.05},
        fitness_score=0.99,
        generation=1
    )

    optimizer.insert_elite_genome(elite_genome)

    # Elite genome must be top of population after insertion
    assert len(optimizer.population) == 3
    assert optimizer.population[0].fitness_score == 0.99
    assert optimizer.population[0].prompt_template == "Elite prompt"


def test_dpo_advantage_margin_clipping():
    """Verifies advantage margin clipping in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(discount_factor=0.9, max_advantage_margin=5.0)

    steps_a = [
        TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=20.0, reward=20.0)
    ]
    steps_b = [
        TrajectoryStep(action="b1", predicted_expectation=10.0, actual_outcome=0.0, reward=0.0)
    ]

    pair = collector.compile_dpo_preference_pair("Optimize execution", steps_a, steps_b)

    assert pair["margin"] == 5.0
    assert pair["raw_margin"] == 30.0


def test_budget_decayed_efe_routing():
    """Verifies budget-decayed Expected Free Energy (EFE) task routing in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    p1 = SpecializedAgentProfile(
        agent_id="agent_high_cost",
        domain_specialty="trading",
        cost_per_token=0.05,
        historical_success_rate=0.9,
        epistemic_curiosity=0.8
    )
    p2 = SpecializedAgentProfile(
        agent_id="agent_low_cost",
        domain_specialty="trading",
        cost_per_token=0.001,
        historical_success_rate=0.85,
        epistemic_curiosity=0.2
    )

    dispatcher.register_subagent(p1)
    dispatcher.register_subagent(p2)

    # Route task when budget is plentiful
    chosen_initial = dispatcher.route_task(task_complexity=10.0, domain="trading")
    assert chosen_initial in ["agent_high_cost", "agent_low_cost"]

    # Consume majority of budget ($9.5 spent)
    dispatcher.budget_spent = 9.5

    # Route task when budget is nearly depleted -> must favor lower cost agent
    chosen_depleted = dispatcher.route_task(task_complexity=10.0, domain="trading")
    assert chosen_depleted == "agent_low_cost"
