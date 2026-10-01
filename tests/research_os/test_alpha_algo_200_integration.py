# -*- coding: utf-8 -*-
"""
test_alpha_algo_200_integration.py: Unit and integration test suite for 200-paper corpus (IDs 301-500)
and runtime components (CodeRewriteEngine, GeneticWorkflowOptimizer, SFTPreferenceCollector, LearnableRoutingGateDispatcher, ResearchOS).
"""

import pytest
import os
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
    SpecializedAgentProfile,
    ALPHAALGO_200_PRINCIPLES
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_200_paper_corpus_uniqueness():
    """Verify that the 200-paper database has zero duplicate titles or DOIs."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_200_NEW_RESEARCH.yaml"
    assert os.path.exists(yaml_path), f"YAML file missing: {yaml_path}"

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 200, f"Expected 200 papers, found {len(papers)}"

    titles = set()
    dois = set()
    for p in papers:
        t = p["metadata"]["title"].strip().lower()
        d = p["metadata"].get("doi", "").strip().lower()
        assert t not in titles, f"Duplicate title detected: {t}"
        titles.add(t)
        if d:
            assert d not in dois, f"Duplicate DOI detected: {d}"
            dois.add(d)


def test_principle_registration_and_literature_review():
    """Verify principle registration and ResearchOS literature review querying."""
    principles = register_200_paper_corpus_principles()
    assert len(principles) == len(ALPHAALGO_200_PRINCIPLES)

    ros = ResearchOS()
    res = ros.conduct_literature_review("EIOS")
    assert res["domain"] == "EIOS"
    assert len(res["matching_principles"]) > 0


def test_code_rewrite_engine_hawkes_ast_check(tmp_path):
    """Verify CodeRewriteEngine Hawkes AST recursion depth validation."""
    engine = CodeRewriteEngine(allowed_paths=[str(tmp_path)])

    # Recursive function with excessive calls
    bad_code = """
def infinite_recurse(x):
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
    infinite_recurse(x)
"""
    proposal = RewriteProposal(
        target_filepath=os.path.join(str(tmp_path), "test.py"),
        original_snippet="",
        proposed_snippet=bad_code,
        rationale="Testing Hawkes call depth limit"
    )

    valid = engine.verify_proposal_ast(proposal, max_call_depth=5)
    assert valid is False


def test_genetic_optimizer_map_elites_gate():
    """Verify MAP-Elites island migration gate in GeneticWorkflowOptimizer."""
    opt = GeneticWorkflowOptimizer(population_size=3)
    opt.initialize_population("Base prompt", {"lr": 0.01})
    opt.evaluate_generation(lambda g: 1.0)

    external_genome = ProgramGenome(
        prompt_template="External elite prompt",
        parameters={"lr": 0.05},
        fitness_score=10.0
    )

    accepted = opt.accept_island_migration(external_genome)
    assert accepted is True
    assert opt.population[0].fitness_score == 10.0


def test_sft_preference_collector_advantage_clipping():
    """Verify trajectory advantage calculation with max clipping."""
    collector = SFTPreferenceCollector(discount_factor=0.9, max_advantage_clip=2.0)
    steps = [
        TrajectoryStep(action="step1", predicted_expectation=0.0, actual_outcome=10.0, reward=100.0)
    ]
    advantages = collector.compute_advantages(steps)
    assert advantages[0] <= 2.0


def test_learnable_routing_dispatcher_efe():
    """Verify budget-bounded Active Inference task routing."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=100.0)
    dispatcher.register_subagent(SpecializedAgentProfile(
        agent_id="agent_quant",
        domain_specialty="Finance",
        cost_per_token=0.01,
        historical_success_rate=0.9,
        epistemic_curiosity=0.8
    ))

    selected = dispatcher.route_task(task_complexity=10.0, domain="Finance")
    assert selected == "agent_quant"
