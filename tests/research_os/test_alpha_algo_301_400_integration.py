# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Comprehensive integration test suite validating
the 301-400 research paper corpus integrity, principle registration, runtime enhancements,
and flaw fixes in AlphaAlgo / Research OS.
"""

import pytest
import os
import glob
import yaml
from typing import List, Dict, Any

from apodex.ai_eos.research.integration import (
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
)


def test_zero_corpus_overlap_301_400():
    """Validates 100% zero Jaccard title and DOI overlap across all 400 papers."""
    existing_titles: Dict[str, str] = {}
    existing_dois: Dict[str, str] = {}
    all_papers: Dict[int, str] = {}

    yaml_files = sorted(glob.glob("docs/research/papers/*.yaml"))
    assert len(yaml_files) >= 3, f"Expected at least 3 research YAML files, found {len(yaml_files)}"

    for path in yaml_files:
        if "INGESTION" in path:
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        papers: List[Dict[str, Any]] = []
        if isinstance(data, dict):
            p_data = data.get("papers", data)
            if isinstance(p_data, dict):
                papers = list(p_data.values())
            elif isinstance(p_data, list):
                papers = p_data
        elif isinstance(data, list):
            papers = data

        for p in papers:
            if not isinstance(p, dict):
                continue
            pid = p.get("id") or p.get("paper_id")
            title = (p.get("title") or p.get("metadata", {}).get("title", "")).strip().lower()
            doi = (p.get("doi") or p.get("metadata", {}).get("doi", "")).strip().lower()

            assert pid not in all_papers, f"Duplicate Paper ID {pid} found in {path}"
            all_papers[pid] = path

            if title:
                assert title not in existing_titles, f"Duplicate title '{title}' found in {path} (already in {existing_titles[title]})"
                existing_titles[title] = path

            if doi:
                assert doi not in existing_dois, f"Duplicate DOI '{doi}' found in {path} (already in {existing_dois[doi]})"
                existing_dois[doi] = path

    assert len(all_papers) >= 400, f"Expected 400 total papers across research DBs, got {len(all_papers)}"


def test_principle_registration_301_400():
    """Validates principle registration for papers 301-400."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 4
    assert principles == ALPHAALGO_301_400_PRINCIPLES

    principle_ids = [p["principle_id"] for p in principles]
    assert "P301_400_01" in principle_ids
    assert "P301_400_02" in principle_ids
    assert "P301_400_03" in principle_ids
    assert "P301_400_04" in principle_ids


def test_hawkes_ast_recursion_limit():
    """Validates Hawkes non-Gaussian recursive AST call depth check in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=["."])

    recursive_snippet = """
def rec_fn(n):
    if n <= 0:
        return 0
    return rec_fn(n - 1) + rec_fn(n - 2) + rec_fn(n - 3) + rec_fn(n - 4) + rec_fn(n - 5) + rec_fn(n - 6)
"""
    normal_snippet = """
def norm_fn(x):
    return sum([i * 2 for i in range(x)])
"""

    prop_bad = engine.propose_rewrite("test.py", "a = 1", recursive_snippet, "Hawkes test")
    prop_good = engine.propose_rewrite("test.py", "a = 1", normal_snippet, "Hawkes test")

    assert engine.verify_proposal_ast(prop_bad, max_recursion_depth=5) is False
    assert engine.verify_proposal_ast(prop_good, max_recursion_depth=5) is True


def test_island_map_elites_migration():
    """Validates island MAP-Elites migration gates in GeneticWorkflowOptimizer."""
    opt_a = GeneticWorkflowOptimizer(population_size=3)
    opt_b = GeneticWorkflowOptimizer(population_size=3)

    opt_a.population = [
        ProgramGenome(prompt_template="t1", fitness_score=100.0),
        ProgramGenome(prompt_template="t2", fitness_score=90.0),
        ProgramGenome(prompt_template="t3", fitness_score=80.0),
    ]

    opt_b.population = [
        ProgramGenome(prompt_template="tb1", fitness_score=10.0),
        ProgramGenome(prompt_template="tb2", fitness_score=5.0),
        ProgramGenome(prompt_template="tb3", fitness_score=1.0),
    ]

    migrated_count = opt_b.migrate_elites_between_islands(opt_a.population, migration_rate=0.33)
    assert migrated_count == 1
    assert opt_b.population[0].fitness_score == 100.0


def test_clipped_advantage_margin():
    """Validates advantage margin clipping in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector()

    steps_high = [
        TrajectoryStep(action="action1", predicted_expectation=0.0, actual_outcome=500.0, reward=500.0)
    ]
    steps_low = [
        TrajectoryStep(action="action2", predicted_expectation=0.0, actual_outcome=0.0, reward=0.0)
    ]

    pair = collector.compile_dpo_preference_pair("Prompt", steps_high, steps_low, max_margin_clip=10.0)
    assert pair["margin"] == 10.0
    assert pair["raw_margin"] == 500.0


def test_budget_decayed_efe_routing():
    """Validates budget-decayed Expected Free Energy task routing in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    ag_curious = SpecializedAgentProfile(
        agent_id="curious_agent",
        domain_specialty="general",
        cost_per_token=0.1,
        historical_success_rate=0.5,
        epistemic_curiosity=5.0,
    )

    dispatcher.register_subagent(ag_curious)

    # Full budget -> high curiosity weighting
    route_full = dispatcher.route_task(task_complexity=1.0, domain="general")
    assert route_full == "curious_agent"

    # Deplete budget near limit
    dispatcher.budget_spent = 9.9
    route_depleted = dispatcher.route_task(task_complexity=0.5, domain="general")
    assert route_depleted == "curious_agent"  # Single agent available
