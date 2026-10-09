# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for the 100 new research papers
corpus (IDs 301-400), principle extraction, literature review querying, and runtime component enhancements.
"""

import os
import pytest
import yaml
from apodex.ai_eos.research.integration import (
    ALPHAALGO_301_400_PRINCIPLES,
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


def test_301_400_paper_corpus_yaml_integrity():
    """Verify that the 100-paper corpus YAML exists, has 100 papers, and zero duplicate titles/DOIs."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    assert os.path.exists(yaml_path), f"File {yaml_path} does not exist."

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 100, f"Expected 100 papers, found {len(papers)}."

    paper_ids = [p["id"] for p in papers]
    assert min(paper_ids) == 301 and max(paper_ids) == 400

    # Load 1-300 DB papers to check zero overlap
    existing_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]
    existing_titles = set()
    existing_dois = set()

    for p_path in existing_paths:
        if os.path.exists(p_path):
            with open(p_path, "r", encoding="utf-8") as f:
                db = yaml.safe_load(f)
            for p in db.get("papers", []):
                meta = p.get("metadata", {})
                t = meta.get("title") or p.get("title")
                d = meta.get("doi") or p.get("doi")
                if t:
                    existing_titles.add(t.strip().lower())
                if d:
                    existing_dois.add(d.strip().lower())

    for p in papers:
        meta = p["metadata"]
        title = meta["title"].strip().lower()
        doi = meta["doi"].strip().lower()

        assert title not in existing_titles, f"Duplicate title found: {title}"
        assert doi not in existing_dois, f"Duplicate DOI found: {doi}"


def test_principle_registration_and_literature_review():
    """Verify registration of 301-400 principles and ResearchOS literature review lookup."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == len(ALPHAALGO_301_400_PRINCIPLES) == 4

    ros = ResearchOS()
    review = ros.conduct_literature_review("CodeRewriteEngine")
    assert review["domain"] == "CodeRewriteEngine"
    assert len(review["matched_principles"]) >= 1
    assert review["matched_principles"][0]["target_subsystem"] == "CodeRewriteEngine"


def test_code_rewrite_engine_hawkes_recursion_check():
    """Verify Hawkes AST non-Gaussian recursion depth check in CodeRewriteEngine."""
    engine = CodeRewriteEngine(allowed_paths=["."], max_recursion_depth=3)

    valid_snippet = """
def simple_fn(x):
    return x + 1
"""
    proposal_valid = engine.propose_rewrite("test.py", "", valid_snippet, "valid test")
    assert engine.verify_proposal_ast(proposal_valid) is True

    recursive_snippet = """
def runaway_fn(x):
    return runaway_fn(x) + runaway_fn(x) + runaway_fn(x) + runaway_fn(x) + runaway_fn(x)
"""
    proposal_invalid = engine.propose_rewrite("test.py", "", recursive_snippet, "invalid test")
    assert engine.verify_proposal_ast(proposal_invalid) is False


def test_genetic_workflow_optimizer_bool_fix_and_island_migration():
    """Verify boolean parameter type integrity in mutation and island MAP-Elites migration gating."""
    optimizer = GeneticWorkflowOptimizer(population_size=4, mutation_rate=1.0)
    params = {"enabled": True, "threshold": 0.5, "count": 10}

    mutated = optimizer._mutate_parameters(params)
    assert isinstance(mutated["enabled"], bool)
    assert mutated["enabled"] is False  # Flipped from True with rate=1.0

    # Initialize population and test MAP-Elites migration
    optimizer.initialize_population("template", params)

    migrant = ProgramGenome(
        prompt_template="migrant template",
        parameters={"enabled": True},
        fitness_score=999.0
    )
    accepted = optimizer.insert_migrant_elite(migrant)
    assert accepted is True
    assert optimizer.population[0].fitness_score == 999.0


def test_sft_preference_collector_clipped_advantage_margins():
    """Verify clipped trajectory advantage margin bounds in DPO preference compilation."""
    collector = SFTPreferenceCollector(discount_factor=0.9, margin_clip_bound=8.0)

    steps_a = [TrajectoryStep(action="act_a", predicted_expectation=0.0, actual_outcome=1.0, reward=100.0)]
    steps_b = [TrajectoryStep(action="act_b", predicted_expectation=0.0, actual_outcome=0.0, reward=0.0)]

    pair = collector.compile_dpo_preference_pair("prompt", steps_a, steps_b)

    assert pair["unclipped_margin"] == 100.0
    assert pair["margin"] == 8.0  # Clipped to margin_clip_bound=8.0


def test_learnable_routing_gate_dispatcher_efe_routing():
    """Verify budget-decayed EFE task routing in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_a = SpecializedAgentProfile(
        agent_id="agent_a",
        domain_specialty="finance",
        cost_per_token=0.001,
        historical_success_rate=0.8,
        epistemic_curiosity=0.7
    )
    dispatcher.register_subagent(agent_a)

    selected = dispatcher.route_task(task_complexity=100.0, domain="finance")
    assert selected == "agent_a"

    # Simulate budget exhaustion and verify fallback behavior
    dispatcher.budget_spent = 9.95
    selected_exhausted = dispatcher.route_task(task_complexity=100.0, domain="finance")
    assert selected_exhausted == "agent_a"  # Fallback to cheapest
