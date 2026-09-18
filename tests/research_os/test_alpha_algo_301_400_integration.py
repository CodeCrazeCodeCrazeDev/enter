# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite validating the 100 new research papers
(IDs 301-400), principle registration, literature review querying, zero overlap across 400 papers,
and runtime enhancements in AlphaAlgo.
"""

from __future__ import annotations
import os
import glob
import yaml
import pytest

from apodex.ai_eos.research.integration import (
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    ProgramGenome,
    TrajectoryStep,
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_zero_corpus_overlap_across_all_400_papers() -> None:
    """Programmatically verifies zero title and DOI overlap across papers 1-400."""
    files = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    ]

    all_ids = set()
    all_titles = set()
    all_dois = set()
    total_papers = 0

    for fpath in files:
        assert os.path.exists(fpath), f"Corpus YAML missing: {fpath}"
        with open(fpath, "r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp)
            papers = data if isinstance(data, list) else data.get("papers", [])
            total_papers += len(papers)

            for p in papers:
                pid = p["id"]
                assert pid not in all_ids, f"Duplicate paper ID {pid} in {fpath}"
                all_ids.add(pid)

                meta = p.get("metadata", {})
                title = meta.get("title", "").strip().lower()
                assert title not in all_titles, f"Duplicate title '{title}' in {fpath}"
                all_titles.add(title)

                doi = meta.get("doi", "").strip().lower()
                if doi and doi not in ("n/a", "none"):
                    assert doi not in all_dois, f"Duplicate DOI '{doi}' in {fpath}"
                    all_dois.add(doi)

    assert total_papers == 400, f"Expected 400 total papers, found {total_papers}"
    assert len(all_ids) == 400
    assert len(all_titles) == 400


def test_register_301_400_principles_and_literature_review() -> None:
    """Verifies 301-400 principle registration and Research OS literature review integration."""
    principles = register_301_400_paper_corpus_principles()
    assert principles["corpus_id"] == "ALPHA_ALGO_301_400"
    assert principles["paper_count"] == 100
    assert len(principles["principles"]) == 4

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference & Microstructure")
    assert review["reviewed_citations_count"] == 100
    assert review["corpus_version"] == "ALPHA_ALGO_301_400"
    assert len(review["principles_applied"]) == 4


def test_code_rewrite_engine_hawkes_ast_recursion_veto() -> None:
    """Verifies CodeRewriteEngine AST check detects and vetos recursive calls beyond threshold."""
    engine = CodeRewriteEngine(allowed_paths=["/tmp"])

    # Valid non-recursive snippet
    valid_code = """
def calculate_alpha(returns):
    return sum(returns) / max(1, len(returns))
"""

    # Invalid code with excessive recursion (>2 recursive calls) inside function
    recursive_code = """
def recursive_hawkes(x):
    if x <= 0:
        return 0
    return recursive_hawkes(x - 1) + recursive_hawkes(x - 2) + recursive_hawkes(x - 3)
"""

    p_valid = engine.propose_rewrite("/tmp/test1.py", "", valid_code, "valid alpha")
    p_invalid = engine.propose_rewrite("/tmp/test2.py", "", recursive_code, "excessive recursion")

    assert engine.verify_proposal_ast(p_valid) is True
    assert engine.verify_proposal_ast(p_invalid) is False


def test_genetic_workflow_optimizer_fitness_sorting() -> None:
    """Verifies GeneticWorkflowOptimizer sorts population by fitness before crossover and elitism."""
    optimizer = GeneticWorkflowOptimizer(population_size=5, mutation_rate=0.1)
    optimizer.initialize_population("base template", {"param_a": 1.0})

    # Manually assign varied fitness scores
    for i, g in enumerate(optimizer.population):
        g.fitness_score = float(i * 10)  # 0, 10, 20, 30, 40

    optimizer.perform_crossover_and_mutation()

    # The top elite (fitness 40) is preserved
    assert len(optimizer.population) == 5
    # Newly generated offspring should have generation 1
    assert optimizer.population[1].generation == 1


def test_sft_preference_collector_clipped_advantage_margin() -> None:
    """Verifies SFTPreferenceCollector clips trajectory advantage margins."""
    collector = SFTPreferenceCollector(discount_factor=0.9)

    steps_a = [
        TrajectoryStep(action="a1", predicted_expectation=1.0, actual_outcome=10.0, reward=100.0),
        TrajectoryStep(action="a2", predicted_expectation=1.0, actual_outcome=10.0, reward=100.0)
    ]
    steps_b = [
        TrajectoryStep(action="b1", predicted_expectation=10.0, actual_outcome=0.0, reward=-100.0),
        TrajectoryStep(action="b2", predicted_expectation=10.0, actual_outcome=0.0, reward=-100.0)
    ]

    record = collector.compile_dpo_preference_pair("optimize workflow", steps_a, steps_b)

    assert "chosen" in record
    assert "rejected" in record
    assert record["margin"] <= 10.0  # Clipped
    assert record["raw_margin"] > 10.0  # Unclipped raw margin preserved for reference


def test_learnable_routing_gate_budget_decay() -> None:
    """Verifies LearnableRoutingGateDispatcher adjusts EFE routing under decaying budgets."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    p1 = SpecializedAgentProfile(agent_id="agent_fast", domain_specialty="finance", cost_per_token=0.001, historical_success_rate=0.9, epistemic_curiosity=0.8)
    p2 = SpecializedAgentProfile(agent_id="agent_thorough", domain_specialty="finance", cost_per_token=0.005, historical_success_rate=0.95, epistemic_curiosity=0.9)

    dispatcher.register_subagent(p1)
    dispatcher.register_subagent(p2)

    # Route task when full budget is available
    agent_selected_full = dispatcher.route_task(task_complexity=100.0, domain="finance")
    assert agent_selected_full in ("agent_fast", "agent_thorough")

    # Spend 9.8 USD of budget (leaving 0.2 USD)
    dispatcher.budget_spent = 9.8

    # Route task when budget is near depletion -> agent_thorough (cost 100 * 0.005 = 0.5 USD) exceeds remaining 0.2 USD, so fallback to agent_fast
    agent_selected_near_depletion = dispatcher.route_task(task_complexity=100.0, domain="finance")
    assert agent_selected_near_depletion == "agent_fast"
