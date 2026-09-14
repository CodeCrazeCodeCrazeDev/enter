# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for 301-400 paper corpus,
extracted principles, ResearchOS querying, and AlphaAlgo runtime flaw fixes.
"""

import os
import yaml
import tempfile
import pytest

from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
    CodeRewriteEngine, RewriteProposal,
    GeneticWorkflowOptimizer, ProgramGenome,
    SFTPreferenceCollector, TrajectoryStep,
    LearnableRoutingGateDispatcher, SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_301_400_paper_corpus_zero_overlap():
    """Verify that all 400 papers (1-400) have 100% zero title and DOI overlap."""
    yaml_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    ]

    all_titles = set()
    all_dois = set()
    total_paper_count = 0

    for path in yaml_paths:
        assert os.path.exists(path), f"Corpus YAML file missing: {path}"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        papers = data if isinstance(data, list) else data.get("papers", [])
        total_paper_count += len(papers)

        for p in papers:
            meta = p.get("metadata", {})
            t = (p.get("title") or meta.get("title", "")).strip().lower()
            d = (p.get("doi") or meta.get("doi", "")).strip().lower()

            if t:
                assert t not in all_titles, f"Duplicate paper title detected across corpora: '{t}'"
                all_titles.add(t)
            if d:
                assert d not in all_dois, f"Duplicate paper DOI detected across corpora: '{d}'"
                all_dois.add(d)

    assert total_paper_count == 400, f"Expected exactly 400 total research papers, found {total_paper_count}"


def test_301_400_principles_registration_and_research_os():
    """Verify registration of 301-400 paper corpus principles and ResearchOS literature review synthesis."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 5
    assert principles == ALPHAALGO_301_400_PRINCIPLES

    ros = ResearchOS()
    review = ros.conduct_literature_review("Active Inference")
    assert review["reviewed_citations_count"] == 100
    assert "principles" in review
    assert len(review["principles"]) >= 1


def test_code_rewrite_hawkes_stability():
    """Verify Non-Gaussian Hawkes Process Stability check in CodeRewriteEngine."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_file.py")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("def foo(): return 1\n")

        engine = CodeRewriteEngine(allowed_paths=[tmpdir], max_mutations_per_file=2)

        # Register recent mutations to simulate high self-exciting branching ratio
        for _ in range(4):
            engine.mutation_history.setdefault(filepath, []).append(
                RewriteProposal(target_filepath=filepath, original_snippet="x", proposed_snippet="y", rationale="test")
            )

        proposal = engine.propose_rewrite(
            filepath=filepath,
            original_snippet="def foo(): return 1\n",
            proposed_snippet="def foo(): return 2\n",
            rationale="Update return value"
        )

        # Dry run simulation should be vetoed due to Hawkes instability
        assert engine.dry_run_simulation(proposal) is False


def test_island_map_elites_migration():
    """Verify Island MAP-Elites migration gates in GeneticWorkflowOptimizer."""
    optimizer = GeneticWorkflowOptimizer(population_size=4, num_islands=2)
    optimizer.island_populations[0] = [
        ProgramGenome(prompt_template="template_a", fitness_score=0.9, behavioral_descriptor=[0.1, 0.1])
    ]
    optimizer.island_populations[1] = [
        ProgramGenome(prompt_template="template_b", fitness_score=0.5, behavioral_descriptor=[0.9, 0.9])
    ]

    migrated = optimizer.evaluate_island_migration(novelty_threshold=0.3)
    assert migrated >= 1
    assert len(optimizer.island_populations[1]) == 2


def test_sft_preference_collector_trajectory_penalty():
    """Verify trajectory length distance penalty in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(trajectory_penalty_beta=0.1)

    steps_direct = [
        TrajectoryStep(action="direct_solve", predicted_expectation=0.5, actual_outcome=1.0, reward=1.0)
    ]

    steps_bloated = [
        TrajectoryStep(action="filler_1", predicted_expectation=0.5, actual_outcome=0.0, reward=0.0),
        TrajectoryStep(action="filler_2", predicted_expectation=0.5, actual_outcome=0.0, reward=0.0),
        TrajectoryStep(action="filler_3", predicted_expectation=0.5, actual_outcome=0.0, reward=0.0),
        TrajectoryStep(action="final_solve", predicted_expectation=0.5, actual_outcome=1.0, reward=1.0)
    ]

    pair = collector.compile_dpo_preference_pair("Solve task", steps_direct, steps_bloated)
    assert "direct_solve" in pair["chosen"]
    assert pair["margin"] > 0.0


def test_learnable_routing_causal_do_calculus():
    """Verify Pearl do-calculus interventional routing in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=100.0)
    dispatcher.register_subagent(
        SpecializedAgentProfile(agent_id="active_inf_agent", domain_specialty="Active Inference", cost_per_token=0.01)
    )
    dispatcher.register_subagent(
        SpecializedAgentProfile(agent_id="finance_agent", domain_specialty="Finance", cost_per_token=0.01)
    )

    routed = dispatcher.route_task(task_complexity=10.0, domain="Active Inference", perform_causal_intervention=True)
    assert routed == "active_inf_agent"
