# -*- coding: utf-8 -*-
"""
test_alpha_algo_301_400_integration.py: Integration test suite for AlphaAlgo 301-400 paper corpus.
Validates zero corpus overlap across all 400 papers, principle registration, literature review multi-field
search, and runtime enhancements/flaw fixes across Research OS, CodeRewriteEngine, GeneticWorkflowOptimizer,
SFTPreferenceCollector, and LearnableRoutingGateDispatcher.
"""

import os
import math
import yaml
import pytest
from apodex.ai_eos.research.integration import (
    register_301_400_paper_corpus_principles,
    ALPHAALGO_301_400_PRINCIPLES,
    CodeRewriteEngine,
    RewriteProposal,
    GeneticWorkflowOptimizer,
    SFTPreferenceCollector,
    TrajectoryStep,
    LearnableRoutingGateDispatcher,
    SpecializedAgentProfile
)
from apodex.ai_eos.research.research_os import ResearchOS


def test_zero_corpus_overlap_301_400():
    """Verifies 100% zero overlap and unique DOIs/titles for papers 301-400 against papers 1-300."""
    baseline_files = [
        "docs/research/papers/AI_EOS_RESEARCH_DB.yaml",
        "docs/research/papers/ALPHA_ALGO_100_NEW_RESEARCH.yaml"
    ]
    new_file = "docs/research/papers/ALPHA_ALGO_301_400_RESEARCH.yaml"

    baseline_titles = []
    baseline_dois = set()

    for bf in baseline_files:
        assert os.path.exists(bf), f"Baseline research YAML file {bf} missing."
        with open(bf, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for p in data.get("papers", []):
            title = p["metadata"]["title"].lower().strip()
            doi = p["metadata"].get("doi", "").lower().strip()
            if title:
                baseline_titles.append(title)
            if doi:
                baseline_dois.add(doi)

    assert len(baseline_titles) == 300, f"Expected 300 baseline papers, found {len(baseline_titles)}"

    assert os.path.exists(new_file), f"New research YAML file {new_file} missing."
    with open(new_file, "r", encoding="utf-8") as f:
        new_data = yaml.safe_load(f)

    new_papers = new_data.get("papers", [])
    assert len(new_papers) == 100, f"Expected 100 new papers in 301-400 corpus, found {len(new_papers)}"

    for p in new_papers:
        title = p["metadata"]["title"].lower().strip()
        doi = p["metadata"].get("doi", "").lower().strip()

        if doi:
            assert doi not in baseline_dois, f"Duplicate DOI detected across corpus: {doi}"

        p_tokens = set(title.split())
        for ext in baseline_titles:
            ext_tokens = set(ext.split())
            if p_tokens and ext_tokens:
                intersection = p_tokens.intersection(ext_tokens)
                union = p_tokens.union(ext_tokens)
                jaccard = len(intersection) / len(union)
                assert jaccard <= 0.30, f"High title similarity ({jaccard:.2f}) between '{title}' and '{ext}'"


def test_register_301_400_principles():
    """Verifies that 100 principles from papers 301-400 are correctly registered."""
    principles = register_301_400_paper_corpus_principles()
    assert len(principles) == 100
    assert 301 in principles
    assert 400 in principles
    assert principles[301]["category"] == "Market Microstructure"
    assert principles[325]["category"] == "Active Inference"
    assert principles[345]["category"] == "RL & Alignment"
    assert principles[365]["category"] == "Multi-Agent Systems"
    assert principles[385]["category"] == "Evolutionary Search"


def test_code_rewrite_engine_hawkes_ast_depth_check(tmp_path):
    """Verifies that CodeRewriteEngine enforces Hawkes recursion depth checks on proposed snippets."""
    engine = CodeRewriteEngine(allowed_paths=[str(tmp_path)])

    deep_recursion_snippet = """
def deep_recursion(n):
    if n <= 0:
        return 0
    return deep_recursion(n-1) + deep_recursion(n-2) + deep_recursion(n-3) + deep_recursion(n-4) + deep_recursion(n-5) + deep_recursion(n-6) + deep_recursion(n-7) + deep_recursion(n-8) + deep_recursion(n-9) + deep_recursion(n-10) + deep_recursion(n-11)
"""

    proposal = engine.propose_rewrite(
        filepath=str(tmp_path / "test_module.py"),
        original_snippet="",
        proposed_snippet=deep_recursion_snippet,
        rationale="Deep recursive optimization test"
    )

    assert not engine.verify_proposal_ast(proposal, max_call_depth=5)

    safe_snippet = """
def safe_calculator(a, b):
    return a + b
"""
    safe_proposal = engine.propose_rewrite(
        filepath=str(tmp_path / "test_module.py"),
        original_snippet="",
        proposed_snippet=safe_snippet,
        rationale="Safe function rewrite"
    )
    assert engine.verify_proposal_ast(safe_proposal, max_call_depth=5)


def test_genetic_workflow_optimizer_map_elites():
    """Verifies MAP-Elites re-sorting and parameter mutation safeguards in GeneticWorkflowOptimizer."""
    optimizer = GeneticWorkflowOptimizer(population_size=10, mutation_rate=0.5)
    optimizer.initialize_population(
        base_template="Base Directive",
        base_params={"pop_size": 10, "mutation_rate": 0.2, "budget": 100.0}
    )

    mutated = optimizer._mutate_parameters({"pop_size": -10, "mutation_rate": -0.5, "budget": -50.0})
    assert mutated["pop_size"] >= 0
    assert mutated["mutation_rate"] >= 0
    assert mutated["budget"] >= 0

    def score_fn(g):
        return len(g.prompt_template) * 0.1

    eval_pop = optimizer.evaluate_generation(score_fn)
    for i in range(len(eval_pop) - 1):
        assert eval_pop[i].fitness_score >= eval_pop[i + 1].fitness_score

    optimizer.perform_crossover_and_mutation()
    for i in range(len(optimizer.population) - 1):
        assert optimizer.population[i].fitness_score >= optimizer.population[i + 1].fitness_score


def test_sft_preference_collector_clipped_advantage():
    """Verifies that SFTPreferenceCollector clips trajectory advantage margins."""
    collector = SFTPreferenceCollector(discount_factor=0.99)

    steps_a = [
        TrajectoryStep(action="a1", predicted_expectation=0.0, actual_outcome=1.0, reward=100.0),
        TrajectoryStep(action="a2", predicted_expectation=0.0, actual_outcome=1.0, reward=200.0)
    ]
    steps_b = [
        TrajectoryStep(action="b1", predicted_expectation=0.0, actual_outcome=0.0, reward=-50.0),
        TrajectoryStep(action="b2", predicted_expectation=0.0, actual_outcome=0.0, reward=-100.0)
    ]

    pref_pair = collector.compile_dpo_preference_pair("Optimize portfolio allocation", steps_a, steps_b)

    assert "chosen" in pref_pair
    assert "rejected" in pref_pair
    assert "margin" in pref_pair
    assert "raw_margin" in pref_pair
    assert abs(pref_pair["margin"]) <= 5.0
    assert pref_pair["raw_margin"] > pref_pair["margin"]


def test_learnable_routing_gate_budget_decay():
    """Verifies budget-decayed Expected Free Energy routing in LearnableRoutingGateDispatcher."""
    dispatcher = LearnableRoutingGateDispatcher(budget_limit_usd=10.0)

    agent_expensive = SpecializedAgentProfile(
        agent_id="agent_quant_expert",
        domain_specialty="Quantitative Finance",
        cost_per_token=0.001,
        historical_success_rate=0.9,
        epistemic_curiosity=0.8
    )
    agent_cheap = SpecializedAgentProfile(
        agent_id="agent_fast_cheap",
        domain_specialty="Quantitative Finance",
        cost_per_token=0.0001,
        historical_success_rate=0.7,
        epistemic_curiosity=0.4
    )

    dispatcher.register_subagent(agent_expensive)
    dispatcher.register_subagent(agent_cheap)

    # High remaining budget: selects expert
    selected_high_budget = dispatcher.route_task(task_complexity=10.0, domain="Quantitative Finance")
    assert selected_high_budget == "agent_quant_expert"

    # Spend almost all budget ($9.80 spent out of $10.0)
    dispatcher.budget_spent = 9.80

    # Low remaining budget: budget decay penalizes expensive agent, selecting cheap agent
    selected_low_budget = dispatcher.route_task(task_complexity=10.0, domain="Quantitative Finance")
    assert selected_low_budget == "agent_fast_cheap"


def test_research_os_literature_review_multi_field():
    """Verifies ResearchOS conduct_literature_review multi-field semantic querying."""
    ros = ResearchOS()

    res_active = ros.conduct_literature_review("Active Inference")
    assert res_active["matched_principles_count"] > 0
    assert "synthesized_trends" in res_active
    assert any("Variational" in t or "Active" in t or "Epistemic" in t for t in res_active["synthesized_trends"])

    res_evo = ros.conduct_literature_review("Evolutionary Search")
    assert res_evo["matched_principles_count"] > 0
    assert any("MAP-Elites" in p["extracted_principle"] or "Genetic" in p["extracted_principle"] for p in res_evo["matched_principles"])
