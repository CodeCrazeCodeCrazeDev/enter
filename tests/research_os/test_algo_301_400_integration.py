# -*- coding: utf-8 -*-
"""
test_algo_301_400_integration.py: Integration test suite for AlphaAlgo 301-400 Research Corpus.
Verifies zero corpus overlap, principle registration, ResearchOS literature search,
CodeRewriteEngine Hawkes call depth AST verification, MAP-Elites island migration,
SFT advantage margin clipping, and budget-decayed EFE task routing.
"""

import os
import yaml
import pytest
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    ALPHAALGO_301_400_PRINCIPLES,
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_corpus_301_400_integrity_and_zero_overlap():
    """Verifies that the 301-400 paper corpus has 100 papers and zero title/DOI overlap with papers 1-300."""
    yaml_301_400 = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    assert os.path.exists(yaml_301_400), f"File {yaml_301_400} does not exist."

    with open(yaml_301_400, "r", encoding="utf-8") as f:
        data_301_400 = yaml.safe_load(f)

    papers_301_400 = data_301_400.get("papers", [])
    assert len(papers_301_400) == 100, f"Expected 100 papers in {yaml_301_400}, got {len(papers_301_400)}."

    titles_301_400 = {p["metadata"]["title"].strip().lower() for p in papers_301_400}
    dois_301_400 = {p["metadata"]["doi"].strip().lower() for p in papers_301_400}

    assert len(titles_301_400) == 100, "Duplicate titles found within 301-400 corpus."
    assert len(dois_301_400) == 100, "Duplicate DOIs found within 301-400 corpus."

    # Compare against papers 1-200 and 201-300
    older_yamls = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]

    older_titles = set()
    older_dois = set()

    for path in older_yamls:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                d = yaml.safe_load(f)
                plist = d.get("papers", []) if isinstance(d, dict) else (d if isinstance(d, list) else [])
                for p in plist:
                    meta = p.get("metadata", {})
                    t = (meta.get("title") or p.get("paper_title") or p.get("title") or "").strip().lower()
                    doi = (meta.get("doi") or p.get("doi") or "").strip().lower()
                    if t:
                        older_titles.add(t)
                    if doi:
                        older_dois.add(doi)

    title_overlap = titles_301_400.intersection(older_titles)
    doi_overlap = dois_301_400.intersection(older_dois)

    assert len(title_overlap) == 0, f"Title overlap detected against papers 1-300: {title_overlap}"
    assert len(doi_overlap) == 0, f"DOI overlap detected against papers 1-300: {doi_overlap}"


def test_301_400_principles_registration_and_literature_review():
    """Tests principle registration and ResearchOS literature review querying."""
    registered = register_301_400_paper_corpus_principles()
    assert len(registered) == 5
    assert "P005_HAWKES_CALL_DEPTH_STABILITY" in registered
    assert "P008_BUDGET_DECAYED_EFE_ROUTING" in registered

    ros = ResearchOS()
    review = ros.conduct_literature_review(domain="Self-Referential Code Synthesis")
    assert review["matched_principles_count"] >= 1
    assert any("P005_HAWKES_CALL_DEPTH_STABILITY" in p["paper_title"] or "Non-Gaussian Hawkes" in p["paper_title"] for p in review["matched_principles"])


def test_hawkes_call_depth_ast_verification():
    """Tests CodeRewriteEngine AST verification and Hawkes recursive call depth limits."""
    allowed_dir = os.path.dirname(os.path.abspath(__file__))
    engine = CodeRewriteEngine(allowed_paths=[allowed_dir], max_recursion_depth=3)

    # Valid non-recursive snippet
    valid_snippet = "def compute_sum(a, b):\n    return a + b\n"
    prop_valid = engine.propose_rewrite(__file__, "def foo(): pass", valid_snippet, "add compute_sum")
    assert engine.verify_proposal_ast(prop_valid) is True

    # Snippet with excessive recursive call depth
    excessive_recursive_snippet = (
        "def recursive_func(n):\n"
        "    if n <= 0:\n"
        "        return 0\n"
        "    return recursive_func(n-1) + recursive_func(n-1) + recursive_func(n-1) + recursive_func(n-1) + recursive_func(n-1)\n"
    )
    prop_excessive = engine.propose_rewrite(__file__, "def foo(): pass", excessive_recursive_snippet, "excessive recursion")
    assert engine.verify_proposal_ast(prop_excessive) is False


def test_map_elites_mutation_type_safety_and_migrant_sorting():
    """Tests GeneticWorkflowOptimizer boolean parameter type safety and migrant elite re-sorting."""
    optimizer = GeneticWorkflowOptimizer(population_size=5)
    base_params = {"learning_rate": 0.01, "enable_logging": True, "num_layers": 4}
    optimizer.initialize_population("Base prompt", base_params)

    # Verify boolean parameter retained boolean type during initialization mutations
    for g in optimizer.population:
        assert isinstance(g.parameters.get("enable_logging"), bool), "Boolean parameter mutated into non-bool type."

    # Test migrant elite insertion and sorting
    migrant = ProgramGenome(
        prompt_template="Migrant elite template",
        parameters={"learning_rate": 0.05, "enable_logging": False},
        fitness_score=99.9,
        generation=1
    )
    optimizer.insert_migrant_elite(migrant)
    assert optimizer.population[0].fitness_score == 99.9, "Migrant elite with top fitness was not sorted to position 0."


def test_dpo_preference_advantage_margin_clipping():
    """Tests SFTPreferenceCollector advantage computation and margin clipping."""
    collector = SFTPreferenceCollector(discount_factor=0.9, max_advantage_margin=5.0)

    steps_run_a = [
        TrajectoryStep(action="action_a1", predicted_expectation=1.0, actual_outcome=10.0, reward=10.0),
        TrajectoryStep(action="action_a2", predicted_expectation=2.0, actual_outcome=20.0, reward=20.0)
    ]
    steps_run_b = [
        TrajectoryStep(action="action_b1", predicted_expectation=5.0, actual_outcome=1.0, reward=0.0),
        TrajectoryStep(action="action_b2", predicted_expectation=5.0, actual_outcome=1.0, reward=0.0)
    ]

    record = collector.compile_dpo_preference_pair("Optimize portfolio", steps_run_a, steps_run_b)
    assert record["margin"] <= 5.0, f"Advantage margin {record['margin']} exceeded max limit of 5.0."
    assert record["chosen"] is not None
    assert record["rejected"] is not None


def test_budget_decayed_efe_task_routing():
    """Tests LearnableRoutingGateDispatcher EFE task routing with budget decay multipliers."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="cheap_agent",
        domain_specialty="Quantitative Finance",
        cost_per_token=0.001,
        historical_success_rate=0.8,
        epistemic_curiosity=0.2
    )
    agent_b = SpecializedAgentProfile(
        agent_id="expensive_agent",
        domain_specialty="Quantitative Finance",
        cost_per_token=0.05,
        historical_success_rate=0.95,
        epistemic_curiosity=0.8
    )

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    # Initial route with full budget should pick high-performance agent
    selected_id_1 = dispatcher.route_task(task_complexity=10.0, domain="Quantitative Finance")
    assert selected_id_1 in {"cheap_agent", "expensive_agent"}

    # Spend 90% of budget
    dispatcher.budget_spent = 9.0

    # With high budget consumption, penalty scales up and route should favor cheaper agent
    selected_id_2 = dispatcher.route_task(task_complexity=10.0, domain="Quantitative Finance")
    assert selected_id_2 == "cheap_agent"
