# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200-paper corpus,
extracted transferable engineering principles, and core subsystem enhancements.
"""

import os
import yaml
import tempfile
import pytest

from apodex.ai_eos.research.integration import (
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile,
    register_200_paper_corpus_principles,
    ALPHAALGO_200_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_200_paper_corpus_and_bibliography_files_exist():
    yaml_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    bib_path = "docs/research/papers/ALPHA_ALGO_200_NEW_BIBLIOGRAPHY.md"

    assert os.path.exists(yaml_path), f"Missing {yaml_path}"
    assert os.path.exists(bib_path), f"Missing {bib_path}"

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers, found {len(papers)}"

    ids = [p["id"] for p in papers]
    assert min(ids) == 301 and max(ids) == 500, f"Unexpected ID range: {min(ids)} to {max(ids)}"


def test_zero_title_overlap_across_all_research_databases():
    db_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    ]

    titles = set()
    total_papers = 0

    for path in db_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            papers = data.get("papers", []) if isinstance(data, dict) else data
            for p in papers:
                total_papers += 1
                t = p.get("metadata", {}).get("title", "").strip().lower()
                assert t, f"Missing title in paper {p.get('id')}"
                assert t not in titles, f"Duplicate title detected across databases: '{t}'"
                titles.add(t)

    assert total_papers == 500, f"Expected 500 total papers, got {total_papers}"
    assert len(titles) == 500, "Title count does not match total papers"


def test_principles_registration_and_researchos_query():
    principles = register_200_paper_corpus_principles()
    assert len(principles) >= 6
    assert principles == ALPHAALGO_200_PRINCIPLES

    ros = ResearchOS()
    review = ros.conduct_literature_review("reinforcement_learning")
    assert review["domain"] == "reinforcement_learning"
    assert review["reviewed_citations_count"] >= 15
    assert len(review["matched_principles"]) >= 1


def test_code_rewrite_engine_hawkes_ast_veto():
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = CodeRewriteEngine(allowed_paths=[tmpdir])
        fpath = os.path.join(tmpdir, "module.py")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("def original(): pass\n")

        # Unbounded recursion snippet
        deep_recursion_code = "def recursive_func():\n" + "\n".join(["    recursive_func()"] * 12)
        prop = engine.propose_rewrite(
            filepath=fpath,
            original_snippet="def original(): pass\n",
            proposed_snippet=deep_recursion_code,
            rationale="Testing Hawkes veto"
        )

        assert engine.verify_proposal_ast(prop) is False
        assert engine.commit_rewrite(prop) is False


def test_genetic_workflow_optimizer_and_sorting():
    optimizer = GeneticWorkflowOptimizer(population_size=5)
    optimizer.initialize_population(
        base_template="Task execution prompt",
        base_params={"temperature": 0.7, "max_tokens": 512}
    )
    assert len(optimizer.population) == 5

    def mock_eval(genome):
        return len(genome.prompt_template) * 0.1

    optimizer.evaluate_generation(mock_eval)
    optimizer.perform_crossover_and_mutation()

    assert len(optimizer.population) == 5
    # Verify population is sorted in descending order of fitness_score
    scores = [g.fitness_score for g in optimizer.population]
    assert scores == sorted(scores, reverse=True)


def test_sft_preference_collector_clipped_margins():
    collector = SFTPreferenceCollector(discount_factor=0.9)
    run_a = [TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=1.0, reward=20.0)]
    run_b = [TrajectoryStep(action="b1", predicted_expectation=0.0, actual_outcome=0.0, reward=0.0)]

    pair = collector.compile_dpo_preference_pair("Solve task", run_a, run_b)
    assert pair["margin"] == 5.0  # Clipped from 20.0 to upper bound 5.0
    assert pair["raw_margin"] == 20.0
    assert "a1" in pair["chosen"]


def test_learnable_routing_gate_dispatcher_efe():
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)
    dispatcher.register_subagent(SpecializedAgentProfile(
        agent_id="rl_expert",
        domain_specialty="rl",
        cost_per_token=0.01,
        historical_success_rate=0.9,
        epistemic_curiosity=0.8
    ))
    dispatcher.register_subagent(SpecializedAgentProfile(
        agent_id="general_agent",
        domain_specialty="general",
        cost_per_token=0.001,
        historical_success_rate=0.5,
        epistemic_curiosity=0.2
    ))

    selected = dispatcher.route_task(task_complexity=10.0, domain="rl")
    assert selected == "rl_expert"

    dispatcher.update_routing_parameters(selected, success=True, cost_incurred=0.1)
    assert dispatcher.budget_spent == 0.1
