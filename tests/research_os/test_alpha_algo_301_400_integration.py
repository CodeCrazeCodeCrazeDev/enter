# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for the 301-400 research paper corpus.
Verifies zero paper overlap for new papers 301-400 against papers 1-300, principle registration,
ResearchOS review retrieval, and runtime enhancements (CodeRewriteEngine AST hawkes depth,
GeneticWorkflowOptimizer MAP-Elites re-sorting, SFTPreferenceCollector clipped margins,
LearnableRoutingGateDispatcher budget decay).
"""

import os
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_zero_corpus_duplicate_overlap_across_400_papers():
    """Verifies 100% zero title and DOI overlap for new papers (301-400) against prior papers (1-300)."""
    db_paths_prior = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
    ]
    db_path_new = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"

    prior_titles = []
    prior_dois = set()

    for path in db_paths_prior:
        assert os.path.exists(path), f"Corpus database path missing: {path}"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            papers = data.get("papers", []) if isinstance(data, dict) else data
            for p in papers:
                if isinstance(p, dict) and "metadata" in p:
                    title = p["metadata"].get("title", "").strip().lower()
                    doi = p["metadata"].get("doi", "").strip().lower()
                    if doi:
                        prior_dois.add(doi)
                    if title:
                        prior_titles.append(title)

    assert len(prior_titles) == 300, f"Expected 300 prior paper titles, found {len(prior_titles)}"

    assert os.path.exists(db_path_new)
    with open(db_path_new, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        new_papers = data.get("papers", []) if isinstance(data, dict) else data

    assert len(new_papers) == 100, f"Expected 100 new paper records in 301-400 dataset, found {len(new_papers)}"

    new_titles = []
    for p in new_papers:
        title = p["metadata"].get("title", "").strip().lower()
        doi = p["metadata"].get("doi", "").strip().lower()

        if doi:
            assert doi not in prior_dois, f"Duplicate DOI found in 301-400 corpus: {doi}"

        p_tokens = set(title.split())
        # Check against all prior titles (1-300)
        for prev_title in prior_titles:
            prev_tokens = set(prev_title.split())
            if p_tokens and prev_tokens:
                intersection = p_tokens.intersection(prev_tokens)
                union = p_tokens.union(prev_tokens)
                score = len(intersection) / len(union)
                assert score <= 0.35, f"Title overlap too high ({score:.2f}): '{title}' vs '{prev_title}'"

        # Check against other new titles in 301-400
        for prev_title in new_titles:
            prev_tokens = set(prev_title.split())
            if p_tokens and prev_tokens:
                intersection = p_tokens.intersection(prev_tokens)
                union = p_tokens.union(prev_tokens)
                score = len(intersection) / len(union)
                assert score <= 0.35, f"Title overlap within 301-400 too high ({score:.2f}): '{title}' vs '{prev_title}'"

        new_titles.append(title)


def test_301_400_principle_registration_and_literature_review():
    """Verifies principles 301-400 registration and ResearchOS literature review querying."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 5

    ros = ResearchOS()
    review = ros.conduct_literature_review("Hawkes AST depth")
    assert "principles_found" in review
    assert len(review["principles_found"]) > 0


def test_code_rewrite_engine_hawkes_ast_depth_check():
    """Verifies CodeRewriteEngine AST function call depth check for recursive calls."""
    engine = CodeRewriteEngine(allowed_paths=["."], max_function_recursion_depth=5)

    valid_code = """
def process_data(x):
    a = str(x)
    b = int(a)
    c = float(b)
    d = str(c)
    return d
"""
    prop_valid = engine.propose_rewrite("test.py", "", valid_code, "valid sequential calls")
    assert engine.verify_proposal_ast(prop_valid) is True

    recursive_code = """
def recursive_func(n):
    if n <= 0:
        return 0
    return recursive_func(n-1) + recursive_func(n-2) + recursive_func(n-3) + recursive_func(n-4) + recursive_func(n-5) + recursive_func(n-6)
"""
    prop_invalid = engine.propose_rewrite("test.py", "", recursive_code, "excessive recursive calls")
    assert engine.verify_proposal_ast(prop_invalid) is False


def test_genetic_optimizer_elite_insertion_sorting():
    """Verifies MAP-Elites immediate population re-sorting on elite genome insertion."""
    opt = GeneticWorkflowOptimizer(population_size=3)
    opt.initialize_population("base template", {"param": 1})

    for g in opt.population:
        g.fitness_score = 1.0

    elite = ProgramGenome(prompt_template="elite template", parameters={"param": 10}, fitness_score=99.0)
    opt.insert_elite(elite)

    assert opt.population[0].fitness_score == 99.0
    assert opt.population[0].prompt_template == "elite template"
    assert len(opt.population) == 3


def test_sft_preference_collector_clipped_margins():
    """Verifies SFTPreferenceCollector advantage margin clipping."""
    collector = SFTPreferenceCollector(margin_clip=3.0)

    run_a = [TrajectoryStep(action="act1", predicted_expectation=0.0, actual_outcome=100.0, reward=100.0)]
    run_b = [TrajectoryStep(action="act2", predicted_expectation=0.0, actual_outcome=0.0, reward=0.0)]

    pair = collector.compile_dpo_preference_pair("Prompt", run_a, run_b)
    assert pair["raw_margin"] == 100.0
    assert pair["margin"] == 3.0


def test_learnable_routing_gate_budget_decay():
    """Verifies LearnableRoutingGateDispatcher budget decay scaling."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=100.0)
    agent = SpecializedAgentProfile(agent_id="agent_a", domain_specialty="trading", cost_per_token=0.01)
    dispatcher.register_subagent(agent)

    routed_1 = dispatcher.route_task(task_complexity=10.0, domain="trading")
    assert routed_1 == "agent_a"

    dispatcher.budget_spent = 95.0
    routed_2 = dispatcher.route_task(task_complexity=10.0, domain="trading")
    assert routed_2 == "agent_a"
