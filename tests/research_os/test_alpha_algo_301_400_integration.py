# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite validating
the 100 new research paper corpus (IDs 301-400), zero overlap across all 400 papers,
principle registration, literature review querying, and enhanced runtime components.
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_400_paper_corpus_zero_overlap():
    """Verifies that all papers in 301-400 have zero title and DOI overlap with papers 1-300."""
    yaml_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    ]

    all_titles = []
    all_dois = []
    paper_counts = {}

    for path in yaml_paths:
        assert os.path.exists(path), f"Expected research YAML database at {path}"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        papers = data.get("papers", []) if isinstance(data, dict) else data
        paper_counts[path] = len(papers)
        for p in papers:
            meta = p["metadata"]
            all_titles.append(meta["title"].strip().lower())
            if meta.get("doi"):
                all_dois.append(meta["doi"].strip().lower())

    assert paper_counts["docs/research/papers/AI_EOS_RESEARCH_DB.yaml"] == 200
    assert paper_counts["docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"] == 100
    assert paper_counts["docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"] == 100
    assert len(all_titles) == 400
    assert len(set(all_titles)) == 400, "Found duplicate titles in the 400-paper corpus!"
    assert len(all_dois) == len(set(all_dois)), "Found duplicate DOIs in the 400-paper corpus!"


def test_principle_registration_and_literature_review():
    """Verifies principles registration and querying in ResearchOS literature review."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) >= 4

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")
    assert review["domain"] == "Active Inference"
    assert review["reviewed_citations_count"] >= 4
    assert review["matched_principles_count"] >= 1
    assert any("EFE_BUDGET_DECAY" in p.get("principle_id", "") for p in review["extracted_principles"])


def test_code_rewrite_engine_hawkes_ast_check():
    """Verifies Hawkes non-Gaussian AST recursion depth check in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=["/tmp"], max_recursion_depth=2)

    # Valid non-recursive snippet
    valid_snippet = "def calculate_yield(x, y):\n    return x + y\n"
    prop_valid = RewriteProposal(
        target_filepath="/tmp/test_valid.py",
        original_snippet="",
        proposed_snippet=valid_snippet,
        rationale="Standard function"
    )
    assert engine.verify_proposal_ast(prop_valid) is True

    # Snippet with excessive recursion (calls calculate_yield 3 times inside calculate_yield)
    recursive_snippet = (
        "def calculate_yield(x):\n"
        "    if x <= 0: return 0\n"
        "    a = calculate_yield(x-1)\n"
        "    b = calculate_yield(x-2)\n"
        "    c = calculate_yield(x-3)\n"
        "    return a + b + c\n"
    )
    prop_recursive = RewriteProposal(
        target_filepath="/tmp/test_rec.py",
        original_snippet="",
        proposed_snippet=recursive_snippet,
        rationale="Excessive recursion"
    )
    assert engine.verify_proposal_ast(prop_recursive) is False


def test_genetic_optimizer_boolean_mutation_and_migration():
    """Verifies boolean type preservation in mutation and immediate sorting on elite migration."""
    opt = GeneticWorkflowOptimizer(population_size=5, mutation_rate=1.0)
    params = {"threshold": 0.5, "flag": True}
    opt.initialize_population("Base template", params)

    # Check bool parameter type preserved
    for genome in opt.population:
        assert isinstance(genome.parameters["flag"], bool)

    # Test island migration gate
    elite = ProgramGenome(
        prompt_template="Migrated Elite",
        parameters={"threshold": 0.9, "flag": False},
        fitness_score=99.0
    )
    opt.insert_elite_migration(elite)
    assert opt.population[0].fitness_score == 99.0
    assert opt.population[0].prompt_template == "Migrated Elite"


def test_sft_preference_collector_advantage_clipping():
    """Verifies advantage margin clipping in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(discount_factor=0.9, max_advantage_margin=5.0)

    steps_a = [TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=10.0, reward=20.0)]
    steps_b = [TrajectoryStep(action="b1", predicted_expectation=0.0, actual_outcome=1.0, reward=1.0)]

    pair = collector.compile_dpo_preference_pair("Prompt", steps_a, steps_b)
    assert pair["raw_margin"] > 5.0
    assert pair["margin"] == 5.0  # Clipped to max_advantage_margin


def test_learnable_routing_gate_budget_decay():
    """Verifies budget-decayed cost penalty scaling in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="agent_high_cost",
        domain_specialty="trading",
        cost_per_token=0.05,
        historical_success_rate=0.8,
        epistemic_curiosity=0.2
    )
    agent_b = SpecializedAgentProfile(
        agent_id="agent_low_cost",
        domain_specialty="trading",
        cost_per_token=0.001,
        historical_success_rate=0.75,
        epistemic_curiosity=0.2
    )

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    # High budget remaining -> prefers high success rate agent_a
    route1 = dispatcher.route_task(task_complexity=10.0, domain="trading")

    # Consume budget up to 90%
    dispatcher.budget_spent = 9.0

    # Low budget remaining -> budget decay penalty forces fallback to low cost agent_b
    route2 = dispatcher.route_task(task_complexity=10.0, domain="trading")
    assert route2 == "agent_low_cost"
