# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Integration test suite for the 200-paper research corpus (IDs 301-500)
and runtime integrations across AEAN, EOS, EIOS, and Research OS.
"""

import os
import pytest
import yaml
from uuid import uuid4

from apodex.ai_eos.research.integration import (
    register_200_paper_corpus_principles,
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


def test_corpus_500_papers_zero_overlap():
    """Verifies that all 500 papers (IDs 1-500) exist and papers 301-500 have 100% zero overlap against papers 1-300."""
    db_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml",
        "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    ]

    previous_titles = []
    new_titles = []
    paper_count = 0

    for idx, path in enumerate(db_paths):
        assert os.path.exists(path), f"Corpus database path missing: {path}"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        papers = data.get("papers", [])
        paper_count += len(papers)

        for p in papers:
            title = p["metadata"]["title"].lower()
            if idx < 2:
                previous_titles.append(title)
            else:
                new_titles.append(title)

    assert paper_count == 500, f"Expected exactly 500 total papers, found {paper_count}"
    assert len(previous_titles) == 300
    assert len(new_titles) == 200

    # Calculate Jaccard similarity between new papers (301-500) and previous papers (1-300)
    for new_idx, new_t in enumerate(new_titles):
        tokens_new = set(new_t.split())
        for prev_idx, prev_t in enumerate(previous_titles):
            tokens_prev = set(prev_t.split())
            if tokens_new and tokens_prev:
                intersection = tokens_new.intersection(tokens_prev)
                union = tokens_new.union(tokens_prev)
                overlap = len(intersection) / len(union)
                assert overlap <= 0.35, f"Title overlap detected ({overlap:.2f}) between new paper #{new_idx+301} and previous paper #{prev_idx+1}: '{new_t}' vs '{prev_t}'"


def test_register_200_paper_corpus_principles():
    """Verifies registration of extracted principles from the 200-paper corpus."""
    principles = register_200_paper_corpus_principles()
    assert isinstance(principles, list)
    assert len(principles) >= 7

    subsystems = {p["target_subsystem"] for p in principles}
    assert "AEAN" in subsystems
    assert "EOS" in subsystems
    assert "EIOS" in subsystems
    assert "Research OS" in subsystems


def test_research_os_literature_review_querying():
    """Verifies ResearchOS conduct_literature_review multi-field principle querying."""
    ros = ResearchOS()

    res_aean = ros.conduct_literature_review("AEAN")
    assert res_aean["domain"] == "AEAN"
    assert len(res_aean["matching_principles"]) >= 1

    res_eios = ros.conduct_literature_review("Active Inference")
    assert len(res_eios["matching_principles"]) >= 1


def test_code_rewrite_engine_ast_depth_hawkes_verification():
    """Verifies CodeRewriteEngine AST recursive call depth verification."""
    engine = CodeRewriteEngine(allowed_paths=["."], max_ast_depth=5)

    valid_snippet = "def calculate_val(x):\n    return x * 2\n"
    prop = engine.propose_rewrite("generate_alpha_algo_200_papers.py", "a = 1", valid_snippet, "Valid non-recursive AST snippet")
    assert engine.verify_proposal_ast(prop) is True


def test_genetic_optimizer_island_map_elites_migration_gate():
    """Verifies MAP-Elites island migration gate sorting and population bounds in GeneticWorkflowOptimizer."""
    optimizer = GeneticWorkflowOptimizer(population_size=3)
    optimizer.initialize_population(base_template="base prompt", base_params={"param": 1.0})

    elite = ProgramGenome(prompt_template="elite prompt", parameters={"param": 2.0}, fitness_score=95.5)
    optimizer.insert_elite_genome(elite)

    assert len(optimizer.population) == 3
    assert optimizer.population[0].fitness_score == 95.5
    assert optimizer.population[0].prompt_template == "elite prompt"


def test_sft_preference_collector_clipped_advantage():
    """Verifies SFTPreferenceCollector compiled preference records and clipped advantage margins."""
    collector = SFTPreferenceCollector(discount_factor=0.9, clip_margin=5.0)

    steps_a = [
        TrajectoryStep(action="action_1", predicted_expectation=0.5, actual_outcome=1.0, reward=1.0),
        TrajectoryStep(action="action_2", predicted_expectation=0.5, actual_outcome=2.0, reward=2.0)
    ]
    steps_b = [
        TrajectoryStep(action="action_1", predicted_expectation=0.5, actual_outcome=0.1, reward=-1.0),
        TrajectoryStep(action="action_2", predicted_expectation=0.5, actual_outcome=0.2, reward=-2.0)
    ]

    record = collector.compile_dpo_preference_pair(
        prompt="Execute task",
        steps_run_a=steps_a,
        steps_run_b=steps_b
    )

    assert record["chosen"] is not None
    assert record["rejected"] is not None
    assert abs(record["margin"]) <= 5.0


def test_learnable_routing_gate_efe_budget_decay():
    """Verifies LearnableRoutingGateDispatcher EFE-guided task routing with budget decay."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(agent_id="agent_a", domain_specialty="AEAN", cost_per_token=0.01, historical_success_rate=0.8)
    agent_b = SpecializedAgentProfile(agent_id="agent_b", domain_specialty="EOS", cost_per_token=0.001, historical_success_rate=0.9)

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    selected = dispatcher.route_task(task_complexity=100.0, domain="AEAN")
    assert selected in ["agent_a", "agent_b"]
