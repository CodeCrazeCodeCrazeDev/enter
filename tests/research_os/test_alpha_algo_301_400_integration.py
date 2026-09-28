# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Unit and integration tests for the
100-paper research corpus (IDs 301-400), principle extraction, literature review querying,
and runtime component enhancements.
"""

import pytest
import os
import yaml
from uuid import uuid4
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
    CodeRewriteEngine,
    GeneticWorkflowOptimizer,
    ProgramGenome,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_301_400_corpus_yaml_integrity_and_zero_overlap():
    """Verifies that docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml contains 100 valid papers with zero overlap against papers 1-300."""
    yaml_path = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"
    assert os.path.exists(yaml_path), f"Corpus YAML file {yaml_path} does not exist!"

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    assert len(papers) == 100, f"Expected 100 papers, got {len(papers)}"

    # Check ID range
    paper_ids = [p["id"] for p in papers]
    assert min(paper_ids) == 301
    assert max(paper_ids) == 400
    assert len(set(paper_ids)) == 100

    # Load 1-300 databases to double check zero overlap
    existing_paths = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]
    existing_titles = set()
    existing_dois = set()

    for epath in existing_paths:
        if os.path.exists(epath):
            with open(epath, "r", encoding="utf-8") as f:
                edb = yaml.safe_load(f)
            epapers = edb if isinstance(edb, list) else edb.get("papers", [])
            for ep in epapers:
                meta = ep.get("metadata", {})
                if meta.get("title"):
                    existing_titles.add(meta["title"].strip().lower())
                if meta.get("doi"):
                    existing_dois.add(meta["doi"].strip().lower())

    for p in papers:
        meta = p["metadata"]
        title = meta["title"].strip().lower()
        doi = meta["doi"].strip().lower()

        assert title not in existing_titles, f"Duplicate title found: {title}"
        assert doi not in existing_dois, f"Duplicate DOI found: {doi}"


def test_register_301_400_principles():
    """Verifies registration of principles extracted from papers 301-400."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) >= 4
    assert "hawkes_non_gaussian_stability" in principles
    assert "amortized_active_inference_eoi" in principles
    assert "clamped_advantage_margin_dpo" in principles
    assert "island_map_elites_sorting" in principles


def test_research_os_literature_review_indexing_301_400():
    """Verifies that ResearchOS literature review indexes and retrieves paper 301-400 principles."""
    ros = ResearchOS()
    res = ros.conduct_literature_review("Market Microstructure")
    assert res["domain"] == "Market Microstructure"
    assert "matched_principles" in res
    assert len(res["matched_principles"]) >= 1


def test_code_rewrite_engine_hawkes_recursion_depth_veto():
    """Verifies that CodeRewriteEngine blocks proposals with recursive calls exceeding max_recursion_depth."""
    engine = CodeRewriteEngine(allowed_paths=["/tmp"], max_recursion_depth=2)

    # Valid non-recursive snippet
    valid_snippet = """
def calculate_sum(a, b):
    return a + b
"""
    proposal_valid = engine.propose_rewrite("/tmp/valid.py", "", valid_snippet, "Valid function")
    assert engine.verify_proposal_ast(proposal_valid) is True

    # Snippet exceeding max recursion depth
    excessive_recursion_snippet = """
def recursive_func(n):
    if n <= 0:
        return 0
    return recursive_func(n - 1) + recursive_func(n - 2) + recursive_func(n - 3)
"""
    proposal_excessive = engine.propose_rewrite("/tmp/excessive.py", "", excessive_recursion_snippet, "Recursive function")
    assert engine.verify_proposal_ast(proposal_excessive) is False


def test_genetic_workflow_optimizer_island_map_elites():
    """Verifies MAP-Elites island insertion and population re-sorting."""
    optimizer = GeneticWorkflowOptimizer(population_size=5)
    optimizer.initialize_population("base template", {"param_a": 1.0})

    # Insert elite genome with high fitness score
    elite = ProgramGenome(prompt_template="elite template", parameters={"param_a": 10.0}, fitness_score=99.0)
    optimizer.insert_elite_genome(elite)

    # Population should be sorted descending by fitness_score
    assert optimizer.population[0].fitness_score == 99.0
    assert len(optimizer.population) <= 5


def test_sft_preference_collector_clamped_margin():
    """Verifies advantage margin clipping in SFTPreferenceCollector."""
    collector = SFTPreferenceCollector(discount_factor=0.95, margin_clip_bound=10.0)

    steps_a = [
        TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=100.0, reward=100.0),
        TrajectoryStep(action="a2", predicted_expectation=0.0, actual_outcome=100.0, reward=100.0)
    ]
    steps_b = [
        TrajectoryStep(action="b1", predicted_expectation=10.0, actual_outcome=0.0, reward=-50.0)
    ]

    dpo_pair = collector.compile_dpo_preference_pair("Optimize portfolio", steps_a, steps_b)

    assert "prompt" in dpo_pair
    assert dpo_pair["margin"] <= 10.0
    assert dpo_pair["margin"] >= -10.0
    assert dpo_pair["raw_margin"] > 10.0  # Unclamped raw margin is larger than bound


def test_learnable_routing_gate_dispatcher_efe():
    """Verifies task routing using Expected Free Energy and remaining budget ratio."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=100.0)
    agent_a = SpecializedAgentProfile(agent_id="agent_a", domain_specialty="fintech", cost_per_token=0.01, historical_success_rate=0.8, epistemic_curiosity=0.2)
    agent_b = SpecializedAgentProfile(agent_id="agent_b", domain_specialty="general", cost_per_token=0.001, historical_success_rate=0.5, epistemic_curiosity=0.1)

    dispatcher.register_subagent(agent_a)
    dispatcher.register_subagent(agent_b)

    selected = dispatcher.route_task(task_complexity=10.0, domain="fintech")
    assert selected == "agent_a"
